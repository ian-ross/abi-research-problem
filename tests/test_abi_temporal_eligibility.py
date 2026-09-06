from __future__ import annotations

from datetime import datetime, timezone

import pytest

from abi_contrail.datasets import ABIPatchIndexRecord, temporal_record_identity_sha256
from abi_contrail.temporal import GOES16ConusScene, build_temporal_cache_manifest_from_eligibility, build_temporal_eligibility_manifest


def _dt(minute: int) -> datetime:
    return datetime(2020, 1, 1, 0, minute, tzinfo=timezone.utc)


def _scene(index: int) -> GOES16ConusScene:
    return GOES16ConusScene(
        key=f"s3://noaa-goes16/ABI-L2-MCMIPC/2020/001/00/scene-{index}.nc",
        time_coverage_start=_dt(index * 5),
        time_coverage_end=_dt(index * 5 + 1),
        canonical_scene_time=_dt(index * 5),
        filename_scene_time=None,
    )


def _record(name: str, minute: int | None) -> ABIPatchIndexRecord:
    return ABIPatchIndexRecord(
        dataset_source="mit",
        split="train",
        scene_name=name,
        scene_index=int(name.rsplit("-", 1)[-1]),
        goes_time=None if minute is None else f"2020-01-01T00:{minute:02d}:00Z",
        row=0,
        col=0,
        positive=True,
        sample_index=None,
    )


def test_temporal_eligibility_manifest_records_full_scope_and_mixed_provenance_policy() -> None:
    records = (_record("mit-scene-0", 5), _record("mit-scene-1", None), _record("mit-scene-2", 0))
    scenes = tuple(_scene(index) for index in range(3))

    manifest = build_temporal_eligibility_manifest(records, scenes, offsets=(-1, 0, 1))

    assert manifest["manifest_version"] == "abi_temporal_eligibility.v1"
    assert manifest["full_dataset_scan"] is True
    assert manifest["dataset_scope"]["record_count"] == 3
    assert manifest["dataset_scope"]["record_identity_sha256"] == temporal_record_identity_sha256(records)
    assert manifest["temporal_frame_offsets"] == [-1, 0, 1]
    assert manifest["source_product_policy"]["zero_offset_center"] == "materialized_training_zarr"
    assert manifest["source_product_policy"]["non_zero_offsets"] == "goes16_conus_abi_l2_mcmipc"
    assert manifest["summary"] == {
        "scanned_record_count": 3,
        "eligible_record_count": 1,
        "missing_goes_time_count": 1,
        "center_match_miss_count": 0,
        "neighbor_window_miss_count": 1,
    }
    eligible = manifest["records"][0]
    assert eligible["scene_name"] == "mit-scene-0"
    assert eligible["matched_conus_center_key"].endswith("scene-1.nc")
    assert eligible["temporal_source_scenes"] == {
        "-1": "s3://noaa-goes16/ABI-L2-MCMIPC/2020/001/00/scene-0.nc",
        "0": "materialized_training_zarr",
        "1": "s3://noaa-goes16/ABI-L2-MCMIPC/2020/001/00/scene-2.nc",
    }


def test_temporal_eligibility_fails_closed_on_duplicate_source_frames() -> None:
    records = (_record("mit-scene-0", 5),)
    scenes = (_scene(0), _scene(1), _scene(1))

    with pytest.raises(ValueError, match="duplicate GOES ABI"):
        build_temporal_eligibility_manifest(records, scenes, offsets=(-1, 0, 1))


def test_temporal_cache_manifest_is_derived_from_eligibility_with_non_zero_patch_paths() -> None:
    records = (_record("mit-scene-0", 5),)
    eligibility = build_temporal_eligibility_manifest(records, tuple(_scene(index) for index in range(3)), offsets=(-1, 0, 1))

    cache = build_temporal_cache_manifest_from_eligibility(
        eligibility,
        patch_path_for=lambda record, offset: f"patches/{record['dataset_source']}/{record['scene_index']}_{offset}.npy",
    )

    assert cache["manifest_version"] == "abi_temporal_cache.v1"
    assert cache["full_dataset_scan"] is True
    assert cache["dataset_scope"] == eligibility["dataset_scope"]
    assert cache["temporal_frame_offsets"] == [-1, 0, 1]
    assert cache["source_product_policy"] == eligibility["source_product_policy"]
    assert cache["records"][0]["patches"] == {
        "-1": "patches/mit/0_-1.npy",
        "1": "patches/mit/0_1.npy",
    }
    assert "0" not in cache["records"][0]["patches"]
