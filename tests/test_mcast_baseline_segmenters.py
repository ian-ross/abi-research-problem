from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
import torch
import zarr

from abi_contrail.baseline_segmenters import (
    MCAST_BASELINE_1_1,
    MCAST_BASELINE_2_1,
    MCASTBaselineSegmenter,
    mcast_input_from_abi_source,
)
from abi_contrail.evaluation import ABIEvaluationAdapter


class ConstantTwoClassModel(torch.nn.Module):
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        class0 = torch.zeros((x.shape[0], 1, x.shape[2], x.shape[3]), dtype=x.dtype, device=x.device)
        class1 = torch.full_like(class0, 2.0)
        return torch.cat([class0, class1], dim=1)


def _model_factory(**_kwargs: object) -> ConstantTwoClassModel:
    return ConstantTwoClassModel()


def test_mcast_input_uses_c11_c14_and_c13_minus_c15_without_lat_lon() -> None:
    source = np.zeros((4, 5, 19), dtype=np.float32)
    source[..., 10] = 11.0
    source[..., 13] = 14.0
    source[..., 12] = 13.0
    source[..., 14] = 15.0
    source[..., 16] = -99.0
    source[..., 17] = 99.0

    mcast = mcast_input_from_abi_source(source)

    assert mcast.shape == (3, 4, 5)
    assert np.all(mcast[0] == 11.0)
    assert np.all(mcast[1] == 14.0)
    assert np.all(mcast[2] == -2.0)


def test_mcast_v1_checkpoint_loads_offline_and_returns_class1_probability(tmp_path: Path) -> None:
    checkpoint = tmp_path / "detection-1.1.pt"
    torch.save({}, checkpoint)

    baseline = MCASTBaselineSegmenter.load(MCAST_BASELINE_1_1, checkpoint, model_factory=_model_factory)
    source = np.zeros((33, 35, 19), dtype=np.float32)
    result = baseline.predict_patch(source)

    assert baseline.version == "1.1"
    assert result.probabilities.shape == (1, 33, 35)
    assert result.mask.shape == (1, 33, 35)
    assert torch.allclose(result.probabilities, torch.full((1, 33, 35), torch.softmax(torch.tensor([0.0, 2.0]), dim=0)[1]))
    assert result.mask.all()


def test_mcast_v2_directory_loads_offline(tmp_path: Path) -> None:
    asset_dir = tmp_path / "detection-2.1"
    asset_dir.mkdir()
    (asset_dir / "config.json").write_text(
        '{"architecture":"Unet","encoder":"resnet18","pretrained_encoder":null,'
        '"n_channels":3,"encoder_depth":5,"decoder_channels":[256,128,64,32,16]}'
    )
    np.save(asset_dir / "means.npy", np.asarray([1.0, 2.0, 3.0], dtype=np.float32))
    np.save(asset_dir / "stds.npy", np.asarray([4.0, 5.0, 6.0], dtype=np.float32))
    (asset_dir / "threshold.dat").write_text("0.7\n")
    torch.save({}, asset_dir / "checkpoint.pt")

    baseline = MCASTBaselineSegmenter.load(MCAST_BASELINE_2_1, asset_dir, model_factory=_model_factory)

    assert baseline.version == "2.1"
    assert baseline.threshold == pytest.approx(0.7)
    assert baseline.means.tolist() == [1.0, 2.0, 3.0]


def test_baseline_evaluation_uses_same_filtered_metric_path_and_records_baseline(tmp_path: Path) -> None:
    data_root = tmp_path / "fixture"
    data_root.mkdir()
    inputs_path = data_root / "inputs.zarr"
    labels_path = data_root / "labels.zarr"
    inputs_group = zarr.open_group(str(inputs_path), mode="w")
    labels_group = zarr.open_group(str(labels_path), mode="w")
    inputs = np.zeros((2, 32, 32, 19), dtype=np.float32)
    labels = np.zeros((2, 32, 32), dtype=np.uint8)
    labels[1, :, :] = 1
    inputs_group.create_array("inputs", data=inputs)
    labels_group.create_array("labels", data=labels)
    checkpoint = tmp_path / "detection-1.1.pt"
    torch.save({}, checkpoint)
    data_config = {
        "dataset_root": str(data_root),
        "layout": "google",
        "inputs_zarr": "inputs.zarr",
        "labels_zarr": "labels.zarr",
        "metadata_rows": [
            {"scene_name": "train-000/patch.zarr", "sample_index": 0, "positive": False},
            {"scene_name": "validation-000/patch.zarr", "sample_index": 1, "positive": True},
        ],
        "scanline_min_length_pixels": 9999,
        "mcast_detection_1_1_path": str(checkpoint),
    }

    evaluation_dir = tmp_path / "baseline-evaluation"
    aggregate, records, threshold_sweep, _diagnostics = ABIEvaluationAdapter().run_baseline_validation_evaluation(
        baseline_name=MCAST_BASELINE_1_1,
        data_config=data_config,
        model_factory=_model_factory,
        evaluation_dir=evaluation_dir,
    )

    assert aggregate["raw/dice"] == pytest.approx(1.0)
    assert aggregate["filtered/dice"] == pytest.approx(1.0)
    assert "artifact_filters/removed_pixel_count" in aggregate
    assert records[0]["baseline/name"] == MCAST_BASELINE_1_1
    assert records[0]["Dataset Source"] == "google"
    assert threshold_sweep["default_threshold"] == pytest.approx(0.42)
    assert (evaluation_dir / "aggregate_metrics.json").is_file()
    assert (evaluation_dir / "per_sample_metrics.jsonl").is_file()
    assert (evaluation_dir / "baseline_evaluation_metadata.json").is_file()
