from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest
import yaml
import zarr

from abi_contrail.adapters import ABITrainingAdapter, build_spec
from ml_autoresearch.research_problems import ResearchProblemProviderConfig, load_research_problem_provider
from ml_autoresearch.runs import RunStatus, run_candidate_with_research_problem


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


def test_build_spec_declares_training_capability_with_temporary_val_dice_metric() -> None:
    spec = build_spec()

    assert spec.operation_capabilities.training is True
    assert spec.training_adapter is not None
    assert spec.primary_metric == "val/dice"
    assert spec.training_adapter.selection_policy() == ("val/dice", "max")


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
    assert loaded.spec.training_adapter is not None


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
    assert "val/dice" in final_metrics
    assert best_metrics["selection_metric"] == "val/dice"
