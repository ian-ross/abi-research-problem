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

import random
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import numpy as np
import zarr

ABI_PATCH_SHAPE = (16, 256, 256)
CONTRAIL_MASK_SHAPE = (1, 256, 256)
ABI_16CH_CHANNEL_COUNT = 16

ArrayLayout = Literal["mit", "google"]
ABIDatasetSource = Literal["mit", "google"]
ABISplitName = Literal["train", "validation"]
DEFAULT_SPLIT_SEED = 20260712


@dataclass(frozen=True)
class ABIPatchArrays:
    """Opened zarr arrays for ABI Patch inputs and labels."""

    inputs: Any
    labels: Any
    layout: ArrayLayout


@dataclass(frozen=True)
class ABIPatchIndexRecord:
    """Leakage-safe ABI Patch sample metadata owned by the provider.

    ``sample_index`` identifies an already-materialized patch in Google/MIT patch
    stacks. ``scene_index`` plus ``row``/``col`` identifies a window in a full MIT
    scene, allowing sample loading to slice only that window.
    """

    dataset_source: ABIDatasetSource
    split: ABISplitName
    scene_name: str
    scene_index: int
    goes_time: str | None
    row: int
    col: int
    positive: bool
    sample_index: int | None = None


@dataclass(frozen=True)
class ABIPatchSplitIndex:
    """Train/validation ABI Patch records plus split policy metadata."""

    train: tuple[ABIPatchIndexRecord, ...]
    validation: tuple[ABIPatchIndexRecord, ...]
    data_policy_metadata: dict[str, object]

    @property
    def records(self) -> tuple[ABIPatchIndexRecord, ...]:
        return self.train + self.validation


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


def build_google_abi_patch_index(metadata_rows: Iterable[Mapping[str, object]]) -> ABIPatchSplitIndex:
    """Build Google ABI Patch records while preserving train/validation provenance.

    Google-distributed patches already encode their split in scene/file names
    such as ``train-*`` and ``validation-*``. This function does not reshuffle
    those rows; it records that provenance as the authoritative split.
    """

    train: list[ABIPatchIndexRecord] = []
    validation: list[ABIPatchIndexRecord] = []
    for fallback_index, row in enumerate(metadata_rows):
        scene_name = _string_field(row, "scene_name", "scene", "name", "filename", "path")
        split = _google_split_from_scene_name(scene_name)
        sample_index = _int_field(row, fallback_index, "sample_index", "index", "patch_index")
        record = ABIPatchIndexRecord(
            dataset_source="google",
            split=split,
            scene_name=scene_name,
            scene_index=_int_field(row, sample_index, "scene_index"),
            goes_time=_optional_string_field(row, "goes_time", "time", "timestamp"),
            row=_int_field(row, 0, "row", "y"),
            col=_int_field(row, 0, "col", "column", "x"),
            positive=_bool_field(row, False, "positive", "has_contrail", "is_positive"),
            sample_index=sample_index,
        )
        if split == "train":
            train.append(record)
        else:
            validation.append(record)
    return ABIPatchSplitIndex(
        train=tuple(train),
        validation=tuple(validation),
        data_policy_metadata={
            "dataset_source": "google",
            "split_policy": "respect_google_scene_name_train_validation_provenance",
            "record_count": len(train) + len(validation),
            "train_count": len(train),
            "validation_count": len(validation),
        },
    )


def build_mit_abi_patch_index(
    labels: Any,
    *,
    scene_names: Sequence[str] | None = None,
    goes_times: Sequence[str | None] | None = None,
    val_fraction: float = 0.2,
    seed: int = DEFAULT_SPLIT_SEED,
    patch_size: int = 256,
    stride: int = 256,
) -> ABIPatchSplitIndex:
    """Split MIT scenes as whole scenes, then index 256x256 label windows.

    Positivity is computed from each label window during index construction and
    stored on the record. Dataset item loading can then slice only the indexed
    input/label window rather than loading a whole scene per sample.
    """

    label_shape = tuple(labels.shape)
    if len(label_shape) != 3:
        raise ValueError(f"MIT full-scene labels must have shape [scene,H,W], got {label_shape}")
    scene_count, height, width = label_shape
    if scene_count < 1:
        raise ValueError("cannot index an empty MIT scene array")
    if patch_size < 1 or stride < 1:
        raise ValueError("patch_size and stride must be positive")
    if height < patch_size or width < patch_size:
        raise ValueError(f"MIT scenes must be at least {patch_size}x{patch_size}, got {height}x{width}")

    names = tuple(scene_names) if scene_names is not None else tuple(f"mit-scene-{idx}" for idx in range(scene_count))
    if len(names) != scene_count:
        raise ValueError(f"scene_names length {len(names)} does not match scene count {scene_count}")
    times = tuple(goes_times) if goes_times is not None else tuple(None for _ in range(scene_count))
    if len(times) != scene_count:
        raise ValueError(f"goes_times length {len(times)} does not match scene count {scene_count}")

    train_scene_indices, validation_scene_indices = _deterministic_scene_split(scene_count, val_fraction, seed)
    split_by_scene = {index: "train" for index in train_scene_indices} | {
        index: "validation" for index in validation_scene_indices
    }

    train: list[ABIPatchIndexRecord] = []
    validation: list[ABIPatchIndexRecord] = []
    rows = range(0, height - patch_size + 1, stride)
    cols = range(0, width - patch_size + 1, stride)
    for scene_index in range(scene_count):
        split = split_by_scene[scene_index]
        target = train if split == "train" else validation
        for row in rows:
            for col in cols:
                label_window = np.asarray(labels[scene_index, row : row + patch_size, col : col + patch_size])
                target.append(
                    ABIPatchIndexRecord(
                        dataset_source="mit",
                        split=split,
                        scene_name=names[scene_index],
                        scene_index=scene_index,
                        goes_time=times[scene_index],
                        row=row,
                        col=col,
                        positive=bool(np.any(label_window != 0)),
                        sample_index=None,
                    )
                )

    return ABIPatchSplitIndex(
        train=tuple(train),
        validation=tuple(validation),
        data_policy_metadata={
            "dataset_source": "mit",
            "split_policy": "deterministic_whole_scene_train_validation_split_before_windowing",
            "split_seed": seed,
            "validation_fraction": val_fraction,
            "patch_size": patch_size,
            "stride": stride,
            "train_scenes": [names[index] for index in train_scene_indices],
            "validation_scenes": [names[index] for index in validation_scene_indices],
            "train_count": len(train),
            "validation_count": len(validation),
        },
    )


def _deterministic_scene_split(scene_count: int, val_fraction: float, seed: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    if scene_count < 2:
        raise ValueError("MIT leakage-safe train/validation split requires at least two scenes")
    if not 0.0 < val_fraction < 1.0:
        raise ValueError("val_fraction must be between 0 and 1")
    indices = list(range(scene_count))
    random.Random(seed).shuffle(indices)
    val_count = max(1, round(scene_count * val_fraction))
    if val_count >= scene_count:
        val_count = scene_count - 1
    validation = set(indices[:val_count])
    train = tuple(index for index in range(scene_count) if index not in validation)
    val = tuple(index for index in range(scene_count) if index in validation)
    return train, val


def _string_field(row: Mapping[str, object], *keys: str) -> str:
    value = _optional_string_field(row, *keys)
    if value is None:
        raise ValueError(f"metadata row is missing required string field from {keys}: {row!r}")
    return value


def _optional_string_field(row: Mapping[str, object], *keys: str) -> str | None:
    for key in keys:
        value = row.get(key)
        if value is not None:
            return str(value)
    return None


def _int_field(row: Mapping[str, object], default: int, *keys: str) -> int:
    for key in keys:
        value = row.get(key)
        if value is not None:
            return int(value)
    return int(default)


def _bool_field(row: Mapping[str, object], default: bool, *keys: str) -> bool:
    for key in keys:
        value = row.get(key)
        if value is not None:
            if isinstance(value, str):
                return value.strip().lower() in {"1", "true", "t", "yes", "y"}
            return bool(value)
    return bool(default)


def _google_split_from_scene_name(scene_name: str) -> ABISplitName:
    parts = scene_name.replace("\\", "/").split("/")
    candidates = parts + [Path(scene_name).name]
    for part in candidates:
        lower = part.lower()
        if lower == "train" or lower.startswith("train-") or lower.startswith("train_"):
            return "train"
        if lower in {"validation", "val"} or lower.startswith("validation-") or lower.startswith("validation_"):
            return "validation"
    raise ValueError(f"Google scene name does not encode train/validation provenance: {scene_name!r}")


class ABIPatchDataset:
    """Minimal map-style ABI Patch dataset backed by opened zarr arrays.

    Items are dictionaries with trusted provider-owned tensors:
    ``inputs`` as float32 ``[16, H, W]`` and ``target`` as float32 ``[1, H, W]``.
    For this vertical slice, the backing arrays are expected to be patch stacks:
    inputs ``[N, H, W, C]`` and labels ``[N, H, W]``.  Single-patch arrays
    ``[H, W, C]``/``[H, W]`` are also accepted for tiny smoke fixtures.
    """

    def __init__(
        self,
        arrays: ABIPatchArrays,
        index_records: Sequence[ABIPatchIndexRecord] | None = None,
        *,
        split: ABISplitName | None = None,
    ) -> None:
        self.arrays = arrays
        records = tuple(index_records or ())
        if split is not None:
            records = tuple(record for record in records if record.split == split)
        self.index_records = records
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
        if len(input_shape) == 3 and input_shape[-3:-1] != label_shape[-2:]:
            raise ValueError(f"Input/label spatial shapes differ: {input_shape[-3:-1]} != {label_shape[-2:]}")
        if len(input_shape) == 4 and not self.index_records and input_shape[-3:-1] != label_shape[-2:]:
            raise ValueError(f"Input/label spatial shapes differ: {input_shape[-3:-1]} != {label_shape[-2:]}")

    def __len__(self) -> int:
        if self.index_records:
            return len(self.index_records)
        if len(self.arrays.inputs.shape) == 3:
            return 1
        return int(self.arrays.inputs.shape[0])

    def __getitem__(self, index: int) -> dict[str, np.ndarray]:
        if index < 0:
            index += len(self)
        if index < 0 or index >= len(self):
            raise IndexError(index)

        record = self.index_records[index] if self.index_records else None
        if record is not None:
            if record.sample_index is not None:
                inputs = self.arrays.inputs[record.sample_index, :, :, :]
                labels = self.arrays.labels[record.sample_index, :, :]
            else:
                row_end = record.row + ABI_PATCH_SHAPE[1]
                col_end = record.col + ABI_PATCH_SHAPE[2]
                inputs = self.arrays.inputs[record.scene_index, record.row : row_end, record.col : col_end, :]
                labels = self.arrays.labels[record.scene_index, record.row : row_end, record.col : col_end]
        elif len(self.arrays.inputs.shape) == 3:
            inputs = self.arrays.inputs[:]
            labels = self.arrays.labels[:]
        else:
            inputs = self.arrays.inputs[index, :, :, :]
            labels = self.arrays.labels[index, :, :]

        sample = {
            "inputs": abi_16ch_channel_first(inputs),
            "target": collapse_contrail_mask(labels),
            "source_layout": self.arrays.layout,
        }
        if record is not None:
            sample["metadata"] = {
                "dataset_source": record.dataset_source,
                "split": record.split,
                "scene_name": record.scene_name,
                "scene_index": record.scene_index,
                "goes_time": record.goes_time,
                "row": record.row,
                "col": record.col,
                "positive": record.positive,
            }
        return sample


def build_abi_patch_dataset(
    inputs_zarr: str | Path,
    labels_zarr: str | Path,
    *,
    layout: ArrayLayout,
    index_records: Sequence[ABIPatchIndexRecord] | None = None,
    split: ABISplitName | None = None,
) -> ABIPatchDataset:
    """Open zarr inputs/labels and return the ABI Patch dataset."""

    return ABIPatchDataset(open_abi_patch_arrays(inputs_zarr, labels_zarr, layout=layout), index_records, split=split)


__all__ = [
    "ABI_PATCH_SHAPE",
    "CONTRAIL_MASK_SHAPE",
    "ABI_16CH_CHANNEL_COUNT",
    "ABIDatasetSource",
    "ABIPatchArrays",
    "ABIPatchDataset",
    "ABIPatchIndexRecord",
    "ABIPatchSplitIndex",
    "ABISplitName",
    "abi_16ch_channel_first",
    "build_abi_patch_dataset",
    "build_google_abi_patch_index",
    "build_mit_abi_patch_index",
    "collapse_contrail_mask",
    "open_abi_patch_arrays",
    "open_google_abi_patch_arrays",
    "open_mit_abi_patch_arrays",
]
