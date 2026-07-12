from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest
import yaml
import torch
import zarr

from abi_contrail.adapters import ABITrainingAdapter, build_spec, derive_auxiliary_target
from ml_autoresearch.evaluations import evaluate_run
from ml_autoresearch.research_problems import ResearchProblemProviderConfig, load_research_problem_provider
from ml_autoresearch.runs import RunStatus, run_candidate_with_research_problem
from ml_autoresearch.training import _best_validation_metrics


def _write_google_fixture(root: Path) -> dict[str, object]:
    root.mkdir()
    inputs_path = root / "inputs.zarr"
    labels_path = root / "labels.zarr"
    inputs_group = zarr.open_group(str(inputs_path), mode="w")
    labels_group = zarr.open_group(str(labels_path), mode="w")
    inputs = np.zeros((2, 256, 256, 19), dtype=np.float32)
    labels = np.zeros((2, 256, 256), dtype=np.uint8)
    inputs[0, :, :, 0] = 0.25
    inputs[1, :, :, 1] = 0.75
    labels[0, 32:96, 32:96] = 1
    labels[1, 64:128, 64:128] = 2
    inputs_group.create_array("inputs", data=inputs)
    labels_group.create_array("labels", data=labels)
    return {
        "dataset_root": str(root),
        "layout": "google",
        "inputs_zarr": "inputs.zarr",
        "labels_zarr": "labels.zarr",
        "metadata_rows": [
            {"scene_name": "train-000/patch.zarr", "sample_index": 0, "positive": True},
            {"scene_name": "validation-000/patch.zarr", "sample_index": 1, "positive": True},
        ],
    }


def _write_minimal_candidate(root: Path) -> Path:
    candidate = root / "candidate"
    candidate.mkdir()
    (candidate / "manifest.yaml").write_text(
        yaml.safe_dump(
            {
                "name": "abi_vertical_slice_candidate",
                "research_problem": "goes_abi_contrail_segmentation",
                "input_mode": "abi_16ch",
                "output_form": "mask_logits",
                "data": {"sampling_policy": "sequential", "augmentation_policy": "none"},
                "training": {
                    "loss": "bce_dice",
                    "optimizer": "adamw",
                    "learning_rate": 0.001,
                    "batch_size": 1,
                    "max_epochs": 1,
                },
            },
            sort_keys=False,
        )
    )
    (candidate / "model.py").write_text(
        "import torch\n"
        "\n"
        "class ABITinyMask(torch.nn.Module):\n"
        "    def __init__(self, channels):\n"
        "        super().__init__()\n"
        "        self.net = torch.nn.Conv2d(channels, 1, kernel_size=1)\n"
        "\n"
        "    def forward(self, x):\n"
        "        return {'mask_logits': self.net(x)}\n"
        "\n"
        "def build_model(input_spec, output_spec):\n"
        "    return ABITinyMask(int(input_spec['shape'][0]))\n"
    )
    return candidate


def test_abi_training_adapter_validates_data_root_and_builds_split_datasets(tmp_path: Path) -> None:
    data_config = _write_google_fixture(tmp_path / "fixture")
    adapter = ABITrainingAdapter()

    root = adapter.validate_data_root(data_config)
    datasets = adapter.build_datasets(data_config=data_config, resolved_manifest_path=tmp_path / "resolved.yaml")

    assert root == (tmp_path / "fixture").resolve()
    assert len(datasets.train_dataset) == 1
    assert len(datasets.validation_dataset) == 1
    assert datasets.data_policy_metadata["split_policy"] == "respect_google_scene_name_train_validation_provenance"


def test_training_adapter_uses_resolved_manifest_input_mode_for_channel_selection(tmp_path: Path) -> None:
    data_config = _write_google_fixture(tmp_path / "fixture")
    resolved_manifest = tmp_path / "resolved.yaml"
    resolved_manifest.write_text("input_mode: abi_thermal_10ch\n")
    adapter = ABITrainingAdapter()

    datasets = adapter.build_datasets(data_config=data_config, resolved_manifest_path=resolved_manifest)
    inputs, target = datasets.train_dataset[0]

    assert tuple(inputs.shape) == (10, 256, 256)
    assert tuple(target.shape) == (1, 256, 256)


def test_training_adapter_dispatches_trusted_allowlisted_primary_losses() -> None:
    adapter = ABITrainingAdapter()
    logits = torch.zeros((1, 1, 4, 4), dtype=torch.float32)
    target = torch.zeros_like(logits)
    target[:, :, 1:3, 1:3] = 1.0

    for loss_name in ("bce_dice", "focal_tversky", "bce_dice_cldice"):
        loss = adapter.compute_primary_loss(loss_name, logits, target)
        assert torch.isfinite(loss)


def test_abi_auxiliary_targets_have_mask_logit_shape_and_expected_values() -> None:
    target = torch.zeros((1, 1, 7, 7), dtype=torch.float32)
    target[:, :, 1:6, 3] = 1.0

    line = derive_auxiliary_target("line", target)
    boundary = derive_auxiliary_target("boundary", target)
    centerline = derive_auxiliary_target("centerline", target)

    assert line.shape == target.shape
    assert boundary.shape == target.shape
    assert centerline.shape == target.shape
    assert torch.equal(centerline, target)
    assert line[0, 0, 3, 2] == 1.0
    assert boundary[0, 0, 3, 3] == 1.0


def test_training_adapter_computes_manifest_declared_auxiliary_losses() -> None:
    adapter = ABITrainingAdapter()
    target = torch.zeros((1, 1, 7, 7), dtype=torch.float32)
    target[:, :, 2:5, 2:5] = 1.0
    outputs = {
        "line_logits": torch.zeros_like(target),
        "boundary_logits": torch.zeros_like(target),
        "centerline_logits": torch.zeros_like(target),
    }

    losses = adapter.compute_auxiliary_losses(
        outputs,
        target,
        [
            {"name": "line", "output": "line_logits", "loss": "weighted_bce", "weight": 0.2},
            {"name": "boundary", "output": "boundary_logits", "loss": "weighted_bce", "weight": 0.3},
            {"name": "centerline", "output": "centerline_logits", "loss": "weighted_bce", "weight": 0.4},
        ],
    )

    assert set(losses) == {"line", "boundary", "centerline"}
    assert all(torch.isfinite(loss) for loss in losses.values())


def test_build_spec_declares_training_capability_with_filtered_dice_metric() -> None:
    spec = build_spec()

    assert spec.operation_capabilities.training is True
    assert spec.training_adapter is not None
    assert spec.evaluation_adapter is not None
    assert spec.operation_capabilities.evaluation_modes == ("whole_validation_failure_analysis",)
    assert spec.primary_metric == "val/filtered_dice"
    assert spec.training_adapter.selection_policy() == ("val/filtered_dice", "max")


def test_best_epoch_selection_follows_filtered_dice_not_raw_dice() -> None:
    best = _best_validation_metrics(
        [
            {"split": "val", "epoch": 1, "val/dice": 0.9, "val/filtered_dice": 0.4},
            {"split": "val", "epoch": 2, "val/dice": 0.5, "val/filtered_dice": 0.8},
        ],
        selection_metric="val/filtered_dice",
        selection_mode="max",
    )

    assert best["epoch"] == 2
    assert best["selection_metric"] == "val/filtered_dice"
    assert best["selection_value"] == 0.8
    assert best["metrics"]["val/dice"] == 0.5


def test_provider_loads_with_training_adapter() -> None:
    loaded = load_research_problem_provider(
        ResearchProblemProviderConfig(
            id="goes_abi_contrail_segmentation",
            expected_contract_version="v0",
            package_root=Path("."),
            provider_target="abi_contrail.research_problem:build_spec",
        )
    )

    assert loaded.spec.operation_capabilities.training is True
    assert loaded.spec.operation_capabilities.evaluation_modes == ("whole_validation_failure_analysis",)
    assert loaded.spec.training_adapter is not None
    assert loaded.spec.evaluation_adapter is not None


def test_minimal_abi_candidate_smoke_and_tiny_training_run_produce_artifacts(tmp_path: Path) -> None:
    pytest.importorskip("torch")
    data_config = _write_google_fixture(tmp_path / "fixture")
    candidate = _write_minimal_candidate(tmp_path)
    provider_config = ResearchProblemProviderConfig(
        id="goes_abi_contrail_segmentation",
        expected_contract_version="v0",
        package_root=Path("."),
        provider_target="abi_contrail.research_problem:build_spec",
        data_config=data_config,
    )

    run = run_candidate_with_research_problem(
        candidate,
        tmp_path / "runs",
        provider_config,
        max_samples=1,
        max_prediction_samples=1,
    )

    assert run.status == RunStatus.COMPLETED
    outputs = run.run_dir / "outputs"
    assert (outputs / "model_summary.json").is_file()
    assert (outputs / "metrics.jsonl").is_file()
    assert (outputs / "final_metrics.json").is_file()
    assert (outputs / "best_metrics.json").is_file()
    assert (outputs / "models" / "best_epoch_model.pt").is_file()
    final_metrics = json.loads((outputs / "final_metrics.json").read_text())
    best_metrics = json.loads((outputs / "best_metrics.json").read_text())
    assert "val/raw_dice" in final_metrics
    assert "val/filtered_dice" in final_metrics
    assert "val/filtered_iou" in final_metrics
    assert "val/filtered_precision" in final_metrics
    assert "val/filtered_recall" in final_metrics
    assert "val/raw_contrail_connectivity" in final_metrics
    assert "val/filtered_contrail_connectivity" in final_metrics
    assert best_metrics["selection_metric"] == "val/filtered_dice"

    evaluation = evaluate_run(run.run_dir, max_artifact_samples=1)
    assert evaluation.status == "completed"
    aggregate = json.loads((evaluation.evaluation_dir / "aggregate_metrics.json").read_text())
    assert "raw/dice" in aggregate["metrics"]
    assert "raw/iou" in aggregate["metrics"]
    assert "raw/precision" in aggregate["metrics"]
    assert "raw/recall" in aggregate["metrics"]
    assert "filtered/dice" in aggregate["metrics"]
    assert "filtered/iou" in aggregate["metrics"]
    assert "filtered/precision" in aggregate["metrics"]
    assert "filtered/recall" in aggregate["metrics"]
    assert "raw/contrail_connectivity" in aggregate["metrics"]
    assert "filtered/contrail_connectivity" in aggregate["metrics"]
    assert "artifact_filters/removed_pixel_count" in aggregate["metrics"]
