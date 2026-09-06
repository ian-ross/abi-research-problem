from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import xarray as xr
import zarr
from pyproj import CRS

from abi_contrail.temporal import GOES16ConusScene
from abi_contrail.temporal_cli import provision_temporal_frames


def _write_google_fixture(root: Path) -> dict[str, object]:
    root.mkdir()
    inputs_group = zarr.open_group(str(root / "inputs.zarr"), mode="w")
    labels_group = zarr.open_group(str(root / "labels.zarr"), mode="w")
    inputs = np.zeros((2, 256, 256, 19), dtype=np.float32)
    rows, cols = np.indices((256, 256))
    for index in range(2):
        inputs[index, :, :, 16] = cols
        inputs[index, :, :, 17] = rows
    inputs_group.create_array("inputs", data=inputs)
    labels_group.create_array("labels", data=np.zeros((2, 256, 256), dtype=np.uint8))
    return {
        "dataset_root": str(root),
        "temporal_cache": str(root / "temporal-cache"),
        "layout": "google",
        "inputs_zarr": "inputs.zarr",
        "labels_zarr": "labels.zarr",
        "metadata_rows": [
            {"scene_name": "train-000/patch.zarr", "sample_index": 0, "goes_time": "2020-01-01T00:05:00Z", "positive": False, "location": _location()},
            {"scene_name": "validation-000/patch.zarr", "sample_index": 1, "goes_time": "2020-01-01T00:10:00Z", "positive": False, "location": _location()},
        ],
    }


def _location() -> dict[str, object]:
    return {
        "projection_wkt": CRS.from_epsg(4326).to_wkt(),
        "col_min": 0.0,
        "row_min": 0.0,
        "col_size": 1.0,
        "row_size": 1.0,
    }


def _dt(minute: int) -> datetime:
    return datetime(2020, 1, 1, 0, minute, tzinfo=timezone.utc)


def _scenes(*, keys: tuple[str, ...] | None = None) -> tuple[GOES16ConusScene, ...]:
    scene_keys = keys or tuple(f"s3://noaa-goes16/ABI-L2-MCMIPC/2020/001/00/scene-{index}.nc" for index in range(4))
    return tuple(
        GOES16ConusScene(
            key=scene_keys[index],
            time_coverage_start=_dt(index * 5),
            time_coverage_end=_dt(index * 5 + 1),
            canonical_scene_time=_dt(index * 5),
            filename_scene_time=None,
        )
        for index in range(len(scene_keys))
    )


def _write_regular_scene(path: Path, *, base: float) -> None:
    y = np.arange(256, dtype=np.float32)
    x = np.arange(256, dtype=np.float32)
    rows, cols = np.indices((256, 256))
    data_vars = {"spatial_ref": xr.DataArray(0, attrs={"crs_wkt": CRS.from_epsg(4326).to_wkt()})}
    for channel in range(1, 17):
        data_vars[f"CMI_C{channel:02d}"] = (("y", "x"), (base + channel + rows * 0 + cols * 0).astype(np.float32))
    xr.Dataset(
        data_vars=data_vars,
        coords={"x": x, "y": y},
        attrs={"time_coverage_start": "2020-01-01T00:00:00Z", "time_coverage_end": "2020-01-01T00:01:00Z"},
    ).to_netcdf(path)


def test_provision_temporal_frames_writes_full_eligibility_manifest_for_configured_snapshot(tmp_path: Path) -> None:
    data_config = _write_google_fixture(tmp_path / "fixture")
    Path(str(data_config["temporal_cache"])).mkdir()

    report = provision_temporal_frames(data_config=data_config, offsets=(-1, 0, 1), scenes=_scenes())

    manifest_path = Path(str(report["eligibility_manifest"]))
    manifest = json.loads(manifest_path.read_text())
    assert report["status"] == "eligibility_manifest_written"
    assert manifest["full_dataset_scan"] is True
    assert manifest["summary"]["scanned_record_count"] == 2
    assert manifest["summary"]["eligible_record_count"] == 2
    assert manifest["dataset_scope"]["record_count"] == 2
    assert len(manifest["dataset_scope"]["record_identity_sha256"]) == 64
    assert [record["split"] for record in manifest["records"]] == ["train", "validation"]


def test_provision_temporal_frames_extracts_non_zero_patches_and_writes_cache_manifest(tmp_path: Path) -> None:
    data_config = _write_google_fixture(tmp_path / "fixture")
    temporal_root = Path(str(data_config["temporal_cache"]))
    temporal_root.mkdir()
    scene_paths = tuple(str(tmp_path / f"scene-{index}.nc") for index in range(3))
    for index, scene_path in enumerate(scene_paths):
        _write_regular_scene(Path(scene_path), base=index * 1000.0)

    report = provision_temporal_frames(
        data_config=data_config,
        offsets=(-1, 0, 1),
        scenes=_scenes(keys=scene_paths),
        extract_patches=True,
    )

    cache_path = Path(str(report["cache_manifest"]))
    cache = json.loads(cache_path.read_text())
    assert report["status"] == "cache_manifest_written"
    assert cache["manifest_version"] == "abi_temporal_cache.v1"
    assert len(cache["records"]) == 1
    patches = cache["records"][0]["patches"]
    assert sorted(patches) == ["-1", "1"]
    minus_one = np.load(temporal_root / patches["-1"])
    plus_one = np.load(temporal_root / patches["1"])
    assert minus_one.shape == (256, 256, 19)
    assert plus_one.shape == (256, 256, 19)
    assert minus_one[0, 0, 0] == 1.0
    assert plus_one[0, 0, 0] == 2001.0


def test_provision_temporal_frames_fails_closed_when_google_location_crosses_center_footprint(tmp_path: Path) -> None:
    data_config = _write_google_fixture(tmp_path / "fixture")
    temporal_root = Path(str(data_config["temporal_cache"]))
    temporal_root.mkdir()
    data_config["metadata_rows"][0]["location"] = dict(_location(), col_min=10.0)
    scene_paths = tuple(str(tmp_path / f"scene-{index}.nc") for index in range(3))
    for index, scene_path in enumerate(scene_paths):
        _write_regular_scene(Path(scene_path), base=index * 1000.0)

    import pytest

    with pytest.raises(ValueError, match="Google location grid validation failed"):
        provision_temporal_frames(
            data_config=data_config,
            offsets=(-1, 0, 1),
            scenes=_scenes(keys=scene_paths),
            extract_patches=True,
        )


def test_provision_temporal_frames_subset_mode_marks_manifest_not_full_scan(tmp_path: Path) -> None:
    data_config = _write_google_fixture(tmp_path / "fixture")
    Path(str(data_config["temporal_cache"])).mkdir()

    report = provision_temporal_frames(
        data_config=data_config,
        offsets=(-1, 0, 1),
        scenes=_scenes(),
        subset_limit=1,
    )

    manifest = json.loads(Path(str(report["eligibility_manifest"])).read_text())
    assert manifest["full_dataset_scan"] is False
    assert manifest["summary"]["scanned_record_count"] == 1
    assert manifest["summary"]["eligible_record_count"] == 1
    assert report["subset_limit"] == 1
