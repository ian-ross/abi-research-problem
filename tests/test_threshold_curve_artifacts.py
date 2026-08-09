from __future__ import annotations

import json

import numpy as np
import pytest
import torch

from abi_contrail.artifact_filters import ABIArtifactFilterPipeline, GeographicFeatureFilter, ScanlineArtifactFilter
from abi_contrail.evaluation import _build_threshold_curve_artifact, _evaluate_probability_tensor, _write_baseline_evaluation_artifacts


class _ThresholdDataset:
    def __len__(self) -> int:
        return 2

    def filter_context(self, index: int) -> dict[str, object]:
        if index != 0:
            return {}
        feature_mask = np.zeros((2, 2), dtype=bool)
        feature_mask[0, 1] = True
        return {"geographic_feature_mask": feature_mask}


def _pipeline() -> ABIArtifactFilterPipeline:
    return ABIArtifactFilterPipeline(
        filters=(GeographicFeatureFilter(pixel_buffer=0), ScanlineArtifactFilter(min_length_pixels=10)),
        pixel_area_km2=1.0,
    )


def test_threshold_curve_artifact_reports_raw_filtered_best_and_equal_precision_recall() -> None:
    probabilities = torch.tensor(
        [
            [[[0.80, 0.90], [0.10, float("nan")]]],
            [[[float("nan"), 0.20], [0.10, 0.00]]],
        ],
        dtype=torch.float32,
    )
    targets = torch.zeros_like(probabilities)
    targets[0, 0, 0, 0] = 1.0

    artifact = _build_threshold_curve_artifact(
        dataset=_ThresholdDataset(),
        probabilities=probabilities,
        targets=targets,
        filter_pipeline=_pipeline(),
        default_threshold=0.5,
        threshold_grid=(0.5, 0.85),
    )

    assert artifact["thresholds"] == [0.5, 0.85]
    raw_05 = artifact["curves"]["raw"][0]
    filtered_05 = artifact["curves"]["filtered"][0]
    assert raw_05["metrics"]["precision"] == pytest.approx(0.5)
    assert raw_05["metrics"]["recall"] == pytest.approx(1.0)
    assert raw_05["metrics"]["dice"] == pytest.approx(2 / 3)
    assert filtered_05["metrics"]["precision"] == pytest.approx(1.0)
    assert filtered_05["metrics"]["recall"] == pytest.approx(1.0)
    assert filtered_05["metrics"]["dice"] == pytest.approx(1.0)
    assert artifact["best_threshold_by_filtered_dice"] == {"threshold": 0.5, "dice": pytest.approx(1.0)}
    assert artifact["precision_recall_equal_threshold"]["threshold"] == pytest.approx(0.5)
    assert artifact["precision_recall_equal_threshold"]["absolute_precision_recall_gap"] == pytest.approx(0.0)
    json.dumps(artifact)


def test_threshold_curve_artifact_handles_empty_masks_no_positives_and_nan_probabilities() -> None:
    probabilities = torch.tensor([[[[float("nan"), 0.7], [0.0, 0.1]]]], dtype=torch.float32)
    targets = torch.zeros_like(probabilities)

    artifact = _build_threshold_curve_artifact(
        dataset=_ThresholdDataset(),
        probabilities=probabilities,
        targets=targets,
        filter_pipeline=_pipeline(),
        default_threshold=0.5,
        threshold_grid=(0.5, 0.8),
    )

    raw_05, raw_08 = artifact["curves"]["raw"]
    assert raw_05["counts"]["predicted_positive_pixel_count"] == 1
    assert raw_05["metrics"]["recall"] == pytest.approx(1.0)
    assert raw_05["metrics"]["precision"] > 0.0
    assert raw_08["counts"]["predicted_positive_pixel_count"] == 0
    assert raw_08["metrics"]["dice"] == pytest.approx(1.0)
    assert artifact["best_threshold_by_filtered_dice"]["threshold"] == pytest.approx(0.5)
    json.dumps(artifact)


def test_evaluation_returns_serializable_threshold_curve_without_changing_aggregate_metrics(tmp_path) -> None:
    probabilities = torch.tensor([[[[0.8, 0.9], [0.0, 0.0]]]], dtype=torch.float32)
    targets = torch.zeros_like(probabilities)
    targets[0, 0, 0, 0] = 1.0

    progress_messages: list[str] = []
    aggregate, per_sample, threshold_sweep, diagnostic_manifest = _evaluate_probability_tensor(
        dataset=_ThresholdDataset(),
        probabilities=probabilities,
        targets=targets,
        threshold=0.5,
        filter_pipeline=_pipeline(),
        diagnostic_output_dir=None,
        max_artifact_samples=0,
        progress_callback=progress_messages.append,
        log_every=1,
    )

    assert any("metrics/filtering samples: 1/1" in message for message in progress_messages)
    assert any("threshold sweep: 19/19" in message for message in progress_messages)
    assert aggregate["filtered/dice"] == pytest.approx(1.0)
    assert aggregate["raw/dice"] == pytest.approx(2 / 3)
    assert threshold_sweep["artifact_type"] == "abi_threshold_curve_evaluation"
    assert diagnostic_manifest["postprocessing"]["backend"] == "torch_cpu"
    assert diagnostic_manifest["postprocessing"]["max_device_batch_samples"] == 1
    assert set(diagnostic_manifest["postprocessing"]["timings_seconds"]) == {
        "artifact_filter_context_preparation",
        "artifact_filter",
        "ordinary_metric",
        "connectivity_metric",
        "threshold_sweep",
    }

    _write_baseline_evaluation_artifacts(
        evaluation_dir=tmp_path,
        baseline_name="fixture_baseline",
        baseline_version="test",
        asset_path=tmp_path / "asset.pt",
        threshold=0.5,
        result=(aggregate, per_sample, threshold_sweep, diagnostic_manifest),
    )
    payload = json.loads((tmp_path / "threshold_sweep.json").read_text())
    assert payload["best_threshold_by_filtered_dice"]["threshold"] == pytest.approx(0.05)
    assert json.loads((tmp_path / "aggregate_metrics.json").read_text())["metrics"]["filtered/dice"] == pytest.approx(1.0)
    metadata = json.loads((tmp_path / "baseline_evaluation_metadata.json").read_text())
    assert metadata["postprocessing"]["backend"] == "torch_cpu"
