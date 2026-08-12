from __future__ import annotations

import numpy as np
import zarr

from abi_contrail.datasets import (
    ABI_INPUT_MODE_SOURCE_INDICES,
    ABIPatchDataset,
    abi_16ch_channel_first,
    abi_input_channel_first,
    build_abi_patch_dataset,
    build_google_abi_patch_index,
    build_mit_abi_patch_index,
    collapse_contrail_mask,
    open_google_abi_patch_arrays,
    open_mit_abi_patch_arrays,
)


def _patch_inputs() -> np.ndarray:
    values = np.arange(2 * 3 * 19, dtype=np.float32).reshape(2, 3, 19)
    return values[np.newaxis, ...]


def _patch_labels() -> np.ndarray:
    return np.array([[[0, 1, 2], [4, 255, 0]]], dtype=np.uint8)


def _write_mit_arrays(tmp_path) -> tuple[object, object]:
    inputs_path = tmp_path / "mit_inputs.zarr"
    labels_path = tmp_path / "mit_labels.zarr"
    zarr.open_array(str(inputs_path), mode="w", shape=_patch_inputs().shape, dtype="f4")[:] = _patch_inputs()
    zarr.open_array(str(labels_path), mode="w", shape=_patch_labels().shape, dtype="u1")[:] = _patch_labels()
    return inputs_path, labels_path


def _write_google_groups(tmp_path) -> tuple[object, object]:
    inputs_path = tmp_path / "google_inputs.zarr"
    labels_path = tmp_path / "google_labels.zarr"
    inputs_group = zarr.open_group(str(inputs_path), mode="w")
    labels_group = zarr.open_group(str(labels_path), mode="w")
    inputs_group.create_array("inputs", data=_patch_inputs())
    labels_group.create_array("labels", data=_patch_labels())
    return inputs_path, labels_path


def _write_mit_groups(tmp_path) -> tuple[object, object]:
    inputs_path = tmp_path / "mit_group_inputs.zarr"
    labels_path = tmp_path / "mit_group_labels.zarr"
    inputs_group = zarr.open_group(str(inputs_path), mode="w")
    labels_group = zarr.open_group(str(labels_path), mode="w")
    inputs_group.create_array("inputs", data=_patch_inputs())
    labels_group.create_array("labels", data=_patch_labels())
    return inputs_path, labels_path


def test_mit_zarr_arrays_are_opened_as_top_level_arrays(tmp_path) -> None:
    inputs_path, labels_path = _write_mit_arrays(tmp_path)

    arrays = open_mit_abi_patch_arrays(inputs_path, labels_path)
    dataset = ABIPatchDataset(arrays)
    sample = dataset[0]

    assert arrays.layout == "mit"
    assert sample["source_layout"] == "mit"
    assert sample["inputs"].shape == (16, 2, 3)
    assert sample["target"].shape == (1, 2, 3)


def test_mit_zarr_groups_are_opened_through_named_arrays(tmp_path) -> None:
    inputs_path, labels_path = _write_mit_groups(tmp_path)

    arrays = open_mit_abi_patch_arrays(inputs_path, labels_path)
    dataset = ABIPatchDataset(arrays)
    sample = dataset[0]

    assert arrays.layout == "mit"
    assert sample["source_layout"] == "mit"
    assert sample["inputs"].shape == (16, 2, 3)
    assert sample["target"].shape == (1, 2, 3)


def test_google_zarr_groups_are_opened_through_named_arrays(tmp_path) -> None:
    inputs_path, labels_path = _write_google_groups(tmp_path)

    arrays = open_google_abi_patch_arrays(inputs_path, labels_path)
    dataset = ABIPatchDataset(arrays)
    sample = dataset[0]

    assert arrays.layout == "google"
    assert sample["source_layout"] == "google"
    assert sample["inputs"].shape == (16, 2, 3)
    assert sample["target"].shape == (1, 2, 3)


def test_labels_0_1_2_4_and_255_collapse_to_binary_contrail_mask() -> None:
    labels = np.array([[0, 1, 2], [4, 255, 0]], dtype=np.uint8)

    mask = collapse_contrail_mask(labels)

    np.testing.assert_array_equal(mask, np.array([[[0, 1, 1], [1, 1, 0]]], dtype=np.float32))
    assert mask.dtype == np.float32


def test_inputs_are_float32_channel_first_abi_16ch_without_extra_channels() -> None:
    channel_last = np.arange(2 * 3 * 19, dtype=np.float64).reshape(2, 3, 19)

    channel_first = abi_16ch_channel_first(channel_last)

    assert channel_first.shape == (16, 2, 3)
    assert channel_first.dtype == np.float32
    np.testing.assert_array_equal(channel_first[0], channel_last[:, :, 0].astype(np.float32))
    np.testing.assert_array_equal(channel_first[15], channel_last[:, :, 15].astype(np.float32))


def test_input_modes_select_exact_channel_mappings_and_never_lon_lat() -> None:
    channel_last = np.arange(2 * 3 * 19, dtype=np.float32).reshape(2, 3, 19)

    expected_shapes = {
        "abi_16ch": (16, 2, 3),
        "abi_16ch_plus_sza": (17, 2, 3),
        "abi_thermal_10ch": (10, 2, 3),
    }
    for input_mode, source_indices in ABI_INPUT_MODE_SOURCE_INDICES.items():
        channel_first = abi_input_channel_first(channel_last, input_mode)

        assert channel_first.shape == expected_shapes[input_mode]
        assert 16 not in source_indices
        assert 17 not in source_indices
        for output_index, source_index in enumerate(source_indices):
            np.testing.assert_array_equal(channel_first[output_index], channel_last[:, :, source_index])


def test_input_mode_dataset_selection_is_provider_owned() -> None:
    channel_last = np.arange(2 * 3 * 19, dtype=np.float32).reshape(2, 3, 19)
    labels = np.zeros((2, 3), dtype=np.uint8)
    arrays = type("Arrays", (), {"inputs": channel_last, "labels": labels, "layout": "google"})()

    dataset = ABIPatchDataset(arrays, input_mode="abi_thermal_10ch")
    sample = dataset[0]

    assert sample["input_mode"] == "abi_thermal_10ch"
    assert sample["inputs"].shape == (10, 2, 3)
    np.testing.assert_array_equal(sample["inputs"][0], channel_last[:, :, 6])
    np.testing.assert_array_equal(sample["inputs"][-1], channel_last[:, :, 15])


def test_explicit_empty_index_does_not_fall_back_to_all_backing_array_records(tmp_path) -> None:
    inputs_path, labels_path = _write_google_groups(tmp_path)
    arrays = open_google_abi_patch_arrays(inputs_path, labels_path)

    dataset = ABIPatchDataset(arrays, ())

    assert len(dataset) == 0


def test_build_dataset_runs_against_tiny_local_fixtures_without_data_symlink(tmp_path) -> None:
    inputs_path, labels_path = _write_google_groups(tmp_path)

    dataset = build_abi_patch_dataset(inputs_path, labels_path, layout="google")
    sample = dataset[0]

    assert len(dataset) == 1
    assert sample["inputs"].dtype == np.float32
    assert sample["target"].dtype == np.float32
    assert sample["inputs"].shape == (16, 2, 3)
    assert sample["target"].shape == (1, 2, 3)


def test_google_index_respects_train_validation_scene_name_provenance() -> None:
    split_index = build_google_abi_patch_index(
        [
            {"scene_name": "train-00042/patch.zarr", "sample_index": 7, "row": 0, "col": 0, "positive": True},
            {"scene_name": "validation-00009/patch.zarr", "sample_index": 8, "row": 256, "col": 0},
        ]
    )

    assert [record.scene_name for record in split_index.train] == ["train-00042/patch.zarr"]
    assert [record.scene_name for record in split_index.validation] == ["validation-00009/patch.zarr"]
    assert split_index.train[0].split == "train"
    assert split_index.validation[0].split == "validation"
    assert split_index.data_policy_metadata["split_policy"] == "respect_google_scene_name_train_validation_provenance"


def test_mit_index_splits_whole_scenes_before_windowing_and_records_metadata(tmp_path) -> None:
    labels_path = tmp_path / "mit_full_scene_labels.zarr"
    labels = zarr.open_array(str(labels_path), mode="w", shape=(4, 512, 512), dtype="u1")
    labels[:] = 0
    labels[0, 0:256, 0:256] = 1

    split_index = build_mit_abi_patch_index(
        labels,
        scene_names=["scene-a", "scene-b", "scene-c", "scene-d"],
        goes_times=["t0", "t1", "t2", "t3"],
        val_fraction=0.5,
        seed=11,
    )

    train_scenes = {record.scene_name for record in split_index.train}
    validation_scenes = {record.scene_name for record in split_index.validation}
    assert train_scenes
    assert validation_scenes
    assert train_scenes.isdisjoint(validation_scenes)
    assert {record.scene_name for record in split_index.records} == {"scene-a", "scene-b", "scene-c", "scene-d"}
    assert all((record.row, record.col) in {(0, 0), (0, 256), (256, 0), (256, 256)} for record in split_index.records)
    assert any(record.positive for record in split_index.records if record.scene_name == "scene-a")
    assert split_index.data_policy_metadata["split_policy"] == "deterministic_whole_scene_train_validation_split_before_windowing"


def test_mit_windowed_dataset_uses_index_records_for_256_by_256_samples(tmp_path) -> None:
    inputs_path = tmp_path / "mit_full_scene_inputs.zarr"
    labels_path = tmp_path / "mit_full_scene_labels.zarr"
    inputs = zarr.open_array(str(inputs_path), mode="w", shape=(2, 512, 512, 19), dtype="f4")
    labels = zarr.open_array(str(labels_path), mode="w", shape=(2, 512, 512), dtype="u1")
    inputs[:] = 0
    labels[:] = 0
    inputs[1, 256:512, 0:256, 0] = 5
    labels[1, 256:512, 0:256] = 2

    arrays = open_mit_abi_patch_arrays(inputs_path, labels_path)
    split_index = build_mit_abi_patch_index(labels, scene_names=["scene-a", "scene-b"], val_fraction=0.5, seed=1)
    target_record = next(record for record in split_index.records if record.scene_index == 1 and record.row == 256 and record.col == 0)
    dataset = ABIPatchDataset(arrays, [target_record])
    sample = dataset[0]

    assert sample["inputs"].shape == (16, 256, 256)
    assert sample["target"].shape == (1, 256, 256)
    assert sample["inputs"][0, 0, 0] == 5
    assert sample["target"].sum() == 256 * 256
    assert sample["metadata"]["scene_name"] == "scene-b"
    assert sample["metadata"]["row"] == 256
    assert sample["metadata"]["positive"] is True
