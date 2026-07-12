from __future__ import annotations

import numpy as np
import zarr

from abi_contrail.datasets import (
    ABIPatchDataset,
    abi_16ch_channel_first,
    build_abi_patch_dataset,
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


def test_mit_zarr_arrays_are_opened_as_top_level_arrays(tmp_path) -> None:
    inputs_path, labels_path = _write_mit_arrays(tmp_path)

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


def test_build_dataset_runs_against_tiny_local_fixtures_without_data_symlink(tmp_path) -> None:
    inputs_path, labels_path = _write_google_groups(tmp_path)

    dataset = build_abi_patch_dataset(inputs_path, labels_path, layout="google")
    sample = dataset[0]

    assert len(dataset) == 1
    assert sample["inputs"].dtype == np.float32
    assert sample["target"].dtype == np.float32
    assert sample["inputs"].shape == (16, 2, 3)
    assert sample["target"].shape == (1, 2, 3)
