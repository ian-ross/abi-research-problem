"""Trusted adapters and ResearchProblemSpec declaration for GOES ABI Contrail Segmentation.

The provider spec is declarative, while this module also hosts the trusted
vertical-slice training adapter used by ml-autoresearch. Candidate code still
cannot own data loading, losses, metrics, or sampling policy boundaries.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
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
INPUT_MODE_ABI_INPUTS = (INPUT_MODE_ABI_16CH, INPUT_MODE_ABI_16CH_PLUS_SZA, INPUT_MODE_ABI_THERMAL_10CH)


class ABITrainingAdapter:
    """Trusted ml-autoresearch training adapter for the ABI vertical slice."""

    def validate_data_root(self, data_config: Mapping[str, object]) -> Path:
        root = Path(str(data_config.get("dataset_root", "."))).expanduser().resolve()
        if not root.is_dir():
            from ml_autoresearch.errors import ResearchProblemDataError

            raise ResearchProblemDataError(f"ABI dataset_root does not exist or is not a directory: {root}")
        self._resolve_required_path(root, data_config, "inputs_zarr")
        self._resolve_required_path(root, data_config, "labels_zarr")
        layout = data_config.get("layout")
        if layout not in {"mit", "google"}:
            from ml_autoresearch.errors import ResearchProblemDataError

            raise ResearchProblemDataError("ABI data_config.layout must be 'mit' or 'google'")
        return root

    def dataset_metadata(self, data_config: Mapping[str, object]) -> dict[str, object]:
        root = self.validate_data_root(data_config)
        return {
            "id": RESEARCH_PROBLEM_ID,
            "dataset_root": str(root),
            "layout": str(data_config["layout"]),
            "input_mode": str(data_config.get("input_mode", INPUT_MODE_ABI_16CH)),
            "target": "contrail_mask",
        }

    def build_datasets(
        self,
        *,
        data_config: Mapping[str, object],
        resolved_manifest_path: str | Path,
        max_samples: int | None = None,
    ):
        from ml_autoresearch.training_adapters import ResearchProblemDatasets

        root = self.validate_data_root(data_config)
        layout = str(data_config["layout"])
        inputs_path = self._resolve_required_path(root, data_config, "inputs_zarr")
        labels_path = self._resolve_required_path(root, data_config, "labels_zarr")
        input_mode = self._input_mode_from_manifest(resolved_manifest_path)
        arrays = open_abi_patch_arrays(inputs_path, labels_path, layout=layout)  # type: ignore[arg-type]
        split_index = self._build_split_index(arrays.labels, layout=layout, data_config=data_config)
        train_records = self._limit_records(split_index.train, max_samples)
        validation_records = self._limit_records(split_index.validation, max_samples)
        train_dataset = _TorchABIPatchDataset(ABIPatchDataset(arrays, train_records, input_mode=input_mode))
        validation_dataset = _TorchABIPatchDataset(ABIPatchDataset(arrays, validation_records, input_mode=input_mode))
        return ResearchProblemDatasets(
            train_dataset=train_dataset,
            validation_dataset=validation_dataset,
            start_line="Starting ABI Contrail fixture training.",
            success_line="ABI Contrail fixture training completed.",
            failure_prefix="ABI Contrail fixture training failed",
            data_policy_metadata=split_index.data_policy_metadata,
        )

    def apply_augmentation_policy(self, dataset: object, augmentation_policy: str) -> object:
        if augmentation_policy != "none":
            from ml_autoresearch.errors import TrainingError

            raise TrainingError(f"unsupported ABI augmentation policy: {augmentation_policy}")
        return dataset

    def primary_output_name(self, output_spec: Mapping[str, object]) -> str:
        return str(output_spec.get("form", OUTPUT_FORM_MASK_LOGITS))

    def compute_primary_loss(self, loss_name: str, logits: Any, target_mask: Any) -> Any:
        if loss_name != "bce_dice":
            from ml_autoresearch.errors import TrainingError

            raise TrainingError(f"unsupported ABI loss: {loss_name}")
        from ml_autoresearch.problem_support.segmentation import bce_dice_loss

        return bce_dice_loss(logits, target_mask)

    def compute_auxiliary_losses(
        self,
        outputs: dict[str, Any],
        target_mask: Any,
        auxiliary_targets: list[dict[str, object]],
    ) -> dict[str, Any]:
        del outputs, target_mask
        if auxiliary_targets:
            from ml_autoresearch.errors import TrainingError

            raise TrainingError("ABI v0 vertical slice does not support auxiliary targets")
        return {}

    def compute_validation_metrics(self, logits: Any, target_mask: Any) -> dict[str, float]:
        from ml_autoresearch.problem_support.segmentation import binary_segmentation_validation_metrics

        return binary_segmentation_validation_metrics(logits, target_mask)

    def selection_policy(self) -> tuple[str, str]:
        return "val/dice", "max"

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


def split_data_policy_metadata() -> dict[str, object]:
    """Provider-owned split/index policy metadata for ABI Patch data adapters."""

    return {
        "google_split_policy": "respect_google_scene_name_train_validation_provenance",
        "mit_split_policy": "deterministic_whole_scene_train_validation_split_before_windowing",
        "mit_window_shape": [256, 256],
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

    del data_config

    from ml_autoresearch.research_problems import ResearchProblemSpec

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
        losses=("bce_dice",),
        optimizers=("adamw",),
        sampling_policies=("sequential", "deterministic_shuffle"),
        frame_selection_policies=("all_target_frames",),
        input_mode_frame_selection_defaults={mode: "all_target_frames" for mode in INPUT_MODE_ABI_INPUTS},
        augmentation_policies=("none",),
        primary_metric="val/dice",
        operation_capabilities={"training": True},
        training_adapter=ABITrainingAdapter(),
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
