"""ABI provider-owned Post-Run Evaluation adapter with Artifact Filters."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from abi_contrail.adapters import ABITrainingAdapter
from abi_contrail.artifact_filters import ABIArtifactFilterPipeline, build_default_artifact_filter_pipeline
from abi_contrail.baseline_segmenters import MCAST_BASELINE_METADATA, MCASTBaselineSegmenter, configured_mcast_baseline_assets

EVALUATION_MODE_WHOLE_VALIDATION_FAILURE_ANALYSIS = "whole_validation_failure_analysis"


@dataclass(frozen=True)
class AcceptanceGateConfig:
    """Configurable thresholds for provider-owned acceptance-gate reports."""

    primary_metric: str = "filtered/dice"
    filtered_recall_tolerance: float = 0.05
    contrail_connectivity_metric: str = "filtered/contrail_connectivity"
    dataset_sources: tuple[str, ...] = ("mit", "google")
    source_failure_metric_name: str = "filtered/dice"
    source_failure_relative_drop: float = 0.50
    source_failure_absolute_floor: float = 0.10
    artifact_filter_removed_fraction_limit: float = 0.50
    artifact_filter_improvement_limit: float = 0.20


def build_acceptance_gate_report(
    *,
    candidate_metrics: Mapping[str, object],
    baseline_metrics: Mapping[str, Mapping[str, object]] | Sequence[Mapping[str, object]],
    candidate_run_id: str | None = None,
    config: AcceptanceGateConfig | None = None,
) -> dict[str, object]:
    """Build a human-reviewed ABI acceptance-gate report.

    The report consumes trusted evaluation artifacts (aggregate candidate and
    Baseline Segmenter metrics).  It does not execute candidate code and it does
    not make an automatic promotion decision; final promotion remains a human
    judgment informed by the gate flags.
    """

    gate_config = config or AcceptanceGateConfig()
    baselines = _normalise_baseline_metrics(baseline_metrics)
    if not baselines:
        raise ValueError("at least one Baseline Segmenter metric record is required")
    best_name, best_metrics = max(
        baselines,
        key=lambda item: _required_float(item[1], gate_config.primary_metric, f"baseline {item[0]!r}"),
    )

    candidate_primary = _required_float(candidate_metrics, gate_config.primary_metric, "candidate")
    baseline_primary = _required_float(best_metrics, gate_config.primary_metric, f"baseline {best_name!r}")
    aggregate_comparison = {
        "metric": gate_config.primary_metric,
        "candidate": candidate_primary,
        "baseline": baseline_primary,
        "delta": candidate_primary - baseline_primary,
        "candidate_beats_baseline": candidate_primary >= baseline_primary,
    }

    flags: list[dict[str, object]] = []
    if candidate_primary < baseline_primary:
        flags.append(
            {
                "id": "aggregate_below_best_baseline",
                "severity": "fail",
                "message": f"candidate {gate_config.primary_metric} is below the best available Baseline Segmenter",
                "candidate": candidate_primary,
                "baseline": baseline_primary,
            }
        )

    recall_regression = _recall_regression(candidate_metrics, best_metrics, gate_config)
    if recall_regression["flagged"]:
        flags.append(
            {
                "id": "filtered_recall_regression",
                "severity": "fail",
                "message": "candidate filtered recall regressed beyond configured tolerance",
                **recall_regression,
            }
        )

    connectivity = _metric_comparison(
        candidate_metrics,
        best_metrics,
        gate_config.contrail_connectivity_metric,
        required=True,
    )
    if connectivity["delta"] < 0:
        flags.append(
            {
                "id": "contrail_connectivity_regression",
                "severity": "warning",
                "message": "candidate Contrail Connectivity Metric is below the best baseline",
                **connectivity,
            }
        )

    source_failures = _dataset_source_failures(candidate_metrics, best_metrics, gate_config)
    for failure in source_failures:
        flags.append(
            {
                "id": "dataset_source_catastrophic_failure",
                "severity": failure["severity"],
                "message": f"candidate has a Dataset Source-specific catastrophic failure on {failure['source']}",
                **failure,
            }
        )

    artifact_dependence = _artifact_filter_dependence(candidate_metrics, gate_config)
    if artifact_dependence["flagged"]:
        flags.append(
            {
                "id": "excessive_artifact_filter_dependence",
                "severity": "warning",
                "message": "candidate appears excessively dependent on provider Artifact Filters",
                **artifact_dependence,
            }
        )

    overall_status = "gate_flags_present" if flags else "ready_for_human_review"
    return {
        "report_type": "abi_acceptance_gate_report",
        "candidate_run_id": candidate_run_id,
        "best_baseline": {
            "name": best_name,
            "selection_metric": gate_config.primary_metric,
            "selection_value": baseline_primary,
        },
        "aggregate_comparison": aggregate_comparison,
        "recall_regression": recall_regression,
        "contrail_connectivity_comparison": connectivity,
        "dataset_source_failures": source_failures,
        "artifact_filter_dependence": artifact_dependence,
        "flags": flags,
        "overall_status": overall_status,
        "promotion_decision": "human_review_required",
        "human_review_required": True,
        "human_review_note": "This report is an acceptance-gate input only; final candidate promotion remains a human-reviewed decision.",
    }


class ABIEvaluationAdapter:
    """Trusted ABI evaluation adapter invoked by the harness evaluation dispatch."""

    def __init__(self, *, training_adapter: ABITrainingAdapter | None = None, filter_pipeline: ABIArtifactFilterPipeline | None = None) -> None:
        self.training_adapter = training_adapter or ABITrainingAdapter()
        self.filter_pipeline = filter_pipeline or build_default_artifact_filter_pipeline()

    def run_evaluation_mode(
        self,
        *,
        mode: str,
        run_dir: Path,
        data_root: Path,
        model_artifact_path: Path,
        threshold: float,
        evaluation_dir: Path,
        max_artifact_samples: int,
    ) -> tuple[dict[str, float], list[dict[str, object]], dict[str, object], dict[str, object]]:
        if mode != EVALUATION_MODE_WHOLE_VALIDATION_FAILURE_ANALYSIS:
            raise ValueError(f"unsupported ABI evaluation mode: {mode}")
        return self._evaluate_validation_split(
            run_dir=run_dir,
            data_root=data_root,
            model_artifact_path=model_artifact_path,
            threshold=threshold,
            evaluation_dir=evaluation_dir,
            max_artifact_samples=max_artifact_samples,
        )

    def baseline_segmenters(self, data_config: Mapping[str, object] | None = None) -> tuple[dict[str, object], ...]:
        """Return provider-owned Baseline Segmenter declarations.

        Asset paths are intentionally runtime configuration, not candidate-owned
        code.  Configure ``mcast_detection_1_1_path`` and/or
        ``mcast_detection_2_1_path`` in the provider data config on the machine
        that will run the baseline evaluations.
        """

        configured_assets = configured_mcast_baseline_assets(data_config or {})
        declarations: list[dict[str, object]] = []
        for name, metadata in MCAST_BASELINE_METADATA.items():
            declaration = {
                "name": metadata.name,
                "version": metadata.version,
                "asset_config_key": metadata.asset_config_key,
                "expected_asset": metadata.expected_asset,
                "output": metadata.output,
                "artifact_filters": "provider_owned_same_pipeline_as_candidates",
                "configured": name in configured_assets,
            }
            if name in configured_assets:
                declaration["asset_path"] = str(configured_assets[name])
            declarations.append(declaration)
        return tuple(declarations)

    def run_baseline_validation_evaluation(
        self,
        *,
        baseline_name: str,
        data_config: Mapping[str, object],
        data_root: Path | None = None,
        threshold: float | None = None,
        device: str | Any = "cpu",
        model_factory: Any | None = None,
        evaluation_dir: Path | None = None,
    ) -> tuple[dict[str, float], list[dict[str, object]], dict[str, object], dict[str, object]]:
        """Evaluate one configured baseline through the same raw/filtered path.

        This method is the provider-owned execution hook for the GPU server.
        It does not run candidate code and does not invoke MCAST operational
        postprocessing.
        """

        import torch

        merged_config = dict(data_config)
        if data_root is not None:
            merged_config["dataset_root"] = str(data_root)
        assets = configured_mcast_baseline_assets(merged_config)
        try:
            asset_path = assets[baseline_name]
        except KeyError as exc:
            metadata = MCAST_BASELINE_METADATA.get(baseline_name)
            key = metadata.asset_config_key if metadata is not None else "<unknown>"
            raise ValueError(f"missing asset path for baseline {baseline_name!r}; set data_config.{key}") from exc
        data_config_for_dataset = {key: value for key, value in merged_config.items() if key not in {m.asset_config_key for m in MCAST_BASELINE_METADATA.values()}}
        dataset = self.training_adapter.build_evaluation_dataset(data_config=data_config_for_dataset, resolved_manifest_path=Path("__abi_baseline_default_manifest__.yaml"))
        baseline = MCASTBaselineSegmenter.load(baseline_name, asset_path, device=device, model_factory=model_factory)
        probabilities_all: list[torch.Tensor] = []
        targets_all: list[torch.Tensor] = []
        with torch.no_grad():
            for index in range(len(dataset)):
                inputs, target = dataset[index]
                source = _baseline_source(dataset, index, inputs)
                result = baseline.predict_patch(source, threshold=threshold, device=device)
                probabilities_all.append(result.probabilities.detach().cpu())
                targets_all.append(target.detach().cpu())
        probabilities = torch.stack(probabilities_all)
        targets = torch.stack(targets_all)
        cutoff = float(threshold if threshold is not None else baseline.threshold)
        result = _evaluate_probability_tensor(
            dataset=dataset,
            probabilities=probabilities,
            targets=targets,
            threshold=cutoff,
            filter_pipeline=build_default_artifact_filter_pipeline(data_config_for_dataset),
            model_record={"baseline/name": baseline.name, "baseline/version": baseline.version},
        )
        if evaluation_dir is not None:
            _write_baseline_evaluation_artifacts(
                evaluation_dir=evaluation_dir,
                baseline_name=baseline.name,
                baseline_version=baseline.version,
                asset_path=asset_path,
                threshold=cutoff,
                result=result,
            )
        return result

    def display_prediction_sample_input(self, inputs: Any) -> Any:
        return self.training_adapter.display_prediction_sample_input(inputs)

    def build_acceptance_gate_report(
        self,
        *,
        candidate_metrics: Mapping[str, object],
        baseline_metrics: Mapping[str, Mapping[str, object]] | Sequence[Mapping[str, object]],
        candidate_run_id: str | None = None,
        config: AcceptanceGateConfig | None = None,
        output_path: Path | None = None,
    ) -> dict[str, object]:
        """Build and optionally persist the provider-owned acceptance report."""

        report = build_acceptance_gate_report(
            candidate_metrics=candidate_metrics,
            baseline_metrics=baseline_metrics,
            candidate_run_id=candidate_run_id,
            config=config,
        )
        if output_path is not None:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        return report

    def _evaluate_validation_split(
        self,
        *,
        run_dir: Path,
        data_root: Path,
        model_artifact_path: Path,
        threshold: float,
        evaluation_dir: Path,
        max_artifact_samples: int,
    ) -> tuple[dict[str, float], list[dict[str, object]], dict[str, object], dict[str, object]]:
        del evaluation_dir, max_artifact_samples
        import torch
        import yaml
        from ml_autoresearch.smoke import _extract_mask_logits, _import_candidate_model, input_spec_from_resolved_manifest, output_spec_from_resolved_manifest

        manifest_path = run_dir / "resolved_manifest.yaml"
        manifest = yaml.safe_load(manifest_path.read_text()) or {}
        batch_size = int(manifest.get("training", {}).get("batch_size", 1))
        input_spec = input_spec_from_resolved_manifest(manifest_path)
        output_spec = output_spec_from_resolved_manifest(manifest_path)
        data_config = _evaluation_data_config(run_dir, data_root)
        filter_pipeline = build_default_artifact_filter_pipeline(data_config)
        dataset = self.training_adapter.build_evaluation_dataset(data_config=data_config, resolved_manifest_path=manifest_path)

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        module = _import_candidate_model(run_dir / "candidate")
        model = module.build_model(dict(input_spec), dict(output_spec))
        if not isinstance(model, torch.nn.Module):
            raise RuntimeError("build_model must return a torch.nn.Module")
        checkpoint = torch.load(model_artifact_path, map_location=device, weights_only=True)
        state_dict = checkpoint.get("model_state_dict") if isinstance(checkpoint, dict) else None
        if not isinstance(state_dict, dict):
            raise RuntimeError(f"model artifact is unreadable: missing model_state_dict in {model_artifact_path}")
        model.load_state_dict(state_dict)
        model = model.to(device)
        model.eval()

        probabilities_all: list[torch.Tensor] = []
        targets_all: list[torch.Tensor] = []
        with torch.no_grad():
            for start in range(0, len(dataset), batch_size):
                batch_indices = list(range(start, min(start + batch_size, len(dataset))))
                inputs = torch.stack([dataset[index][0] for index in batch_indices]).to(device)
                targets = torch.stack([dataset[index][1] for index in batch_indices]).to(device)
                logits = _extract_mask_logits(model(inputs), output_spec)[0]
                probabilities_all.extend(probability.detach().cpu() for probability in torch.sigmoid(logits))
                targets_all.extend(target.detach().cpu() for target in targets)

        return _evaluate_probability_tensor(
            dataset=dataset,
            probabilities=torch.stack(probabilities_all),
            targets=torch.stack(targets_all),
            threshold=threshold,
            filter_pipeline=filter_pipeline,
        )


def _evaluate_probability_tensor(
    *,
    dataset: object,
    probabilities: Any,
    targets: Any,
    threshold: float,
    filter_pipeline: ABIArtifactFilterPipeline,
    model_record: Mapping[str, object] | None = None,
) -> tuple[dict[str, float], list[dict[str, object]], dict[str, object], dict[str, object]]:
    import torch
    from ml_autoresearch.problem_support.segmentation import binary_confusion_counts, binary_segmentation_metrics, contrail_connectivity_metric

    probabilities = probabilities.detach().cpu()
    targets = targets.detach().cpu()
    predictions = probabilities >= threshold
    target_masks = targets >= 0.5
    raw_predictions: list[torch.Tensor] = []
    filtered_predictions: list[torch.Tensor] = []
    targets_all: list[torch.Tensor] = []
    probabilities_all: list[torch.Tensor] = []
    per_sample_records: list[dict[str, object]] = []
    sample_sources: list[str | None] = []
    removed_pixels_total = 0
    removed_area_total = 0.0
    for index in range(predictions.shape[0]):
        probability = probabilities[index].numpy()
        prediction = predictions[index].numpy()
        context = _filter_context(dataset, index)
        filtered = filter_pipeline.apply(prediction, probability, context=context)
        filtered_prediction = torch.from_numpy(filtered.filtered_mask.astype(bool))
        sample_prediction = predictions[index : index + 1]
        sample_filtered_prediction = filtered_prediction.unsqueeze(0)
        sample_target = target_masks[index : index + 1]
        raw_metrics = binary_segmentation_metrics(sample_prediction, sample_target)
        filtered_metrics = binary_segmentation_metrics(sample_filtered_prediction, sample_target)
        raw_connectivity = contrail_connectivity_metric(sample_prediction, sample_target)
        filtered_connectivity = contrail_connectivity_metric(sample_filtered_prediction, sample_target)
        diagnostics = filtered.diagnostics
        removed_count = int(diagnostics["removed_pixel_count"])
        removed_area = float(diagnostics["removed_area_km2"])
        removed_pixels_total += removed_count
        removed_area_total += removed_area
        record = {
            "sample_id": f"val/{index:06d}",
            "dataset_index": int(index),
            **{f"raw/{key}": value for key, value in raw_metrics.items()},
            "raw/cldice": raw_connectivity,
            "raw/contrail_connectivity": raw_connectivity,
            **{f"filtered/{key}": value for key, value in filtered_metrics.items()},
            "filtered/cldice": filtered_connectivity,
            "filtered/contrail_connectivity": filtered_connectivity,
            **{f"raw/{key}": value for key, value in binary_confusion_counts(sample_prediction, sample_target).items()},
            **{f"filtered/{key}": value for key, value in binary_confusion_counts(sample_filtered_prediction, sample_target).items()},
            "artifact_filters/removed_pixel_count": removed_count,
            "artifact_filters/removed_area_km2": removed_area,
            "artifact_filters/diagnostics": diagnostics,
        }
        if model_record:
            record.update(model_record)
        metadata = _sample_metadata(dataset, index)
        record.update(metadata)
        sample_sources.append(_dataset_source_from_metadata(metadata))
        per_sample_records.append(record)
        raw_predictions.append(sample_prediction)
        filtered_predictions.append(sample_filtered_prediction)
        probabilities_all.append(probabilities[index : index + 1])
        targets_all.append(sample_target)

    raw_tensor = torch.cat(raw_predictions)
    filtered_tensor = torch.cat(filtered_predictions)
    target_tensor = torch.cat(targets_all)
    raw_aggregate = binary_segmentation_metrics(raw_tensor, target_tensor)
    filtered_aggregate = binary_segmentation_metrics(filtered_tensor, target_tensor)
    raw_connectivity = contrail_connectivity_metric(raw_tensor, target_tensor)
    filtered_connectivity = contrail_connectivity_metric(filtered_tensor, target_tensor)
    aggregate = {
        **{f"raw/{key}": value for key, value in raw_aggregate.items()},
        "raw/cldice": raw_connectivity,
        "raw/contrail_connectivity": raw_connectivity,
        **{f"raw/{key}": float(value) for key, value in binary_confusion_counts(raw_tensor, target_tensor).items()},
        **{f"filtered/{key}": value for key, value in filtered_aggregate.items()},
        "filtered/cldice": filtered_connectivity,
        "filtered/contrail_connectivity": filtered_connectivity,
        **{f"filtered/{key}": float(value) for key, value in binary_confusion_counts(filtered_tensor, target_tensor).items()},
        "artifact_filters/removed_pixel_count": float(removed_pixels_total),
        "artifact_filters/removed_area_km2": float(removed_area_total),
    }
    for source in ("mit", "google"):
        indices = [index for index, sample_source in enumerate(sample_sources) if sample_source == source]
        if not indices:
            continue
        source_index = torch.as_tensor(indices, dtype=torch.long)
        source_raw = raw_tensor.index_select(0, source_index)
        source_filtered = filtered_tensor.index_select(0, source_index)
        source_target = target_tensor.index_select(0, source_index)
        source_raw_metrics = binary_segmentation_metrics(source_raw, source_target)
        source_filtered_metrics = binary_segmentation_metrics(source_filtered, source_target)
        source_raw_connectivity = contrail_connectivity_metric(source_raw, source_target)
        source_filtered_connectivity = contrail_connectivity_metric(source_filtered, source_target)
        aggregate.update(
            {
                **{f"source/{source}/raw/{key}": value for key, value in source_raw_metrics.items()},
                f"source/{source}/raw/cldice": source_raw_connectivity,
                f"source/{source}/raw/contrail_connectivity": source_raw_connectivity,
                **{f"source/{source}/filtered/{key}": value for key, value in source_filtered_metrics.items()},
                f"source/{source}/filtered/cldice": source_filtered_connectivity,
                f"source/{source}/filtered/contrail_connectivity": source_filtered_connectivity,
            }
        )
    threshold_sweep = {"default_threshold": float(threshold), "note": "ABI filtered evaluation records threshold-specific raw and filtered metrics."}
    diagnostic_manifest = {"samples": [], "note": "ABI v0 filtered evaluation does not yet emit qualitative diagnostic images."}
    return aggregate, per_sample_records, threshold_sweep, diagnostic_manifest


def _normalise_baseline_metrics(
    baseline_metrics: Mapping[str, Mapping[str, object]] | Sequence[Mapping[str, object]],
) -> list[tuple[str, Mapping[str, object]]]:
    if isinstance(baseline_metrics, Mapping):
        return [(str(name), metrics) for name, metrics in baseline_metrics.items()]
    normalised: list[tuple[str, Mapping[str, object]]] = []
    for index, metrics in enumerate(baseline_metrics):
        name = metrics.get("baseline/name", metrics.get("name", f"baseline_{index}"))
        normalised.append((str(name), metrics))
    return normalised


def _required_float(metrics: Mapping[str, object], key: str, owner: str) -> float:
    value = metrics.get(key)
    if value is None:
        raise ValueError(f"missing required {owner} metric {key!r}")
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{owner} metric {key!r} is not numeric: {value!r}") from exc


def _optional_float(metrics: Mapping[str, object], key: str) -> float | None:
    value = metrics.get(key)
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _metric_comparison(
    candidate_metrics: Mapping[str, object],
    baseline_metrics: Mapping[str, object],
    metric: str,
    *,
    required: bool,
) -> dict[str, object]:
    candidate = _required_float(candidate_metrics, metric, "candidate") if required else _optional_float(candidate_metrics, metric)
    baseline = _required_float(baseline_metrics, metric, "baseline") if required else _optional_float(baseline_metrics, metric)
    delta = None if candidate is None or baseline is None else candidate - baseline
    return {"metric": metric, "candidate": candidate, "baseline": baseline, "delta": delta}


def _recall_regression(
    candidate_metrics: Mapping[str, object],
    baseline_metrics: Mapping[str, object],
    config: AcceptanceGateConfig,
) -> dict[str, object]:
    comparison = _metric_comparison(candidate_metrics, baseline_metrics, "filtered/recall", required=True)
    candidate = float(comparison["candidate"])
    baseline = float(comparison["baseline"])
    tolerance = float(config.filtered_recall_tolerance)
    return {
        **comparison,
        "tolerance": tolerance,
        "allowed_floor": baseline - tolerance,
        "flagged": candidate < baseline - tolerance,
    }


def _dataset_source_failures(
    candidate_metrics: Mapping[str, object],
    baseline_metrics: Mapping[str, object],
    config: AcceptanceGateConfig,
) -> list[dict[str, object]]:
    failures: list[dict[str, object]] = []
    for source in config.dataset_sources:
        metric = f"source/{source}/{config.source_failure_metric_name}"
        candidate = _optional_float(candidate_metrics, metric)
        baseline = _optional_float(baseline_metrics, metric)
        if candidate is None or baseline is None:
            continue
        relative_floor = baseline * (1.0 - config.source_failure_relative_drop)
        absolute_floor = float(config.source_failure_absolute_floor)
        if candidate < absolute_floor or candidate < relative_floor:
            failures.append(
                {
                    "source": source,
                    "metric": metric,
                    "candidate": candidate,
                    "baseline": baseline,
                    "relative_floor": relative_floor,
                    "absolute_floor": absolute_floor,
                    "severity": "fail",
                }
            )
    return failures


def _artifact_filter_dependence(candidate_metrics: Mapping[str, object], config: AcceptanceGateConfig) -> dict[str, object]:
    removed_pixels = _optional_float(candidate_metrics, "artifact_filters/removed_pixel_count")
    raw_predicted_pixels = _optional_float(candidate_metrics, "raw/predicted_positive_pixel_count")
    removed_fraction = None
    if removed_pixels is not None and raw_predicted_pixels is not None and raw_predicted_pixels > 0:
        removed_fraction = removed_pixels / raw_predicted_pixels

    raw_metric = config.primary_metric.replace("filtered/", "raw/", 1)
    raw_primary = _optional_float(candidate_metrics, raw_metric)
    filtered_primary = _optional_float(candidate_metrics, config.primary_metric)
    filtered_minus_raw = None
    if raw_primary is not None and filtered_primary is not None:
        filtered_minus_raw = filtered_primary - raw_primary

    reasons: list[str] = []
    if removed_fraction is not None and removed_fraction > config.artifact_filter_removed_fraction_limit:
        reasons.append("removed_fraction_exceeds_limit")
    if filtered_minus_raw is not None and filtered_minus_raw > config.artifact_filter_improvement_limit:
        reasons.append("filtered_metric_improvement_exceeds_limit")

    return {
        "flagged": bool(reasons),
        "reasons": reasons,
        "removed_pixels": removed_pixels,
        "raw_predicted_positive_pixels": raw_predicted_pixels,
        "removed_fraction": removed_fraction,
        "removed_fraction_limit": float(config.artifact_filter_removed_fraction_limit),
        "raw_metric": raw_metric,
        "raw_primary": raw_primary,
        "filtered_primary": filtered_primary,
        "filtered_minus_raw_primary": filtered_minus_raw,
        "filtered_minus_raw_limit": float(config.artifact_filter_improvement_limit),
    }


def _write_baseline_evaluation_artifacts(
    *,
    evaluation_dir: Path,
    baseline_name: str,
    baseline_version: str,
    asset_path: Path,
    threshold: float,
    result: tuple[dict[str, float], list[dict[str, object]], dict[str, object], dict[str, object]],
) -> None:
    aggregate, per_sample_records, threshold_sweep, diagnostic_manifest = result
    evaluation_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "baseline": {"name": baseline_name, "version": baseline_version, "asset_path": str(asset_path)},
        "threshold": float(threshold),
        "sample_count": len(per_sample_records),
        "metrics": aggregate,
    }
    (evaluation_dir / "aggregate_metrics.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    with (evaluation_dir / "per_sample_metrics.jsonl").open("w") as handle:
        for record in per_sample_records:
            handle.write(json.dumps(record, sort_keys=True) + "\n")
    (evaluation_dir / "threshold_sweep.json").write_text(json.dumps(threshold_sweep, indent=2, sort_keys=True) + "\n")
    diagnostics_dir = evaluation_dir / "diagnostic_samples"
    diagnostics_dir.mkdir(parents=True, exist_ok=True)
    (diagnostics_dir / "samples.json").write_text(json.dumps(diagnostic_manifest, indent=2, sort_keys=True) + "\n")
    (evaluation_dir / "baseline_evaluation_metadata.json").write_text(
        json.dumps(
            {
                "status": "completed",
                "baseline": {"name": baseline_name, "version": baseline_version, "asset_path": str(asset_path)},
                "artifacts": {
                    "aggregate_metrics": "aggregate_metrics.json",
                    "per_sample_metrics": "per_sample_metrics.jsonl",
                    "threshold_sweep": "threshold_sweep.json",
                    "diagnostic_samples": "diagnostic_samples/samples.json",
                },
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


def _evaluation_data_config(run_dir: Path, data_root: Path) -> dict[str, object]:
    metadata_path = run_dir / "run_metadata.json"
    if not metadata_path.is_file():
        return {"dataset_root": str(data_root)}
    metadata = json.loads(metadata_path.read_text())
    dataset = metadata.get("dataset")
    if not isinstance(dataset, Mapping):
        return {"dataset_root": str(data_root)}
    config = {
        key: value
        for key, value in dataset.items()
        if key
        in {
            "layout",
            "inputs_zarr",
            "labels_zarr",
            "metadata_rows",
            "scene_names",
            "goes_times",
            "val_fraction",
            "split_seed",
            "patch_size",
            "stride",
            "coastline_geojson",
            "rivers_geojson",
            "geographic_filter_pixel_buffer",
            "scanline_min_length_pixels",
            "scanline_max_probability_std",
            "pixel_area_km2",
        }
    }
    config["dataset_root"] = str(data_root)
    return config


def _baseline_source(dataset: object, index: int, fallback_inputs: Any) -> Any:
    getter = getattr(dataset, "raw_inputs", None)
    if callable(getter):
        return getter(index)
    return fallback_inputs


def _filter_context(dataset: object, index: int) -> dict[str, object]:
    getter = getattr(dataset, "filter_context", None)
    if callable(getter):
        return dict(getter(index))
    return {}


def _sample_metadata(dataset: object, index: int) -> dict[str, object]:
    getter = getattr(dataset, "sample_metadata", None)
    if not callable(getter):
        return {}
    metadata = dict(getter(index))
    record = {f"sample/{key}": value for key, value in metadata.items()}
    if "dataset_source" in metadata:
        record["Dataset Source"] = metadata["dataset_source"]
    for key in ("scene_name", "scene_index", "goes_time", "row", "col"):
        if key in metadata:
            record[key] = metadata[key]
    return record


def _dataset_source_from_metadata(metadata: Mapping[str, object]) -> str | None:
    value = metadata.get("sample/dataset_source", metadata.get("Dataset Source"))
    if value is None:
        return None
    source = str(value).lower()
    return source if source in {"mit", "google"} else None


__all__ = [
    "ABIEvaluationAdapter",
    "AcceptanceGateConfig",
    "EVALUATION_MODE_WHOLE_VALIDATION_FAILURE_ANALYSIS",
    "build_acceptance_gate_report",
]
