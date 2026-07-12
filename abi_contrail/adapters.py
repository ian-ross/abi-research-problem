"""Trusted adapters and ResearchProblemSpec declaration for GOES ABI Contrail Segmentation.

The provider spec is declarative, while this module also hosts the trusted
vertical-slice training adapter used by ml-autoresearch. Candidate code still
cannot own data loading, losses, metrics, or sampling policy boundaries.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from abi_contrail.datasets import (
    ABI_FORBIDDEN_SOURCE_INDICES,
    ABI_INPUT_MODE_SOURCE_INDICES,
    ABIPatchDataset,
    ABIPatchIndexRecord,
    INPUT_MODE_ABI_16CH,
    INPUT_MODE_ABI_16CH_PLUS_SZA,
    INPUT_MODE_ABI_THERMAL_10CH,
    build_google_abi_patch_index,
    build_mit_abi_patch_index,
    open_abi_patch_arrays,
)


RESEARCH_PROBLEM_ID = "goes_abi_contrail_segmentation"
RESEARCH_PROBLEM_VERSION = "v0"
CONTRACT_VERSION = "v0"
OUTPUT_FORM_MASK_LOGITS = "mask_logits"
AUXILIARY_TARGET_LINE = "line"
AUXILIARY_TARGET_BOUNDARY = "boundary"
AUXILIARY_TARGET_CENTERLINE = "centerline"
AUXILIARY_OUTPUT_LINE_LOGITS = "line_logits"
AUXILIARY_OUTPUT_BOUNDARY_LOGITS = "boundary_logits"
AUXILIARY_OUTPUT_CENTERLINE_LOGITS = "centerline_logits"
AUXILIARY_LOSS_WEIGHTED_BCE = "weighted_bce"
INPUT_MODE_ABI_INPUTS = (INPUT_MODE_ABI_16CH, INPUT_MODE_ABI_16CH_PLUS_SZA, INPUT_MODE_ABI_THERMAL_10CH)
AUXILIARY_TARGETS = (AUXILIARY_TARGET_LINE, AUXILIARY_TARGET_BOUNDARY, AUXILIARY_TARGET_CENTERLINE)
AUXILIARY_OUTPUTS = {
    AUXILIARY_TARGET_LINE: AUXILIARY_OUTPUT_LINE_LOGITS,
    AUXILIARY_TARGET_BOUNDARY: AUXILIARY_OUTPUT_BOUNDARY_LOGITS,
    AUXILIARY_TARGET_CENTERLINE: AUXILIARY_OUTPUT_CENTERLINE_LOGITS,
}
AUXILIARY_OUTPUT_SHAPES = {target: [1, 256, 256] for target in AUXILIARY_TARGETS}
SAMPLING_POLICY_SEED = 20260531
SAMPLING_POLICY_SEQUENTIAL = "sequential"
SAMPLING_POLICY_DETERMINISTIC_SHUFFLE = "deterministic_shuffle"
SAMPLING_POLICY_MIT_ONLY = "mit_only"
SAMPLING_POLICY_GOOGLE_ONLY = "google_only"
SAMPLING_POLICY_COMBINED_SOURCE_BALANCED = "combined_source_balanced"
ABI_SAMPLING_POLICIES = (
    SAMPLING_POLICY_SEQUENTIAL,
    SAMPLING_POLICY_DETERMINISTIC_SHUFFLE,
    SAMPLING_POLICY_MIT_ONLY,
    SAMPLING_POLICY_GOOGLE_ONLY,
    SAMPLING_POLICY_COMBINED_SOURCE_BALANCED,
)
SOURCE_BALANCED_SAMPLING_POLICIES = {
    SAMPLING_POLICY_MIT_ONLY,
    SAMPLING_POLICY_GOOGLE_ONLY,
    SAMPLING_POLICY_COMBINED_SOURCE_BALANCED,
}
DEFAULT_SOURCE_MIXTURE = {"mit": 0.5, "google": 0.5}


@dataclass(frozen=True)
class _ABISamplingConfig:
    positive_patch_preference: float
    source_mixture: dict[str, float]


def _sampling_config(data_config: Mapping[str, object]) -> _ABISamplingConfig:
    positive_patch_preference = float(data_config.get("positive_patch_preference", 1.0))
    if positive_patch_preference <= 0.0:
        raise ValueError("positive_patch_preference must be positive")
    source_mixture = _source_mixture(data_config.get("source_mixture", DEFAULT_SOURCE_MIXTURE))
    return _ABISamplingConfig(
        positive_patch_preference=positive_patch_preference,
        source_mixture=source_mixture,
    )


def _source_mixture(value: object) -> dict[str, float]:
    if not isinstance(value, Mapping):
        raise ValueError("source_mixture must map Dataset Source names to weights")
    mixture = {str(source).lower(): float(weight) for source, weight in value.items()}
    allowed = {"mit", "google"}
    unknown = set(mixture) - allowed
    if unknown:
        raise ValueError(f"unsupported Dataset Source in source_mixture: {sorted(unknown)}")
    if any(weight < 0.0 for weight in mixture.values()):
        raise ValueError("source_mixture weights must be non-negative")
    total = sum(mixture.values())
    if total <= 0.0:
        raise ValueError("source_mixture must contain at least one positive weight")
    return {source: weight / total for source, weight in mixture.items() if weight > 0.0}


def source_balanced_sampling_weights(
    sample_metadata: Sequence[Mapping[str, object]],
    *,
    sampling_policy: str,
    positive_patch_preference: float = 1.0,
    source_mixture: Mapping[str, float] | None = None,
) -> tuple[float, ...]:
    """Return per-sample weights for ABI provider-owned source-aware policies.

    Source weights are normalised within each Dataset Source so
    ``combined_source_balanced`` follows an explicit mixture rather than raw
    source counts. Positive-patch preference reweights positives within each
    source without changing that source's total mixture mass.
    """

    if positive_patch_preference <= 0.0:
        raise ValueError("positive_patch_preference must be positive")
    if sampling_policy == SAMPLING_POLICY_MIT_ONLY:
        mixture = {"mit": 1.0}
    elif sampling_policy == SAMPLING_POLICY_GOOGLE_ONLY:
        mixture = {"google": 1.0}
    elif sampling_policy == SAMPLING_POLICY_COMBINED_SOURCE_BALANCED:
        mixture = _source_mixture(source_mixture or DEFAULT_SOURCE_MIXTURE)
    else:
        raise ValueError(f"unsupported ABI source-aware sampling policy: {sampling_policy}")

    sources = [str(row.get("dataset_source", "")).lower() for row in sample_metadata]
    positives = [bool(row.get("positive", False)) for row in sample_metadata]
    weights = [0.0 for _ in sample_metadata]
    for source, source_mass in mixture.items():
        indices = [index for index, row_source in enumerate(sources) if row_source == source]
        if not indices:
            raise ValueError(f"sampling policy {sampling_policy!r} requested Dataset Source {source!r}, but no samples are available")
        raw = [positive_patch_preference if positives[index] else 1.0 for index in indices]
        raw_total = sum(raw)
        for index, raw_weight in zip(indices, raw, strict=True):
            weights[index] = source_mass * raw_weight / raw_total
    return tuple(weights)


class ABITrainingAdapter:
    """Trusted ml-autoresearch training adapter for the ABI vertical slice."""

    def __init__(self, data_config: Mapping[str, object] | None = None) -> None:
        from abi_contrail.artifact_filters import build_default_artifact_filter_pipeline

        self.filter_pipeline = build_default_artifact_filter_pipeline(data_config)
        self._sampling_config = _sampling_config(data_config or {})

    def validate_data_root(self, data_config: Mapping[str, object]) -> Path:
        root = Path(str(data_config.get("dataset_root", "."))).expanduser().resolve()
        if not root.is_dir():
            from ml_autoresearch.errors import ResearchProblemDataError

            raise ResearchProblemDataError(f"ABI dataset_root does not exist or is not a directory: {root}")
        source_configs = self._source_data_configs(root, data_config)
        for source_config in source_configs:
            self._resolve_required_path(root, source_config, "inputs_zarr")
            self._resolve_required_path(root, source_config, "labels_zarr")
            layout = source_config.get("layout")
            if layout not in {"mit", "google"}:
                from ml_autoresearch.errors import ResearchProblemDataError

                raise ResearchProblemDataError("ABI data_config.layout must be 'mit' or 'google'")
        return root

    def dataset_metadata(self, data_config: Mapping[str, object]) -> dict[str, object]:
        root = self.validate_data_root(data_config)
        metadata: dict[str, object] = {
            "id": RESEARCH_PROBLEM_ID,
            "dataset_root": str(root),
            "host_data_path": str(root),
            "input_mode": str(data_config.get("input_mode", INPUT_MODE_ABI_16CH)),
            "target": "contrail_mask",
        }
        if "layout" in data_config:
            metadata["layout"] = str(data_config["layout"])
        if "inputs_zarr" in data_config:
            metadata["inputs_zarr"] = str(data_config["inputs_zarr"])
        if "labels_zarr" in data_config:
            metadata["labels_zarr"] = str(data_config["labels_zarr"])
        for optional_key in (
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
            "positive_patch_preference",
            "source_mixture",
            "sources",
        ):
            if optional_key in data_config:
                metadata[optional_key] = data_config[optional_key]
        return metadata

    def build_datasets(
        self,
        *,
        data_config: Mapping[str, object],
        resolved_manifest_path: str | Path,
        max_samples: int | None = None,
    ):
        from ml_autoresearch.training_adapters import ResearchProblemDatasets

        root = self.validate_data_root(data_config)
        input_mode = self._input_mode_from_manifest(resolved_manifest_path)
        source_datasets: list[tuple[_TorchABIPatchDataset, _TorchABIPatchDataset, dict[str, object]]] = []
        for source_config in self._source_data_configs(root, data_config):
            layout = str(source_config["layout"])
            inputs_path = self._resolve_required_path(root, source_config, "inputs_zarr")
            labels_path = self._resolve_required_path(root, source_config, "labels_zarr")
            arrays = open_abi_patch_arrays(inputs_path, labels_path, layout=layout)  # type: ignore[arg-type]
            split_index = self._build_split_index(arrays.labels, layout=layout, data_config=source_config)
            train_records = self._limit_records(split_index.train, max_samples)
            validation_records = self._limit_records(split_index.validation, max_samples)
            source_datasets.append(
                (
                    _TorchABIPatchDataset(ABIPatchDataset(arrays, train_records, input_mode=input_mode)),
                    _TorchABIPatchDataset(ABIPatchDataset(arrays, validation_records, input_mode=input_mode)),
                    split_index.data_policy_metadata,
                )
            )
        if len(source_datasets) == 1:
            train_dataset, validation_dataset, split_metadata = source_datasets[0]
        else:
            train_dataset = _CombinedTorchABIPatchDataset(tuple(item[0] for item in source_datasets))
            validation_dataset = _CombinedTorchABIPatchDataset(tuple(item[1] for item in source_datasets))
            split_metadata = {"dataset_source": "combined", "source_split_policies": [item[2] for item in source_datasets]}
        data_policy_metadata = {
            **split_metadata,
            "sampling_policy_owner": "provider/harness",
            "available_sampling_policies": list(ABI_SAMPLING_POLICIES),
            "positive_patch_preference": self._sampling_config.positive_patch_preference,
            "source_mixture": dict(self._sampling_config.source_mixture),
        }
        return ResearchProblemDatasets(
            train_dataset=train_dataset,
            validation_dataset=validation_dataset,
            start_line="Starting ABI Contrail fixture training.",
            success_line="ABI Contrail fixture training completed.",
            failure_prefix="ABI Contrail fixture training failed",
            data_policy_metadata=data_policy_metadata,
        )

    def apply_augmentation_policy(self, dataset: object, augmentation_policy: str) -> object:
        if augmentation_policy != "none":
            from ml_autoresearch.errors import TrainingError

            raise TrainingError(f"unsupported ABI augmentation policy: {augmentation_policy}")
        return dataset

    def data_loader_for_sampling(
        self,
        dataset: object,
        *,
        batch_size: int,
        sampling_policy: str,
        loader_kwargs: Mapping[str, object] | None = None,
    ) -> object | None:
        """Build ABI provider-owned samplers for source-aware training policies."""

        if sampling_policy not in SOURCE_BALANCED_SAMPLING_POLICIES:
            return None
        import torch
        from torch.utils.data import DataLoader, WeightedRandomSampler
        from ml_autoresearch.errors import TrainingError

        if not hasattr(dataset, "sample_metadata"):
            raise TrainingError(f"ABI sampling policy {sampling_policy!r} requires sample metadata")
        metadata = [dataset.sample_metadata(index) for index in range(len(dataset))]  # type: ignore[arg-type]
        weights = source_balanced_sampling_weights(
            metadata,
            sampling_policy=sampling_policy,
            positive_patch_preference=self._sampling_config.positive_patch_preference,
            source_mixture=self._sampling_config.source_mixture,
        )
        generator = torch.Generator()
        generator.manual_seed(SAMPLING_POLICY_SEED)
        sampler = WeightedRandomSampler(
            weights=torch.as_tensor(weights, dtype=torch.double),
            num_samples=len(weights),
            replacement=True,
            generator=generator,
        )
        return DataLoader(dataset, batch_size=batch_size, sampler=sampler, **dict(loader_kwargs or {}))

    def primary_output_name(self, output_spec: Mapping[str, object]) -> str:
        return str(output_spec.get("form", OUTPUT_FORM_MASK_LOGITS))

    def compute_primary_loss(self, loss_name: str, logits: Any, target_mask: Any) -> Any:
        from ml_autoresearch.problem_support.segmentation import bce_dice_cldice_loss, bce_dice_loss, focal_tversky_loss

        losses = {
            "bce_dice": bce_dice_loss,
            "focal_tversky": focal_tversky_loss,
            "bce_dice_cldice": bce_dice_cldice_loss,
        }
        try:
            loss_function = losses[loss_name]
        except KeyError as exc:
            from ml_autoresearch.errors import TrainingError

            raise TrainingError(f"unsupported ABI loss: {loss_name}") from exc
        return loss_function(logits, target_mask)

    def compute_auxiliary_losses(
        self,
        outputs: dict[str, Any],
        target_mask: Any,
        auxiliary_targets: list[dict[str, object]],
    ) -> dict[str, Any]:
        from ml_autoresearch.errors import TrainingError
        from ml_autoresearch.problem_support.segmentation import weighted_bce_loss

        losses: dict[str, Any] = {}
        for target in auxiliary_targets:
            target_name = str(target.get("name", ""))
            output_name = str(target.get("output", ""))
            loss_name = str(target.get("loss", ""))
            if target_name not in AUXILIARY_TARGETS:
                raise TrainingError(f"unsupported ABI auxiliary target: {target_name}")
            expected_output = AUXILIARY_OUTPUTS[target_name]
            if output_name != expected_output:
                raise TrainingError(f"ABI auxiliary target {target_name!r} must use output {expected_output!r}")
            if loss_name != AUXILIARY_LOSS_WEIGHTED_BCE:
                raise TrainingError(f"unsupported ABI auxiliary loss: {loss_name}")
            try:
                logits = outputs[output_name]
            except KeyError as exc:
                raise TrainingError(f"missing ABI auxiliary output: {output_name}") from exc
            auxiliary_target = derive_auxiliary_target(target_name, target_mask)
            if logits.shape != auxiliary_target.shape:
                raise TrainingError(
                    f"ABI auxiliary output {output_name!r} shape {tuple(logits.shape)} does not match target shape "
                    f"{tuple(auxiliary_target.shape)}"
                )
            losses[target_name] = float(target.get("weight", 1.0)) * weighted_bce_loss(logits, auxiliary_target)
        return losses

    def compute_validation_metrics(self, logits: Any, target_mask: Any) -> dict[str, float]:
        import torch
        from ml_autoresearch.problem_support.segmentation import binary_segmentation_metrics, contrail_connectivity_metric

        probabilities = torch.sigmoid(logits.detach().cpu())
        raw_predictions = probabilities >= 0.5
        targets = (target_mask.detach().cpu() >= 0.5)
        filtered_predictions: list[torch.Tensor] = []
        for index in range(raw_predictions.shape[0]):
            filtered = self.filter_pipeline.apply(raw_predictions[index].numpy(), probabilities[index].numpy(), context={})
            filtered_predictions.append(torch.from_numpy(filtered.filtered_mask.astype(bool)))
        filtered_tensor = torch.stack(filtered_predictions)
        raw_metrics = binary_segmentation_metrics(raw_predictions, targets)
        filtered_metrics = binary_segmentation_metrics(filtered_tensor, targets)
        raw_connectivity = contrail_connectivity_metric(raw_predictions, targets)
        filtered_connectivity = contrail_connectivity_metric(filtered_tensor, targets)
        return {
            "val/dice": raw_metrics["dice"],
            "val/iou": raw_metrics["iou"],
            "val/precision": raw_metrics["precision"],
            "val/recall": raw_metrics["recall"],
            "val/raw_dice": raw_metrics["dice"],
            "val/raw_iou": raw_metrics["iou"],
            "val/raw_precision": raw_metrics["precision"],
            "val/raw_recall": raw_metrics["recall"],
            "val/raw_cldice": raw_connectivity,
            "val/raw_contrail_connectivity": raw_connectivity,
            "val/filtered_dice": filtered_metrics["dice"],
            "val/filtered_iou": filtered_metrics["iou"],
            "val/filtered_precision": filtered_metrics["precision"],
            "val/filtered_recall": filtered_metrics["recall"],
            "val/filtered_cldice": filtered_connectivity,
            "val/filtered_contrail_connectivity": filtered_connectivity,
        }

    def selection_policy(self) -> tuple[str, str]:
        return "val/filtered_dice", "max"

    def build_evaluation_dataset(
        self,
        *,
        data_config: Mapping[str, object],
        resolved_manifest_path: str | Path,
    ) -> object:
        datasets = self.build_datasets(data_config=data_config, resolved_manifest_path=resolved_manifest_path)
        return datasets.validation_dataset

    def display_prediction_sample_input(self, inputs: Any) -> Any:
        """Render ABI channels as a simple RGB diagnostic composite.

        The ABI vertical slice exposes 16 physical channels, not natural RGB.
        For qualitative smoke artifacts we map channels 13/7/2 when available
        and min-max each plane independently.
        """

        import torch

        if inputs.ndim != 3 or inputs.shape[0] < 3:
            raise ValueError(f"cannot render ABI sample input with shape {tuple(inputs.shape)}")
        indices = [12, 6, 1] if inputs.shape[0] >= 13 else [0, 1, 2]
        rgb = inputs[indices, :, :].float()
        flat_min = rgb.amin(dim=(1, 2), keepdim=True)
        flat_max = rgb.amax(dim=(1, 2), keepdim=True)
        scale = torch.clamp(flat_max - flat_min, min=1e-6)
        return torch.clamp((rgb - flat_min) / scale, 0.0, 1.0)

    @staticmethod
    def _source_data_configs(root: Path, data_config: Mapping[str, object]) -> tuple[Mapping[str, object], ...]:
        sources = data_config.get("sources")
        if sources is None:
            return (data_config,)
        if not isinstance(sources, Sequence) or isinstance(sources, (str, bytes)):
            from ml_autoresearch.errors import ResearchProblemDataError

            raise ResearchProblemDataError("ABI data_config.sources must be a sequence of source configs")
        source_configs: list[Mapping[str, object]] = []
        for source in sources:
            if not isinstance(source, Mapping):
                from ml_autoresearch.errors import ResearchProblemDataError

                raise ResearchProblemDataError("each ABI data_config.sources item must be a mapping")
            merged = {key: value for key, value in data_config.items() if key != "sources"}
            merged.update(source)
            source_configs.append(merged)
        if not source_configs:
            from ml_autoresearch.errors import ResearchProblemDataError

            raise ResearchProblemDataError("ABI data_config.sources must not be empty")
        return tuple(source_configs)

    def _build_split_index(self, labels: Any, *, layout: str, data_config: Mapping[str, object]):
        if layout == "google":
            metadata_rows = data_config.get("metadata_rows")
            if not isinstance(metadata_rows, Sequence) or isinstance(metadata_rows, (str, bytes)):
                from ml_autoresearch.errors import ResearchProblemDataError

                raise ResearchProblemDataError("google ABI fixtures require data_config.metadata_rows")
            return build_google_abi_patch_index(metadata_rows)  # type: ignore[arg-type]
        return build_mit_abi_patch_index(
            labels,
            scene_names=self._optional_string_sequence(data_config.get("scene_names")),
            goes_times=self._optional_string_sequence(data_config.get("goes_times")),
            val_fraction=float(data_config.get("val_fraction", 0.2)),
            seed=int(data_config.get("split_seed", 20260712)),
            patch_size=int(data_config.get("patch_size", 256)),
            stride=int(data_config.get("stride", 256)),
        )

    @staticmethod
    def _input_mode_from_manifest(resolved_manifest_path: str | Path) -> str:
        path = Path(resolved_manifest_path)
        if not path.is_file():
            return INPUT_MODE_ABI_16CH
        import yaml

        manifest = yaml.safe_load(path.read_text()) or {}
        input_mode = str(manifest.get("input_mode", INPUT_MODE_ABI_16CH))
        if input_mode not in ABI_INPUT_MODE_SOURCE_INDICES:
            from ml_autoresearch.errors import TrainingError

            raise TrainingError(f"unsupported ABI input mode: {input_mode}")
        return input_mode

    @staticmethod
    def _optional_string_sequence(value: object) -> tuple[str, ...] | None:
        if value is None:
            return None
        if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
            raise ValueError("expected a sequence of strings")
        return tuple(str(item) for item in value)

    @staticmethod
    def _limit_records(records: Sequence[ABIPatchIndexRecord], max_samples: int | None) -> tuple[ABIPatchIndexRecord, ...]:
        limit = len(records) if max_samples is None else max(1, min(len(records), int(max_samples)))
        return tuple(records[:limit])

    @staticmethod
    def _resolve_required_path(root: Path, data_config: Mapping[str, object], key: str) -> Path:
        value = data_config.get(key)
        if not isinstance(value, str) or not value:
            from ml_autoresearch.errors import ResearchProblemDataError

            raise ResearchProblemDataError(f"ABI data_config.{key} is required")
        path = Path(value).expanduser()
        if not path.is_absolute():
            path = root / path
        path = path.resolve()
        if not path.exists():
            from ml_autoresearch.errors import ResearchProblemDataError

            raise ResearchProblemDataError(f"ABI data_config.{key} does not exist: {path}")
        return path


class _TorchABIPatchDataset:
    """Tuple/tensor view expected by the generic ml-autoresearch training loop."""

    def __init__(self, dataset: ABIPatchDataset) -> None:
        self.dataset = dataset

    def __len__(self) -> int:
        return len(self.dataset)

    def __getitem__(self, index: int):
        import torch

        sample = self.dataset[index]
        return torch.from_numpy(sample["inputs"]), torch.from_numpy(sample["target"])

    def sample_metadata(self, index: int) -> dict[str, object]:
        if self.dataset.index_records:
            record = self.dataset.index_records[index]
            return {
                "dataset_source": record.dataset_source,
                "split": record.split,
                "scene_name": record.scene_name,
                "scene_index": record.scene_index,
                "goes_time": record.goes_time,
                "row": record.row,
                "col": record.col,
                "positive": record.positive,
            }
        sample = self.dataset[index]
        metadata = sample.get("metadata", {})
        return dict(metadata) if isinstance(metadata, Mapping) else {}

    def filter_context(self, index: int) -> dict[str, object]:
        """Return trusted provider-only context for Artifact Filters.

        Longitude and latitude are read from source channels 16/17 when present,
        but they are never returned by ``__getitem__`` and therefore are not
        exposed as candidate model inputs.
        """

        import numpy as np

        source = self.dataset.raw_inputs(index)
        context: dict[str, object] = {}
        if source.shape[-1] > 17:
            context["longitude"] = np.asarray(source[..., 16], dtype=np.float64)
            context["latitude"] = np.asarray(source[..., 17], dtype=np.float64)
        return context


class _CombinedTorchABIPatchDataset:
    """Concatenate provider ABI datasets while preserving per-source metadata."""

    def __init__(self, datasets: Sequence[_TorchABIPatchDataset]) -> None:
        if not datasets:
            raise ValueError("combined ABI dataset requires at least one source dataset")
        self.datasets = tuple(datasets)
        self._offsets: list[int] = []
        offset = 0
        for dataset in self.datasets:
            self._offsets.append(offset)
            offset += len(dataset)
        self._length = offset

    def __len__(self) -> int:
        return self._length

    def __getitem__(self, index: int):
        dataset, local_index = self._resolve(index)
        return dataset[local_index]

    def sample_metadata(self, index: int) -> dict[str, object]:
        dataset, local_index = self._resolve(index)
        return dataset.sample_metadata(local_index)

    def filter_context(self, index: int) -> dict[str, object]:
        dataset, local_index = self._resolve(index)
        return dataset.filter_context(local_index)

    def _resolve(self, index: int) -> tuple[_TorchABIPatchDataset, int]:
        if index < 0:
            index += len(self)
        if index < 0 or index >= len(self):
            raise IndexError(index)
        for dataset_index in range(len(self.datasets) - 1, -1, -1):
            offset = self._offsets[dataset_index]
            if index >= offset:
                return self.datasets[dataset_index], index - offset
        raise IndexError(index)


def _input_specs() -> dict[str, dict[str, object]]:
    forbidden_names = ["longitude", "latitude"]
    forbidden_indices = list(ABI_FORBIDDEN_SOURCE_INDICES)
    return {
        INPUT_MODE_ABI_16CH: {
            "mode": INPUT_MODE_ABI_16CH,
            "shape": [16, 256, 256],
            "layout": "channel_first",
            "channel_set": "goes_abi_channels_1_16",
            "source_channel_indices": list(ABI_INPUT_MODE_SOURCE_INDICES[INPUT_MODE_ABI_16CH]),
            "goes_abi_channel_numbers": list(range(1, 17)),
            "forbidden_channels": forbidden_names,
            "forbidden_source_channel_indices": forbidden_indices,
        },
        INPUT_MODE_ABI_16CH_PLUS_SZA: {
            "mode": INPUT_MODE_ABI_16CH_PLUS_SZA,
            "shape": [17, 256, 256],
            "layout": "channel_first",
            "channel_set": "goes_abi_channels_1_16_plus_solar_geometry_input",
            "source_channel_indices": list(ABI_INPUT_MODE_SOURCE_INDICES[INPUT_MODE_ABI_16CH_PLUS_SZA]),
            "goes_abi_channel_numbers": list(range(1, 17)),
            "extra_inputs": [{"name": "solar_zenith_angle", "source_channel_index": 18}],
            "forbidden_channels": forbidden_names,
            "forbidden_source_channel_indices": forbidden_indices,
        },
        INPUT_MODE_ABI_THERMAL_10CH: {
            "mode": INPUT_MODE_ABI_THERMAL_10CH,
            "shape": [10, 256, 256],
            "layout": "channel_first",
            "channel_set": "goes_abi_channels_7_16",
            "source_channel_indices": list(ABI_INPUT_MODE_SOURCE_INDICES[INPUT_MODE_ABI_THERMAL_10CH]),
            "goes_abi_channel_numbers": list(range(7, 17)),
            "forbidden_channels": forbidden_names,
            "forbidden_source_channel_indices": forbidden_indices,
        },
    }


def derive_auxiliary_target(target_name: str, target_mask: Any) -> Any:
    """Derive a trusted ABI auxiliary target from the Contrail Mask target."""

    from ml_autoresearch.problem_support.segmentation import derive_boundary_target_v1, derive_line_target_v1, _soft_skeletonize

    if target_name == AUXILIARY_TARGET_LINE:
        return derive_line_target_v1(target_mask)
    if target_name == AUXILIARY_TARGET_BOUNDARY:
        return derive_boundary_target_v1(target_mask)
    if target_name == AUXILIARY_TARGET_CENTERLINE:
        return _soft_skeletonize(target_mask.float().clamp(0.0, 1.0), iterations=32)
    raise ValueError(f"unsupported ABI auxiliary target: {target_name}")


def split_data_policy_metadata() -> dict[str, object]:
    """Provider-owned split/index policy metadata for ABI Patch data adapters."""

    return {
        "google_split_policy": "respect_google_scene_name_train_validation_provenance",
        "mit_split_policy": "deterministic_whole_scene_train_validation_split_before_windowing",
        "mit_window_shape": [256, 256],
        "sampling_policy_owner": "provider/harness",
        "sampling_policies": list(ABI_SAMPLING_POLICIES),
        "positive_patch_preference_metadata_key": "positive_patch_preference",
        "source_mixture_metadata_key": "source_mixture",
        "records_include": [
            "dataset_source",
            "scene_name",
            "scene_index",
            "goes_time",
            "row",
            "col",
            "split",
            "positive",
        ],
    }


def build_spec(data_config: Mapping[str, object] | None = None):
    """Build the GOES ABI Contrail Segmentation Research Problem Spec.

    Parameters
    ----------
    data_config:
        Accepted for the ml-autoresearch provider interface. Runtime data paths
        are validated by :class:`ABITrainingAdapter` before training.
    """

    filter_config = dict(data_config or {})

    from ml_autoresearch.research_problems import ResearchProblemSpec
    from abi_contrail.artifact_filters import build_default_artifact_filter_pipeline
    from abi_contrail.evaluation import ABIEvaluationAdapter, EVALUATION_MODE_WHOLE_VALIDATION_FAILURE_ANALYSIS

    training_adapter = ABITrainingAdapter(filter_config)
    evaluation_adapter = ABIEvaluationAdapter(
        training_adapter=training_adapter,
        filter_pipeline=build_default_artifact_filter_pipeline(filter_config),
    )
    return ResearchProblemSpec(
        id=RESEARCH_PROBLEM_ID,
        version=RESEARCH_PROBLEM_VERSION,
        contract_version=CONTRACT_VERSION,
        input_modes=INPUT_MODE_ABI_INPUTS,
        input_specs=_input_specs(),
        output_forms=(OUTPUT_FORM_MASK_LOGITS,),
        output_specs={
            OUTPUT_FORM_MASK_LOGITS: {
                "form": OUTPUT_FORM_MASK_LOGITS,
                "shape": [1, 256, 256],
                "target": "contrail_mask",
            },
        },
        losses=("bce_dice", "focal_tversky", "bce_dice_cldice"),
        auxiliary_targets=AUXILIARY_TARGETS,
        auxiliary_outputs=AUXILIARY_OUTPUTS,
        auxiliary_output_shapes=AUXILIARY_OUTPUT_SHAPES,
        auxiliary_losses=(AUXILIARY_LOSS_WEIGHTED_BCE,),
        optimizers=("adamw",),
        sampling_policies=ABI_SAMPLING_POLICIES,
        frame_selection_policies=("all_target_frames",),
        input_mode_frame_selection_defaults={mode: "all_target_frames" for mode in INPUT_MODE_ABI_INPUTS},
        augmentation_policies=("none",),
        primary_metric="val/filtered_dice",
        operation_capabilities={"training": True, "evaluation_modes": (EVALUATION_MODE_WHOLE_VALIDATION_FAILURE_ANALYSIS,)},
        training_adapter=training_adapter,
        evaluation_adapter=evaluation_adapter,
        brief_documents=(
            {
                "name": "goes_abi_contrail_segmentation",
                "role": "problem_brief",
                "path": "abi_contrail/brief/goes-abi-contrail-segmentation.md",
                "summary": "Initial GOES ABI Contrail Segmentation task contract and provider registration notes.",
                "required": True,
            },
        ),
        dataset_profile_artifacts=(
            {
                "name": "goes_abi_initial_dataset_profile",
                "role": "initial_dataset_profile_placeholder",
                "path": "abi_contrail/profile/initial-dataset-profile.md",
                "summary": "Placeholder dataset profile for the ABI provider scaffold; filled by later data-profile tasks.",
                "split_scope": "not yet data-backed in ABI-001 scaffold",
                "required": False,
            },
        ),
    )
