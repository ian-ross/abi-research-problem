"""ABI provider-owned Post-Run Evaluation adapter with Artifact Filters."""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from abi_contrail.adapters import ABITrainingAdapter
from abi_contrail.artifact_filters import ABIArtifactFilterPipeline, build_default_artifact_filter_pipeline

EVALUATION_MODE_WHOLE_VALIDATION_FAILURE_ANALYSIS = "whole_validation_failure_analysis"


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

    def display_prediction_sample_input(self, inputs: Any) -> Any:
        return self.training_adapter.display_prediction_sample_input(inputs)

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
        from ml_autoresearch.problem_support.segmentation import binary_confusion_counts, binary_segmentation_metrics, contrail_connectivity_metric
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

        raw_predictions: list[torch.Tensor] = []
        filtered_predictions: list[torch.Tensor] = []
        targets_all: list[torch.Tensor] = []
        probabilities_all: list[torch.Tensor] = []
        per_sample_records: list[dict[str, object]] = []
        removed_pixels_total = 0
        removed_area_total = 0.0
        with torch.no_grad():
            for start in range(0, len(dataset), batch_size):
                batch_indices = list(range(start, min(start + batch_size, len(dataset))))
                inputs = torch.stack([dataset[index][0] for index in batch_indices]).to(device)
                targets = torch.stack([dataset[index][1] for index in batch_indices]).to(device)
                logits = _extract_mask_logits(model(inputs), output_spec)[0]
                probabilities = torch.sigmoid(logits).detach().cpu()
                predictions = probabilities >= threshold
                target_masks = (targets >= 0.5).detach().cpu()
                for offset, index in enumerate(batch_indices):
                    probability = probabilities[offset].numpy()
                    prediction = predictions[offset].numpy()
                    context = _filter_context(dataset, index)
                    filtered = filter_pipeline.apply(prediction, probability, context=context)
                    filtered_prediction = torch.from_numpy(filtered.filtered_mask.astype(bool))
                    sample_prediction = predictions[offset : offset + 1]
                    sample_filtered_prediction = filtered_prediction.unsqueeze(0)
                    sample_target = target_masks[offset : offset + 1]
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
                    record.update(_sample_metadata(dataset, index))
                    per_sample_records.append(record)
                    raw_predictions.append(sample_prediction)
                    filtered_predictions.append(sample_filtered_prediction)
                    probabilities_all.append(probabilities[offset : offset + 1])
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
            **{f"filtered/{key}": value for key, value in filtered_aggregate.items()},
            "filtered/cldice": filtered_connectivity,
            "filtered/contrail_connectivity": filtered_connectivity,
            "artifact_filters/removed_pixel_count": float(removed_pixels_total),
            "artifact_filters/removed_area_km2": float(removed_area_total),
        }
        threshold_sweep = {"default_threshold": float(threshold), "note": "ABI filtered evaluation records threshold-specific raw and filtered metrics."}
        diagnostic_manifest = {"samples": [], "note": "ABI v0 filtered evaluation does not yet emit qualitative diagnostic images."}
        return aggregate, per_sample_records, threshold_sweep, diagnostic_manifest


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


def _filter_context(dataset: object, index: int) -> dict[str, object]:
    getter = getattr(dataset, "filter_context", None)
    if callable(getter):
        return dict(getter(index))
    return {}


def _sample_metadata(dataset: object, index: int) -> dict[str, object]:
    getter = getattr(dataset, "sample_metadata", None)
    if callable(getter):
        return {f"sample/{key}": value for key, value in dict(getter(index)).items()}
    return {}


__all__ = ["ABIEvaluationAdapter", "EVALUATION_MODE_WHOLE_VALIDATION_FAILURE_ANALYSIS"]
