"""Bounded-batch trusted postprocessing for ABI Contrail Masks.

The implementation keeps validation tensors on CPU and transfers only bounded
sample batches to the selected torch device.  It accelerates the provider-owned
Artifact Filters and metrics without exposing filter context to candidate code.
"""

from __future__ import annotations

import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any

import numpy as np

from abi_contrail.artifact_filters import (
    ABIArtifactFilterPipeline,
    GeographicFeatureFilter,
    ScanlineArtifactFilter,
)

_EPSILON = 1e-7


@dataclass(frozen=True)
class PreparedFilterContext:
    """Hot-loop representation of provider-only Artifact Filter context."""

    geographic_feature_mask: np.ndarray
    geographic_pre_rasterized: bool
    geographic_context_source: str
    diagnostic_georeferencing: Mapping[str, object] | None


@dataclass(frozen=True)
class OperationalPostprocessingResult:
    """Operational-threshold outputs and metric components."""

    raw_predictions: Any
    filtered_predictions: Any
    filter_diagnostics: tuple[dict[str, object], ...]
    raw_counts: tuple[dict[str, int], ...]
    filtered_counts: tuple[dict[str, int], ...]
    raw_metrics: tuple[dict[str, float], ...]
    filtered_metrics: tuple[dict[str, float], ...]
    raw_connectivity: tuple[float, ...]
    filtered_connectivity: tuple[float, ...]


class BoundedBatchPostprocessor:
    """Evaluate trusted ABI postprocessing in bounded CPU or CUDA batches."""

    def __init__(
        self,
        *,
        filter_pipeline: ABIArtifactFilterPipeline,
        device: str | Any = "cpu",
        batch_size: int = 8,
        progress_callback: Callable[[str], None] | None = None,
        log_every: int = 100,
        threshold_tile_size: int = 4,
    ) -> None:
        import torch

        if batch_size <= 0:
            raise ValueError("postprocessing batch_size must be positive")
        if log_every <= 0:
            raise ValueError("log_every must be positive")
        if threshold_tile_size <= 0:
            raise ValueError("threshold_tile_size must be positive")
        requested = torch.device(device)
        if requested.type == "cuda" and not torch.cuda.is_available():
            selected = torch.device("cpu")
        else:
            selected = requested
        self.filter_pipeline = filter_pipeline
        self.requested_device = str(requested)
        self.device = selected
        self.batch_size = int(batch_size)
        self.threshold_tile_size = int(threshold_tile_size)
        self.emit = progress_callback or (lambda _message: None)
        self.log_every = int(log_every)
        self.report: dict[str, object] = {
            "backend": "torch_cuda" if selected.type == "cuda" else "torch_cpu",
            "requested_device": str(requested),
            "device": str(selected),
            "batch_size": self.batch_size,
            "threshold_tile_size": self.threshold_tile_size,
            "bounded_device_batches": True,
            "full_validation_gpu_residency": False,
            "timings_seconds": {},
            "target_skeleton_batches": 0,
        }
        self._validate_pipeline()

    def prepare_contexts(
        self,
        *,
        dataset: object,
        sample_count: int,
        prediction_shape: tuple[int, int],
    ) -> tuple[PreparedFilterContext, ...]:
        """Read each provider context once and pre-rasterize geographic masks."""

        geographic = self._geographic_filter()
        started = time.monotonic()
        self.emit(f"Artifact Filter context preparation started; samples={sample_count}")
        prepared: list[PreparedFilterContext] = []
        for index in range(sample_count):
            context = _filter_context(dataset, index) if geographic is not None else {}
            pre_rasterized = context.get("geographic_feature_mask") is not None
            if geographic is None:
                feature_mask = np.zeros(prediction_shape, dtype=bool)
                source = "none"
            else:
                feature_mask = geographic.feature_mask_for_prediction(prediction_shape, context)
                source = (
                    "pre_rasterized_mask"
                    if pre_rasterized
                    else "provider_longitude_latitude"
                    if geographic.active
                    else "none"
                )
            prepared.append(
                PreparedFilterContext(
                    geographic_feature_mask=np.asarray(feature_mask, dtype=bool),
                    geographic_pre_rasterized=pre_rasterized,
                    geographic_context_source=source,
                    diagnostic_georeferencing=_prepare_georeferencing(context, prediction_shape),
                )
            )
            _emit_periodic_progress(
                self.emit,
                phase="Artifact Filter context preparation",
                completed=index + 1,
                total=sample_count,
                started_at=started,
                log_every=self.log_every,
            )
        elapsed = time.monotonic() - started
        self._record_timing("artifact_filter_context_preparation", elapsed)
        self.emit(f"Artifact Filter context preparation complete; elapsed={elapsed:.3f}s")
        return tuple(prepared)

    def evaluate_operational(
        self,
        *,
        probabilities: Any,
        targets: Any,
        threshold: float,
        contexts: Sequence[PreparedFilterContext],
    ) -> OperationalPostprocessingResult:
        """Apply filters and compute ordinary/connectivity metrics by batch."""

        import torch

        probs = probabilities.detach().cpu()
        target_masks = targets.detach().cpu() >= 0.5
        sample_count = int(probs.shape[0])
        if len(contexts) != sample_count:
            raise ValueError("prepared context count does not match probabilities")
        self.report["sample_count"] = sample_count
        self.report["max_device_batch_samples"] = min(self.batch_size, sample_count)

        filter_started = time.monotonic()
        self.emit(f"Artifact Filter phase started; samples={sample_count} device={self.device}")
        raw_batches: list[Any] = []
        filtered_batches: list[Any] = []
        diagnostics: list[dict[str, object]] = []
        for start, end in _batch_ranges(sample_count, self.batch_size):
            probability_batch = probs[start:end].to(self.device)
            raw_batch = probability_batch >= threshold
            filtered_batch, batch_diagnostics = self._apply_filters(
                raw_batch,
                probability_batch,
                contexts[start:end],
                build_diagnostics=True,
            )
            raw_batches.append(raw_batch.cpu())
            filtered_batches.append(filtered_batch.cpu())
            diagnostics.extend(batch_diagnostics)
            _emit_periodic_progress(
                self.emit,
                phase="Artifact Filter phase",
                completed=end,
                total=sample_count,
                started_at=filter_started,
                log_every=self.log_every,
            )
        self._synchronize()
        raw_predictions = torch.cat(raw_batches) if raw_batches else probs >= threshold
        filtered_predictions = torch.cat(filtered_batches) if filtered_batches else raw_predictions.clone()
        filter_elapsed = time.monotonic() - filter_started
        self._record_timing("artifact_filter", filter_elapsed)
        self.emit(f"Artifact Filter phase complete; elapsed={filter_elapsed:.3f}s")

        ordinary_started = time.monotonic()
        self.emit(f"ordinary metric phase started; samples={sample_count} device={self.device}")
        raw_counts: list[dict[str, int]] = []
        filtered_counts: list[dict[str, int]] = []
        raw_metrics: list[dict[str, float]] = []
        filtered_metrics: list[dict[str, float]] = []
        for start, end in _batch_ranges(sample_count, self.batch_size):
            raw_batch = raw_predictions[start:end].to(self.device)
            filtered_batch = filtered_predictions[start:end].to(self.device)
            target_batch = target_masks[start:end].to(self.device)
            batch_raw_counts = _confusion_counts_by_sample(raw_batch, target_batch)
            batch_filtered_counts = _confusion_counts_by_sample(filtered_batch, target_batch)
            for counts in batch_raw_counts:
                raw_counts.append(counts)
                raw_metrics.append(_metrics_from_counts(counts))
            for counts in batch_filtered_counts:
                filtered_counts.append(counts)
                filtered_metrics.append(_metrics_from_counts(counts))
            _emit_periodic_progress(
                self.emit,
                phase="ordinary metric phase",
                completed=end,
                total=sample_count,
                started_at=ordinary_started,
                log_every=self.log_every,
            )
        self._synchronize()
        ordinary_elapsed = time.monotonic() - ordinary_started
        self._record_timing("ordinary_metric", ordinary_elapsed)
        self.emit(f"ordinary metric phase complete; elapsed={ordinary_elapsed:.3f}s")

        connectivity_started = time.monotonic()
        self.emit(f"connectivity metric phase started; samples={sample_count} device={self.device}")
        raw_connectivity: list[float] = []
        filtered_connectivity: list[float] = []
        target_skeleton_batches = 0
        for start, end in _batch_ranges(sample_count, self.batch_size):
            raw_batch = raw_predictions[start:end].to(self.device)
            filtered_batch = filtered_predictions[start:end].to(self.device)
            target_batch = target_masks[start:end].to(self.device)
            target_skeleton = _soft_skeletonize(target_batch.float(), iterations=32)
            target_skeleton_batches += 1
            raw_scores = _cldice_scores_with_target_skeleton(raw_batch, target_batch, target_skeleton)
            filtered_scores = _cldice_scores_with_target_skeleton(filtered_batch, target_batch, target_skeleton)
            raw_connectivity.extend(float(value) for value in raw_scores.cpu().tolist())
            filtered_connectivity.extend(float(value) for value in filtered_scores.cpu().tolist())
            _emit_periodic_progress(
                self.emit,
                phase="connectivity metric phase",
                completed=end,
                total=sample_count,
                started_at=connectivity_started,
                log_every=self.log_every,
            )
        self._synchronize()
        connectivity_elapsed = time.monotonic() - connectivity_started
        self._record_timing("connectivity_metric", connectivity_elapsed)
        self.report["target_skeleton_batches"] = target_skeleton_batches
        self.emit(
            "connectivity metric phase complete; "
            f"elapsed={connectivity_elapsed:.3f}s target_skeleton_batches={target_skeleton_batches}"
        )

        return OperationalPostprocessingResult(
            raw_predictions=raw_predictions,
            filtered_predictions=filtered_predictions,
            filter_diagnostics=tuple(diagnostics),
            raw_counts=tuple(raw_counts),
            filtered_counts=tuple(filtered_counts),
            raw_metrics=tuple(raw_metrics),
            filtered_metrics=tuple(filtered_metrics),
            raw_connectivity=tuple(raw_connectivity),
            filtered_connectivity=tuple(filtered_connectivity),
        )

    def threshold_sweep_counts(
        self,
        *,
        probabilities: Any,
        targets: Any,
        thresholds: Sequence[float],
        contexts: Sequence[PreparedFilterContext],
    ) -> tuple[tuple[dict[str, int], ...], tuple[dict[str, int], ...]]:
        """Accumulate raw/filtered threshold counts without full GPU residency."""

        import torch

        probs = torch.nan_to_num(
            probabilities.detach().cpu().float(),
            nan=float("-inf"),
            posinf=1.0,
            neginf=float("-inf"),
        )
        target_masks = targets.detach().cpu() >= 0.5
        threshold_values = tuple(float(value) for value in thresholds)
        sample_count = int(probs.shape[0])
        raw_totals = [_empty_counts() for _ in threshold_values]
        filtered_totals = [_empty_counts() for _ in threshold_values]
        started = time.monotonic()
        self.emit(
            f"threshold-sweep phase started; thresholds={len(threshold_values)} "
            f"samples={sample_count} device={self.device}"
        )
        for start, end in _batch_ranges(sample_count, self.batch_size):
            probability_batch = probs[start:end].to(self.device)
            target_batch = target_masks[start:end].to(self.device)
            batch_contexts = contexts[start:end]
            for threshold_start in range(0, len(threshold_values), self.threshold_tile_size):
                tile = threshold_values[threshold_start : threshold_start + self.threshold_tile_size]
                threshold_tensor = torch.as_tensor(tile, dtype=probability_batch.dtype, device=self.device)
                raw = probability_batch.unsqueeze(0) >= threshold_tensor.reshape(-1, 1, 1, 1, 1)
                tile_count, batch_count = int(raw.shape[0]), int(raw.shape[1])
                flat_raw = raw.reshape(tile_count * batch_count, *raw.shape[2:])
                flat_probabilities = probability_batch.unsqueeze(0).expand(tile_count, *probability_batch.shape).reshape_as(flat_raw)
                repeated_contexts = tuple(context for _threshold in tile for context in batch_contexts)
                flat_filtered, _ = self._apply_filters(
                    flat_raw,
                    flat_probabilities,
                    repeated_contexts,
                    build_diagnostics=False,
                )
                repeated_targets = target_batch.unsqueeze(0).expand(tile_count, *target_batch.shape)
                raw_tile_counts = _confusion_counts_by_threshold(raw, repeated_targets)
                filtered_tile_counts = _confusion_counts_by_threshold(
                    flat_filtered.reshape_as(raw),
                    repeated_targets,
                )
                for offset, counts in enumerate(raw_tile_counts):
                    _add_counts(raw_totals[threshold_start + offset], counts)
                for offset, counts in enumerate(filtered_tile_counts):
                    _add_counts(filtered_totals[threshold_start + offset], counts)
            _emit_periodic_progress(
                self.emit,
                phase="threshold-sweep phase samples",
                completed=end,
                total=sample_count,
                started_at=started,
                log_every=self.log_every,
            )
        self._synchronize()
        elapsed = time.monotonic() - started
        self._record_timing("threshold_sweep", elapsed)
        self.emit(f"threshold-sweep phase complete; elapsed={elapsed:.3f}s")
        return tuple(raw_totals), tuple(filtered_totals)

    def _apply_filters(
        self,
        predictions: Any,
        probabilities: Any,
        contexts: Sequence[PreparedFilterContext],
        *,
        build_diagnostics: bool,
    ) -> tuple[Any, list[dict[str, object]]]:
        import torch

        current_mask = predictions.bool()
        current_probabilities = probabilities.float()
        per_filter_removed: list[Any] = []
        geographic_masks: Any | None = None
        for artifact_filter in self.filter_pipeline.filters:
            if isinstance(artifact_filter, GeographicFeatureFilter):
                geographic_masks = torch.from_numpy(
                    np.stack([context.geographic_feature_mask for context in contexts], axis=0)[:, np.newaxis]
                ).to(device=self.device, dtype=torch.bool)
                removed = torch.logical_and(current_mask, geographic_masks)
            elif isinstance(artifact_filter, ScanlineArtifactFilter):
                removed = _scanline_removed_mask(
                    current_mask,
                    current_probabilities,
                    min_length_pixels=artifact_filter.min_length_pixels,
                    max_probability_std=artifact_filter.max_probability_std,
                )
            else:  # guarded by _validate_pipeline
                raise TypeError(f"unsupported accelerated Artifact Filter: {type(artifact_filter).__name__}")
            per_filter_removed.append(removed)
            current_mask = torch.logical_and(current_mask, ~removed)
            current_probabilities = torch.where(removed, torch.zeros((), device=self.device), current_probabilities)

        if not build_diagnostics:
            return current_mask, []

        diagnostics: list[dict[str, object]] = []
        for sample_index, context in enumerate(contexts):
            filter_records: list[dict[str, object]] = []
            total_removed = torch.zeros_like(current_mask[sample_index], dtype=torch.bool)
            for filter_index, artifact_filter in enumerate(self.filter_pipeline.filters):
                removed = per_filter_removed[filter_index][sample_index]
                total_removed |= removed
                removed_count = int(removed.sum().item())
                if isinstance(artifact_filter, GeographicFeatureFilter):
                    feature_mask = context.geographic_feature_mask
                    filter_records.append(
                        {
                            "filter": artifact_filter.name,
                            "active": artifact_filter.active or context.geographic_pre_rasterized,
                            "available": artifact_filter.active or context.geographic_pre_rasterized,
                            "required": artifact_filter.required,
                            "reason": (
                                "pre_rasterized_mask"
                                if context.geographic_pre_rasterized
                                else artifact_filter.reason
                            ),
                            "bundle_id": artifact_filter.bundle_id,
                            "manifest_path": (
                                str(artifact_filter.manifest_path)
                                if artifact_filter.manifest_path is not None
                                else None
                            ),
                            "removed_pixel_count": removed_count,
                            "feature_pixel_count": int(feature_mask.sum()),
                            "intersects_grid": bool(feature_mask.any()),
                            "context_source": context.geographic_context_source,
                            "ancillary_sources": [dict(source) for source in artifact_filter.ancillary_sources],
                        }
                    )
                else:
                    assert isinstance(artifact_filter, ScanlineArtifactFilter)
                    filter_records.append(
                        {
                            "filter": artifact_filter.name,
                            "removed_pixel_count": removed_count,
                            "min_length_pixels": int(artifact_filter.min_length_pixels),
                            "max_probability_std": float(artifact_filter.max_probability_std),
                        }
                    )
            removed_count = int(total_removed.sum().item())
            diagnostics.append(
                {
                    "removed_pixel_count": removed_count,
                    "removed_area_km2": float(removed_count * self.filter_pipeline.pixel_area_km2),
                    "pixel_area_km2": float(self.filter_pipeline.pixel_area_km2),
                    "filters": filter_records,
                }
            )
        return current_mask, diagnostics

    def _validate_pipeline(self) -> None:
        supported = (GeographicFeatureFilter, ScanlineArtifactFilter)
        unsupported = [item for item in self.filter_pipeline.filters if not isinstance(item, supported)]
        if unsupported:
            names = ", ".join(type(item).__name__ for item in unsupported)
            raise TypeError(f"accelerated postprocessing does not support Artifact Filter(s): {names}")

    def _geographic_filter(self) -> GeographicFeatureFilter | None:
        return next(
            (
                artifact_filter
                for artifact_filter in self.filter_pipeline.filters
                if isinstance(artifact_filter, GeographicFeatureFilter)
            ),
            None,
        )

    def _record_timing(self, name: str, elapsed: float) -> None:
        timings = self.report["timings_seconds"]
        assert isinstance(timings, dict)
        timings[name] = float(elapsed)

    def _synchronize(self) -> None:
        if self.device.type == "cuda":
            import torch

            torch.cuda.synchronize(self.device)


def aggregate_counts(records: Sequence[Mapping[str, int]]) -> dict[str, int]:
    """Sum per-sample confusion-count records."""

    total = _empty_counts()
    for record in records:
        _add_counts(total, record)
    return total


def metrics_from_counts(counts: Mapping[str, int]) -> dict[str, float]:
    """Public conversion preserving trusted segmentation metric semantics."""

    return _metrics_from_counts(counts)


def mean_connectivity(values: Sequence[float]) -> float:
    """Match the float32 mean used by the trusted connectivity metric."""

    import torch

    if not values:
        return float("nan")
    return float(torch.as_tensor(values, dtype=torch.float32).mean().item())


def _scanline_removed_mask(
    predictions: Any,
    probabilities: Any,
    *,
    min_length_pixels: int,
    max_probability_std: float,
) -> Any:
    """Vectorized contiguous-row Scanline Artifact Filter."""

    import torch
    import torch.nn.functional as F

    pred = predictions.bool()
    if pred.ndim != 4 or pred.shape[1] != 1:
        raise ValueError(f"expected [N,1,H,W] predictions, got {tuple(pred.shape)}")
    probs = probabilities.float()
    previous = F.pad(pred[..., :-1], (1, 0), value=False)
    starts = pred & ~previous
    width = int(pred.shape[-1])
    row_count = int(pred.shape[0] * pred.shape[1] * pred.shape[2])
    positions = torch.arange(width, dtype=torch.long, device=pred.device).reshape(1, 1, 1, width)
    start_positions = torch.where(starts, positions, torch.full_like(positions, -1))
    start_positions = torch.cummax(start_positions, dim=-1).values.clamp_min(0)
    row_offsets = (
        torch.arange(row_count, dtype=torch.long, device=pred.device).reshape(pred.shape[0], pred.shape[1], pred.shape[2], 1)
        * width
    )
    labels = (row_offsets + start_positions).reshape(-1)
    flat_pred = pred.reshape(-1)
    value = probs.to(torch.float64).reshape(-1)
    group_count = pred.numel()
    counts = torch.zeros(group_count, dtype=torch.float64, device=pred.device)
    sums = torch.zeros_like(counts)
    squared_sums = torch.zeros_like(counts)
    weights = flat_pred.to(torch.float64)
    counts.scatter_add_(0, labels, weights)
    sums.scatter_add_(0, labels, value * weights)
    squared_sums.scatter_add_(0, labels, value.square() * weights)
    safe_counts = counts.clamp_min(1.0)
    means = sums / safe_counts
    variances = (squared_sums / safe_counts - means.square()).clamp_min(0.0)
    stddev = torch.sqrt(variances)
    tolerance = 4.0 * torch.finfo(torch.float32).eps * max(1.0, abs(float(max_probability_std)))
    qualifying = (counts >= int(min_length_pixels)) & (stddev <= float(max_probability_std) + tolerance)
    return (flat_pred & qualifying.gather(0, labels)).reshape_as(pred)


def _soft_skeletonize(mask: Any, *, iterations: int) -> Any:
    import torch
    import torch.nn.functional as F

    if iterations < 1:
        raise ValueError("iterations must be at least 1")
    image = mask.float().clamp(0.0, 1.0)

    def erode(tensor: Any) -> Any:
        return -F.max_pool2d(-tensor, kernel_size=3, stride=1, padding=1)

    def dilate(tensor: Any) -> Any:
        return F.max_pool2d(tensor, kernel_size=3, stride=1, padding=1)

    opened = dilate(erode(image))
    skeleton = F.relu(image - opened)
    current = image
    for _ in range(iterations - 1):
        current = erode(current)
        opened = dilate(erode(current))
        delta = F.relu(current - opened)
        skeleton = skeleton + F.relu(delta - skeleton * delta)
    return skeleton.clamp(0.0, 1.0)


def _cldice_scores_with_target_skeleton(predicted_mask: Any, target_mask: Any, target_skeleton: Any) -> Any:
    import torch

    prediction = predicted_mask.float().clamp(0.0, 1.0)
    target = target_mask.float().clamp(0.0, 1.0)
    dims = tuple(range(1, prediction.ndim))
    pred_mass = prediction.sum(dim=dims)
    target_mass = target.sum(dim=dims)
    both_empty = (pred_mass <= _EPSILON) & (target_mass <= _EPSILON)
    one_empty = (pred_mass <= _EPSILON) ^ (target_mass <= _EPSILON)
    pred_skeleton = _soft_skeletonize(prediction, iterations=32)
    topology_precision = (pred_skeleton * target).sum(dim=dims) / (pred_skeleton.sum(dim=dims) + _EPSILON)
    topology_sensitivity = (target_skeleton * prediction).sum(dim=dims) / (
        target_skeleton.sum(dim=dims) + _EPSILON
    )
    score = (2.0 * topology_precision * topology_sensitivity) / (
        topology_precision + topology_sensitivity + _EPSILON
    )
    score = torch.where(both_empty, torch.ones_like(score), score)
    return torch.where(one_empty, torch.zeros_like(score), score)


def _confusion_counts_by_sample(predictions: Any, targets: Any) -> tuple[dict[str, int], ...]:
    pred = predictions.bool()
    target = targets.bool()
    if pred.shape != target.shape:
        raise ValueError(f"prediction and target shapes differ: {tuple(pred.shape)} != {tuple(target.shape)}")
    dims = tuple(range(1, pred.ndim))
    positive = target.sum(dim=dims)
    predicted_positive = pred.sum(dim=dims)
    true_positive = (pred & target).sum(dim=dims)
    false_positive = (pred & ~target).sum(dim=dims)
    false_negative = (~pred & target).sum(dim=dims)
    rows: list[dict[str, int]] = []
    for index in range(int(pred.shape[0])):
        rows.append(
            {
                "positive_pixel_count": int(positive[index].item()),
                "predicted_positive_pixel_count": int(predicted_positive[index].item()),
                "true_positive_pixels": int(true_positive[index].item()),
                "false_positive_pixels": int(false_positive[index].item()),
                "false_negative_pixels": int(false_negative[index].item()),
            }
        )
    return tuple(rows)


def _confusion_counts_by_threshold(predictions: Any, targets: Any) -> tuple[dict[str, int], ...]:
    pred = predictions.bool()
    target = targets.bool()
    dims = tuple(range(1, pred.ndim))
    positive = target.sum(dim=dims)
    predicted_positive = pred.sum(dim=dims)
    true_positive = (pred & target).sum(dim=dims)
    false_positive = (pred & ~target).sum(dim=dims)
    false_negative = (~pred & target).sum(dim=dims)
    return tuple(
        {
            "positive_pixel_count": int(positive[index].item()),
            "predicted_positive_pixel_count": int(predicted_positive[index].item()),
            "true_positive_pixels": int(true_positive[index].item()),
            "false_positive_pixels": int(false_positive[index].item()),
            "false_negative_pixels": int(false_negative[index].item()),
        }
        for index in range(int(pred.shape[0]))
    )


def _metrics_from_counts(counts: Mapping[str, int]) -> dict[str, float]:
    true_positive = int(counts["true_positive_pixels"])
    false_positive = int(counts["false_positive_pixels"])
    false_negative = int(counts["false_negative_pixels"])
    return {
        "dice": float((2 * true_positive + _EPSILON) / (2 * true_positive + false_positive + false_negative + _EPSILON)),
        "iou": float((true_positive + _EPSILON) / (true_positive + false_positive + false_negative + _EPSILON)),
        "precision": float((true_positive + _EPSILON) / (true_positive + false_positive + _EPSILON)),
        "recall": float((true_positive + _EPSILON) / (true_positive + false_negative + _EPSILON)),
    }


def _empty_counts() -> dict[str, int]:
    return {
        "positive_pixel_count": 0,
        "predicted_positive_pixel_count": 0,
        "true_positive_pixels": 0,
        "false_positive_pixels": 0,
        "false_negative_pixels": 0,
    }


def _add_counts(total: dict[str, int], values: Mapping[str, int]) -> None:
    for key in total:
        total[key] += int(values[key])


def _batch_ranges(sample_count: int, batch_size: int) -> Sequence[tuple[int, int]]:
    return tuple((start, min(sample_count, start + batch_size)) for start in range(0, sample_count, batch_size))


def _filter_context(dataset: object, index: int) -> dict[str, object]:
    getter = getattr(dataset, "filter_context", None)
    return dict(getter(index)) if callable(getter) else {}


def _prepare_georeferencing(
    context: Mapping[str, object],
    shape: tuple[int, int],
) -> Mapping[str, object] | None:
    lon = context.get("longitude")
    lat = context.get("latitude")
    if lon is None or lat is None:
        return None
    lon_grid = np.asarray(lon, dtype=np.float64)
    lat_grid = np.asarray(lat, dtype=np.float64)
    height, width = shape
    min_lon = float(np.nanmin(lon_grid))
    max_lon = float(np.nanmax(lon_grid))
    min_lat = float(np.nanmin(lat_grid))
    max_lat = float(np.nanmax(lat_grid))
    pixel_width = abs(max_lon - min_lon) / max(1, width - 1)
    pixel_height = abs(max_lat - min_lat) / max(1, height - 1)
    tiepoint_x = min_lon - pixel_width / 2.0
    tiepoint_y = max_lat + pixel_height / 2.0
    return {
        "pixel_scale": (pixel_width, pixel_height, 0.0),
        "tiepoint": (0.0, 0.0, 0.0, tiepoint_x, tiepoint_y, 0.0),
        "epsg": 4326,
        "metadata": {
            "crs": "EPSG:4326",
            "model": "regular_lon_lat_from_provider_longitude_latitude_context",
            "bbox": [tiepoint_x, min_lat - pixel_height / 2.0, max_lon + pixel_width / 2.0, tiepoint_y],
            "pixel_size": [pixel_width, pixel_height],
        },
    }


def _emit_periodic_progress(
    emit: Callable[[str], None],
    *,
    phase: str,
    completed: int,
    total: int,
    started_at: float,
    log_every: int,
) -> None:
    if completed != total and completed % log_every != 0:
        return
    elapsed = max(0.0, time.monotonic() - started_at)
    rate = completed / elapsed if elapsed > 0 else 0.0
    remaining = max(0, total - completed)
    eta = remaining / rate if rate > 0 else 0.0
    percent = 100.0 if total <= 0 else 100.0 * completed / total
    emit(
        f"{phase}: {completed}/{total} ({percent:.1f}%); "
        f"elapsed={elapsed:.1f}s rate={rate:.2f} samples/s eta={eta:.1f}s"
    )


__all__ = [
    "BoundedBatchPostprocessor",
    "OperationalPostprocessingResult",
    "PreparedFilterContext",
    "aggregate_counts",
    "mean_connectivity",
    "metrics_from_counts",
]
