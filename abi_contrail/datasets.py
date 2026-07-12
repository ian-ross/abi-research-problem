"""Trusted ABI Patch dataset loading for GOES ABI Contrail Segmentation.

This module owns the data-layout boundary for candidate training inputs.  The
initial vertical slice supports two zarr layouts seen in planning data:

* MIT-style top-level zarr arrays opened directly with :func:`zarr.open_array`.
* Google-style zarr groups where arrays live under ``inputs`` and ``labels``.

Only GOES ABI channels 1-16 are exposed.  Longitude, latitude, and any other
extra channels in 19-channel training arrays are intentionally not returned to
candidate code.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import numpy as np
import zarr

ABI_PATCH_SHAPE = (16, 256, 256)
CONTRAIL_MASK_SHAPE = (1, 256, 256)
ABI_16CH_CHANNEL_COUNT = 16

ArrayLayout = Literal["mit", "google"]


@dataclass(frozen=True)
class ABIPatchArrays:
    """Opened zarr arrays for ABI Patch inputs and labels."""

    inputs: Any
    labels: Any
    layout: ArrayLayout


def open_mit_abi_patch_arrays(inputs_zarr: str | Path, labels_zarr: str | Path) -> ABIPatchArrays:
    """Open MIT-style top-level zarr arrays.

    MIT fixtures and reprojected scene arrays are arrays at the zarr root, so
    they must be opened with ``zarr.open_array`` rather than as groups.
    """

    return ABIPatchArrays(
        inputs=zarr.open_array(str(inputs_zarr), mode="r"),
        labels=zarr.open_array(str(labels_zarr), mode="r"),
        layout="mit",
    )


def open_google_abi_patch_arrays(inputs_zarr: str | Path, labels_zarr: str | Path) -> ABIPatchArrays:
    """Open Google-style zarr groups containing ``inputs`` and ``labels`` arrays."""

    inputs_group = zarr.open_group(str(inputs_zarr), mode="r")
    labels_group = zarr.open_group(str(labels_zarr), mode="r")
    return ABIPatchArrays(
        inputs=inputs_group["inputs"],
        labels=labels_group["labels"],
        layout="google",
    )


def open_abi_patch_arrays(
    inputs_zarr: str | Path,
    labels_zarr: str | Path,
    *,
    layout: ArrayLayout,
) -> ABIPatchArrays:
    """Open ABI Patch zarr arrays using the explicitly declared source layout."""

    if layout == "mit":
        return open_mit_abi_patch_arrays(inputs_zarr, labels_zarr)
    if layout == "google":
        return open_google_abi_patch_arrays(inputs_zarr, labels_zarr)
    raise ValueError(f"Unsupported ABI Patch zarr layout: {layout!r}")


def collapse_contrail_mask(labels: np.ndarray) -> np.ndarray:
    """Collapse bit-packed label values to a float32 ``[1, H, W]`` Contrail Mask.

    The v0 target is binary semantic segmentation: every nonzero label value is
    positive, including values from overlapping bit planes such as 1, 2, 4, and
    packed/missing-like values such as 255.
    """

    label_array = np.asarray(labels)
    if label_array.ndim != 2:
        raise ValueError(f"Contrail labels must be a 2D [H, W] array, got shape {label_array.shape}")
    return (label_array != 0).astype(np.float32, copy=False)[np.newaxis, :, :]


def abi_16ch_channel_first(inputs: np.ndarray) -> np.ndarray:
    """Return float32 channel-first GOES ABI channels 1-16 from ``[H, W, C]`` input."""

    input_array = np.asarray(inputs)
    if input_array.ndim != 3:
        raise ValueError(f"ABI inputs must be a 3D [H, W, C] array, got shape {input_array.shape}")
    if input_array.shape[-1] < ABI_16CH_CHANNEL_COUNT:
        raise ValueError(
            f"ABI inputs need at least {ABI_16CH_CHANNEL_COUNT} channels, got {input_array.shape[-1]}"
        )
    abi_16ch = input_array[..., :ABI_16CH_CHANNEL_COUNT]
    return np.moveaxis(abi_16ch, -1, 0).astype(np.float32, copy=False)


class ABIPatchDataset:
    """Minimal map-style ABI Patch dataset backed by opened zarr arrays.

    Items are dictionaries with trusted provider-owned tensors:
    ``inputs`` as float32 ``[16, H, W]`` and ``target`` as float32 ``[1, H, W]``.
    For this vertical slice, the backing arrays are expected to be patch stacks:
    inputs ``[N, H, W, C]`` and labels ``[N, H, W]``.  Single-patch arrays
    ``[H, W, C]``/``[H, W]`` are also accepted for tiny smoke fixtures.
    """

    def __init__(self, arrays: ABIPatchArrays) -> None:
        self.arrays = arrays
        input_shape = tuple(arrays.inputs.shape)
        label_shape = tuple(arrays.labels.shape)
        if len(input_shape) not in {3, 4}:
            raise ValueError(f"Expected inputs shape [N,H,W,C] or [H,W,C], got {input_shape}")
        if len(label_shape) not in {2, 3}:
            raise ValueError(f"Expected labels shape [N,H,W] or [H,W], got {label_shape}")
        if (len(input_shape), len(label_shape)) not in {(4, 3), (3, 2)}:
            raise ValueError(f"Input and label ranks do not describe the same patch layout: {input_shape}, {label_shape}")
        if len(input_shape) == 4 and input_shape[0] != label_shape[0]:
            raise ValueError(f"Input/label sample counts differ: {input_shape[0]} != {label_shape[0]}")
        if input_shape[-3:-1] != label_shape[-2:]:
            raise ValueError(f"Input/label spatial shapes differ: {input_shape[-3:-1]} != {label_shape[-2:]}")

    def __len__(self) -> int:
        if len(self.arrays.inputs.shape) == 3:
            return 1
        return int(self.arrays.inputs.shape[0])

    def __getitem__(self, index: int) -> dict[str, np.ndarray]:
        if index < 0:
            index += len(self)
        if index < 0 or index >= len(self):
            raise IndexError(index)

        if len(self.arrays.inputs.shape) == 3:
            inputs = self.arrays.inputs[:]
            labels = self.arrays.labels[:]
        else:
            inputs = self.arrays.inputs[index, :, :, :]
            labels = self.arrays.labels[index, :, :]

        return {
            "inputs": abi_16ch_channel_first(inputs),
            "target": collapse_contrail_mask(labels),
            "source_layout": self.arrays.layout,
        }


def build_abi_patch_dataset(
    inputs_zarr: str | Path,
    labels_zarr: str | Path,
    *,
    layout: ArrayLayout,
) -> ABIPatchDataset:
    """Open zarr inputs/labels and return the minimal ABI Patch dataset."""

    return ABIPatchDataset(open_abi_patch_arrays(inputs_zarr, labels_zarr, layout=layout))


__all__ = [
    "ABI_PATCH_SHAPE",
    "CONTRAIL_MASK_SHAPE",
    "ABI_16CH_CHANNEL_COUNT",
    "ABIPatchArrays",
    "ABIPatchDataset",
    "abi_16ch_channel_first",
    "build_abi_patch_dataset",
    "collapse_contrail_mask",
    "open_abi_patch_arrays",
    "open_google_abi_patch_arrays",
    "open_mit_abi_patch_arrays",
]
