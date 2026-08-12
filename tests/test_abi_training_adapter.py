from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import yaml
import torch
import zarr

import abi_contrail.adapters as adapters_module
from abi_contrail.adapters import (
    ABITrainingAdapter,
    AUGMENTATION_POLICY_RANDOM_MIRRORING,
    _RandomMirroringDataset,
    build_spec,
    derive_auxiliary_target,
    source_balanced_sampling_weights,
)
from abi_contrail.datasets import ABIPatchArrays, ABIPatchIndexRecord, ABIPatchSplitIndex
from abi_contrail.evaluation import _evaluation_data_config
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


def _write_google_selection_fixture(root: Path) -> dict[str, object]:
    root.mkdir()
    inputs_path = root / "inputs.zarr"
    labels_path = root / "labels.zarr"
    inputs_group = zarr.open_group(str(inputs_path), mode="w")
    labels_group = zarr.open_group(str(labels_path), mode="w")
    inputs_group.create_array("inputs", data=np.zeros((8, 2, 2, 19), dtype=np.float32))
    labels_group.create_array("labels", data=np.zeros((8, 2, 2), dtype=np.uint8))
    metadata_rows = []
    for sample_index in range(8):
        split = "train" if sample_index < 4 else "validation"
        metadata_rows.append(
            {
                "scene_name": f"{split}-provenance-{sample_index}/patch.zarr",
                "sample_index": sample_index,
                "positive": sample_index % 2 == 0,
            }
        )
    return {
        "dataset_root": str(root),
        "layout": "google",
        "inputs_zarr": "inputs.zarr",
        "labels_zarr": "labels.zarr",
        "metadata_rows": metadata_rows,
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


def test_training_adapter_consumes_named_training_root(tmp_path: Path) -> None:
    data_config = _write_google_fixture(tmp_path / "fixture")
    training_root = Path(str(data_config.pop("dataset_root")))
    ancillary_root = tmp_path / "ancillary"
    ancillary_root.mkdir()
    data_config["data_roots"] = {
        "training": str(training_root),
        "ancillary": str(ancillary_root),
    }
    adapter = ABITrainingAdapter()

    root = adapter.validate_data_root(data_config)
    datasets = adapter.build_datasets(
        data_config=data_config,
        resolved_manifest_path=tmp_path / "resolved.yaml",
    )

    assert root == training_root.resolve()
    assert len(datasets.train_dataset) == 1
    assert len(datasets.validation_dataset) == 1
    assert datasets.train_dataset[0][0].shape[0] == 16


def test_training_adapter_loads_google_split_metadata_from_trusted_parquet(tmp_path: Path) -> None:
    data_config = _write_google_fixture(tmp_path / "fixture")
    metadata_rows = data_config.pop("metadata_rows")
    metadata_path = tmp_path / "fixture" / "metadata.parquet"
    pd.DataFrame(
        [
            {"scene": "train-000", "contrail_pixels": 12, "goes_time": "2020-01-01 00:00"},
            {"scene": "validation-000", "contrail_pixels": 0, "goes_time": "2020-01-01 00:10"},
        ]
    ).to_parquet(metadata_path)
    data_config["metadata_parquet"] = "metadata.parquet"
    adapter = ABITrainingAdapter()

    datasets = adapter.build_datasets(data_config=data_config, resolved_manifest_path=tmp_path / "resolved.yaml")

    assert len(datasets.train_dataset) == 1
    assert len(datasets.validation_dataset) == 1
    assert datasets.train_dataset.sample_metadata(0)["scene_name"] == metadata_rows[0]["scene_name"].split("/")[0]
    assert datasets.train_dataset.sample_metadata(0)["positive"] is True
    assert datasets.validation_dataset.sample_metadata(0)["positive"] is False


def test_training_adapter_records_bounded_selection_metadata_per_source_and_split(tmp_path: Path) -> None:
    data_config = _write_google_selection_fixture(tmp_path / "fixture")

    datasets = ABITrainingAdapter().build_datasets(
        data_config=data_config,
        resolved_manifest_path=tmp_path / "resolved.yaml",
        max_samples=2,
    )

    assert len(datasets.train_dataset) == 2
    assert len(datasets.validation_dataset) == 2
    bounded = datasets.data_policy_metadata["bounded_record_selection"]
    assert bounded["requested_cap_per_source_split"] == 2
    assert bounded["cap_scope"] == "independent_per_dataset_source_and_leakage_safe_split"
    assert bounded["policy_name"] == "abi_representative_scene_positive_hash"
    source = bounded["source_split_selections"][0]
    assert source["dataset_source"] == "google"
    for split in ("train", "validation"):
        summary = source["splits"][split]
        assert summary["available_count"] == 4
        assert summary["selected_count"] == 2
        assert summary["selected_positive_count"] == 1
        assert summary["selected_negative_count"] == 1
        assert len(summary["selected_record_identity_sha256"]) == 64
        assert "records" not in summary


def test_combined_adapter_keeps_selection_audits_isolated_by_source_and_split(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "fixture"
    root.mkdir()
    for name in ("mit-inputs", "mit-labels", "google-inputs", "google-labels"):
        (root / name).touch()
    data_config = {
        "dataset_root": str(root),
        "sources": [
            {"layout": "mit", "inputs_zarr": "mit-inputs", "labels_zarr": "mit-labels"},
            {"layout": "google", "inputs_zarr": "google-inputs", "labels_zarr": "google-labels"},
        ],
    }

    def fake_arrays(_inputs: Path, _labels: Path, *, layout: str) -> ABIPatchArrays:
        return ABIPatchArrays(
            inputs=np.zeros((8, 2, 2, 19), dtype=np.float32),
            labels=np.zeros((8, 2, 2), dtype=np.uint8),
            layout=layout,  # type: ignore[arg-type]
        )

    def fake_split_index(_labels: object, *, root: Path, layout: str, data_config: object) -> ABIPatchSplitIndex:
        del root, data_config

        def records(split: str) -> tuple[ABIPatchIndexRecord, ...]:
            offset = 0 if split == "train" else 4
            return tuple(
                ABIPatchIndexRecord(
                    dataset_source=layout,  # type: ignore[arg-type]
                    split=split,  # type: ignore[arg-type]
                    scene_name=f"{layout}-{split}-scene-{index}",
                    scene_index=index,
                    goes_time=None,
                    row=0,
                    col=0,
                    positive=index % 2 == 0,
                    sample_index=offset + index if layout == "google" else None,
                )
                for index in range(4)
            )

        return ABIPatchSplitIndex(
            train=records("train"),
            validation=records("validation"),
            data_policy_metadata={"dataset_source": layout, "split_policy": f"trusted-{layout}"},
        )

    monkeypatch.setattr(adapters_module, "open_abi_patch_arrays", fake_arrays)
    adapter = ABITrainingAdapter()
    monkeypatch.setattr(adapter, "_build_split_index", fake_split_index)

    datasets = adapter.build_datasets(
        data_config=data_config,
        resolved_manifest_path=tmp_path / "resolved.yaml",
        max_samples=2,
    )

    assert len(datasets.train_dataset) == 4
    assert len(datasets.validation_dataset) == 4
    assert datasets.data_policy_metadata["dataset_source"] == "combined"
    assert {policy["dataset_source"] for policy in datasets.data_policy_metadata["source_split_policies"]} == {
        "mit",
        "google",
    }
    selections = datasets.data_policy_metadata["bounded_record_selection"]["source_split_selections"]
    assert {selection["dataset_source"] for selection in selections} == {"mit", "google"}
    for selection in selections:
        assert set(selection["splits"]) == {"train", "validation"}
        assert all(summary["selected_count"] == 2 for summary in selection["splits"].values())


def test_training_adapter_logs_sampling_policy_metadata(tmp_path: Path) -> None:
    data_config = _write_google_fixture(tmp_path / "fixture")
    data_config["positive_patch_preference"] = 3.0
    data_config["source_mixture"] = {"mit": 1, "google": 2}
    adapter = ABITrainingAdapter(data_config)

    datasets = adapter.build_datasets(data_config=data_config, resolved_manifest_path=tmp_path / "resolved.yaml")

    assert datasets.data_policy_metadata["sampling_policy_owner"] == "provider/harness"
    assert datasets.data_policy_metadata["positive_patch_preference"] == 3.0
    assert datasets.data_policy_metadata["source_mixture"] == {"mit": 1 / 3, "google": 2 / 3}
    assert "combined_source_balanced" in datasets.data_policy_metadata["available_sampling_policies"]


def test_training_adapter_wraps_only_selected_random_mirroring_policy() -> None:
    class TinyDataset:
        def __len__(self) -> int:
            return 1

        def __getitem__(self, index: int):
            return torch.zeros((1, 2, 2)), torch.zeros((1, 2, 2))

    adapter = ABITrainingAdapter()
    dataset = TinyDataset()

    assert adapter.apply_augmentation_policy(dataset, "none") is dataset
    wrapped = adapter.apply_augmentation_policy(dataset, AUGMENTATION_POLICY_RANDOM_MIRRORING)

    assert isinstance(wrapped, _RandomMirroringDataset)


def test_random_mirroring_flips_inputs_and_targets_consistently_for_all_modes() -> None:
    image = torch.tensor(
        [
            [[1, 2, 3], [4, 5, 6]],
            [[7, 8, 9], [10, 11, 12]],
        ],
        dtype=torch.float32,
    )
    mask = torch.tensor([[[0, 1, 2], [3, 4, 5]]], dtype=torch.float32)

    class TinyDataset:
        modes = ("none", "horizontal", "vertical", "both")

        def __len__(self) -> int:
            return len(self.modes)

        def __getitem__(self, index: int):
            return image.clone(), mask.clone()

    mirrored = _RandomMirroringDataset(TinyDataset(), flip_selector=lambda index: TinyDataset.modes[index])

    expected = {
        "none": (image, mask),
        "horizontal": (torch.flip(image, dims=[-1]), torch.flip(mask, dims=[-1])),
        "vertical": (torch.flip(image, dims=[-2]), torch.flip(mask, dims=[-2])),
        "both": (torch.flip(image, dims=[-2, -1]), torch.flip(mask, dims=[-2, -1])),
    }
    for index, mode in enumerate(TinyDataset.modes):
        augmented_image, augmented_mask = mirrored[index]
        expected_image, expected_mask = expected[mode]
        assert torch.equal(augmented_image, expected_image)
        assert torch.equal(augmented_mask, expected_mask)


def test_random_mirroring_uses_torch_seed_for_default_selector() -> None:
    class TinyDataset:
        def __len__(self) -> int:
            return 1

        def __getitem__(self, index: int):
            image = torch.arange(4, dtype=torch.float32).reshape(1, 2, 2)
            return image, image.clone()

    mirrored = _RandomMirroringDataset(TinyDataset())
    torch.manual_seed(12345)
    first = mirrored[0]
    torch.manual_seed(12345)
    second = mirrored[0]

    assert torch.equal(first[0], second[0])
    assert torch.equal(first[1], second[1])


def test_source_aware_sampling_weights_filter_and_balance_sources() -> None:
    metadata = [
        {"dataset_source": "mit", "positive": False},
        {"dataset_source": "mit", "positive": True},
        {"dataset_source": "google", "positive": False},
        {"dataset_source": "google", "positive": False},
        {"dataset_source": "google", "positive": True},
    ]

    mit_only = source_balanced_sampling_weights(metadata, sampling_policy="mit_only")
    google_only = source_balanced_sampling_weights(metadata, sampling_policy="google_only")
    combined = source_balanced_sampling_weights(
        metadata,
        sampling_policy="combined_source_balanced",
        positive_patch_preference=4.0,
        source_mixture={"mit": 0.25, "google": 0.75},
    )

    assert mit_only[0] > 0
    assert mit_only[1] > 0
    assert mit_only[2:] == (0.0, 0.0, 0.0)
    assert google_only[:2] == (0.0, 0.0)
    assert sum(google_only[2:]) == pytest.approx(1.0)
    assert sum(combined[:2]) == pytest.approx(0.25)
    assert sum(combined[2:]) == pytest.approx(0.75)
    assert combined[1] > combined[0]
    assert combined[4] > combined[2]


def test_training_adapter_builds_provider_owned_source_sampler() -> None:
    class IndexDataset:
        metadata = [
            {"dataset_source": "mit", "positive": False},
            {"dataset_source": "mit", "positive": True},
            {"dataset_source": "google", "positive": True},
        ]

        def __len__(self) -> int:
            return len(self.metadata)

        def __getitem__(self, index: int):
            return torch.tensor([index]), torch.tensor([0.0])

        def sample_metadata(self, index: int) -> dict[str, object]:
            return dict(self.metadata[index])

    adapter = ABITrainingAdapter({"positive_patch_preference": 2.0})
    loader = adapter.data_loader_for_sampling(IndexDataset(), batch_size=1, sampling_policy="mit_only", loader_kwargs={})

    sampled_indices = [int(inputs.item()) for inputs, _target in loader]
    assert sampled_indices
    assert set(sampled_indices) <= {0, 1}


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


def test_validation_metrics_are_dataset_source_stratified() -> None:
    class ValidationDataset:
        metadata = (
            {"dataset_source": "mit", "scene_name": "mit-scene", "scene_index": 0, "goes_time": "2020-01-01T00:00:00Z", "row": 0, "col": 0},
            {"dataset_source": "google", "scene_name": "validation-google", "scene_index": 1, "goes_time": "2020-01-01T00:10:00Z", "row": 0, "col": 0},
        )

        def sample_metadata(self, index: int) -> dict[str, object]:
            return dict(self.metadata[index])

        def filter_context(self, index: int) -> dict[str, object]:
            return {}

    logits = torch.full((2, 1, 4, 4), -10.0)
    target = torch.zeros((2, 1, 4, 4), dtype=torch.float32)
    target[:, :, 1:3, 1:3] = 1.0
    logits[0, :, 1:3, 1:3] = 10.0
    metrics = ABITrainingAdapter().compute_validation_metrics_from_dataset(logits, target, ValidationDataset())

    assert "val/source/mit/raw_dice" in metrics
    assert "val/source/google/raw_dice" in metrics
    assert "val/source/mit/filtered_dice" in metrics
    assert "val/source/google/filtered_dice" in metrics
    assert metrics["val/source/mit/raw_dice"] > metrics["val/source/google/raw_dice"]


def test_accelerated_validation_result_preserves_source_metrics_and_reports_bounded_cpu_work(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class ValidationDataset:
        metadata = (
            {"dataset_source": "mit"},
            {"dataset_source": "google"},
        )

        def sample_metadata(self, index: int) -> dict[str, object]:
            return dict(self.metadata[index])

        def filter_context(self, index: int) -> dict[str, object]:
            return {}

    logits = torch.full((2, 1, 4, 4), -10.0)
    target = torch.zeros((2, 1, 4, 4), dtype=torch.float32)
    target[:, :, 1:3, 1:3] = 1.0
    logits[0, :, 1:3, 1:3] = 10.0
    adapter = ABITrainingAdapter({"postprocessing_batch_size": 1})
    expected = adapter.compute_validation_metrics_from_dataset(logits, target, ValidationDataset())

    class AcceleratedOnlyPipeline:
        filters = adapter.filter_pipeline.filters
        pixel_area_km2 = adapter.filter_pipeline.pixel_area_km2

    adapter.filter_pipeline = AcceleratedOnlyPipeline()  # type: ignore[assignment]
    messages: list[str] = []

    result = adapter.compute_validation_result_from_dataset(
        logits,
        target,
        ValidationDataset(),
        device=torch.device("cpu"),
        progress_callback=messages.append,
    )

    assert result.metrics == pytest.approx(expected)
    assert result.report["backend"] == "torch_cpu"
    assert result.report["requested_device"] == "cpu"
    assert result.report["batch_size"] == 1
    assert result.report["max_device_batch_samples"] == 1
    assert result.report["bounded_device_batches"] is True
    assert result.report["full_validation_gpu_residency"] is False
    assert set(result.report["timings_seconds"]) == {
        "artifact_filter_context_preparation",
        "artifact_filter",
        "ordinary_metric",
        "connectivity_metric",
    }
    assert any(message.startswith("Artifact Filter context preparation started") for message in messages)
    assert any(message.startswith("connectivity metric phase complete") for message in messages)

    monkeypatch.setattr(torch.cuda, "is_available", lambda: False)
    fallback = adapter.compute_validation_result_from_dataset(
        logits,
        target,
        ValidationDataset(),
        device=torch.device("cuda"),
        progress_callback=lambda _message: None,
    )
    assert fallback.report["requested_device"] == "cuda"
    assert fallback.report["backend"] == "torch_cpu"
    assert fallback.metrics == pytest.approx(expected)


def test_accelerated_source_metrics_preserve_geographic_then_scanline_filter_order() -> None:
    from abi_contrail.artifact_filters import (
        ABIArtifactFilterPipeline,
        GeographicFeatureFilter,
        ScanlineArtifactFilter,
    )

    class ValidationDataset:
        sources = ("mit", "google")
        geographic_masks = (
            np.array([[False, False, False, False, False, True, False, False, False, False]]),
            np.zeros((1, 10), dtype=bool),
        )

        def sample_metadata(self, index: int) -> dict[str, object]:
            return {"dataset_source": self.sources[index]}

        def filter_context(self, index: int) -> dict[str, object]:
            return {"geographic_feature_mask": self.geographic_masks[index]}

    probabilities = torch.stack(
        (
            torch.full((1, 1, 10), 0.7),
            torch.linspace(0.55, 0.95, 10).reshape(1, 1, 10),
        )
    )
    logits = torch.logit(probabilities)
    target = torch.ones_like(logits)
    adapter = ABITrainingAdapter({"postprocessing_batch_size": 2})
    adapter.filter_pipeline = ABIArtifactFilterPipeline(
        filters=(
            GeographicFeatureFilter(pixel_buffer=0),
            ScanlineArtifactFilter(min_length_pixels=8, max_probability_std=0.01),
        ),
        pixel_area_km2=1.0,
    )
    expected = adapter.compute_validation_metrics_from_dataset(logits, target, ValidationDataset())

    result = adapter.compute_validation_result_from_dataset(
        logits,
        target,
        ValidationDataset(),
        device=torch.device("cpu"),
        progress_callback=lambda _message: None,
    )

    assert result.metrics == pytest.approx(expected)
    assert result.metrics["val/source/mit/filtered_dice"] > 0.9
    assert result.metrics["val/source/google/filtered_dice"] == pytest.approx(1.0)


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
    baselines = spec.evaluation_adapter.baseline_segmenters()
    assert {baseline["name"] for baseline in baselines} == {"mcast_detection_1_1", "mcast_detection_2_1"}
    assert all(baseline["artifact_filters"] == "provider_owned_same_pipeline_as_candidates" for baseline in baselines)


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


def test_evaluation_config_preserves_container_named_ancillary_root(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    (run_dir / "run_metadata.json").write_text(
        json.dumps(
            {
                "dataset": {
                    "layout": "google",
                    "inputs_zarr": "google/inputs.zarr",
                    "labels_zarr": "google/labels.zarr",
                }
            }
        )
    )

    config = _evaluation_data_config(
        run_dir,
        Path("/data/training"),
        base_config={
            "data_roots": {
                "training": "/host/training",
                "ancillary": "/data/ancillary",
            },
            "geographic_ancillary_manifest": "natural-earth/manifest.json",
        },
    )

    assert config["data_roots"] == {
        "training": "/data/training",
        "ancillary": "/data/ancillary",
    }
    assert config["geographic_ancillary_manifest"] == "natural-earth/manifest.json"


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
    training_root = Path(str(data_config.pop("dataset_root")))
    ancillary_root = tmp_path / "ancillary"
    ancillary_root.mkdir()
    candidate = _write_minimal_candidate(tmp_path)
    provider_config = ResearchProblemProviderConfig(
        id="goes_abi_contrail_segmentation",
        expected_contract_version="v0",
        package_root=Path("."),
        provider_target="abi_contrail.research_problem:build_spec",
        data_config=data_config,
        data_roots={"training": training_root, "ancillary": ancillary_root},
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
    bounded_selection = final_metrics["data_policy"]["bounded_record_selection"]
    assert bounded_selection["requested_cap_per_source_split"] == 1
    assert bounded_selection["source_split_selections"][0]["splits"]["train"]["selected_count"] == 1
    run_metadata = json.loads((run.run_dir / "run_metadata.json").read_text())
    assert run_metadata["data_policy"]["bounded_record_selection"] == bounded_selection
    assert best_metrics["selection_metric"] == "val/filtered_dice"
    validation_index = json.loads((outputs / "validation_postprocessing" / "index.json").read_text())
    validation_report = json.loads((outputs / "validation_postprocessing" / "epoch_001.json").read_text())
    assert validation_index["reports"] == ["outputs/validation_postprocessing/epoch_001.json"]
    expected_backend = "torch_cuda" if final_metrics["hardware/device"] == "cuda" else "torch_cpu"
    assert validation_report["postprocessing"]["backend"] == expected_backend
    assert validation_report["postprocessing"]["bounded_device_batches"] is True
    assert validation_report["postprocessing"]["max_device_batch_samples"] == 1
    training_log = (outputs / "logs" / "training.log").read_text()
    assert "validation inference complete" in training_log
    assert "Artifact Filter context preparation complete" in training_log
    assert "connectivity metric phase complete" in training_log

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
    assert "source/google/raw/dice" in aggregate["metrics"]
    assert "source/google/filtered/dice" in aggregate["metrics"]
    assert "artifact_filters/removed_pixel_count" in aggregate["metrics"]
    per_sample_record = json.loads((evaluation.evaluation_dir / "per_sample_metrics.jsonl").read_text().splitlines()[0])
    assert per_sample_record["Dataset Source"] == "google"
    assert per_sample_record["scene_name"] == "validation-000/patch.zarr"
