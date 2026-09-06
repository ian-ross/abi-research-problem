from __future__ import annotations

from datetime import datetime, timezone

import pytest

from abi_contrail.temporal import (
    GOES16_CONUS_BUCKET,
    GOES16_MCMIPC_PRODUCT,
    GOES16ConusScene,
    choose_nearest_scene,
    goes16_mcmipc_hour_prefixes,
    parse_goes_abi_filename_scene_time,
    scene_from_coverage_metadata,
    temporal_window_by_frame_offsets,
)


def _dt(minute: int, second: int = 0) -> datetime:
    return datetime(2020, 1, 1, 0, minute, second, tzinfo=timezone.utc)


def test_goes16_mcmipc_prefixes_cover_adjacent_hours_for_boundary_matching() -> None:
    prefixes = goes16_mcmipc_hour_prefixes(datetime(2020, 1, 1, 0, 1, tzinfo=timezone.utc))

    assert prefixes == (
        f"s3://{GOES16_CONUS_BUCKET}/{GOES16_MCMIPC_PRODUCT}/2019/365/23/",
        f"s3://{GOES16_CONUS_BUCKET}/{GOES16_MCMIPC_PRODUCT}/2020/001/00/",
        f"s3://{GOES16_CONUS_BUCKET}/{GOES16_MCMIPC_PRODUCT}/2020/001/01/",
    )


def test_goes_filename_timestamp_is_parsed_only_as_discovery_hint() -> None:
    scene_time = parse_goes_abi_filename_scene_time(
        "OR_ABI-L2-MCMIPC-M6_G16_s20200010001172_e20200010003545_c20200010004029.nc"
    )

    assert scene_time == datetime(2020, 1, 1, 0, 1, 17, 200000, tzinfo=timezone.utc)


def test_nearest_scene_uses_coverage_midpoint_metadata_not_filename_hint() -> None:
    target = _dt(5)
    misleading_filename = "OR_ABI-L2-MCMIPC-M6_G16_s20200010030000_e20200010031000_c20200010032000.nc"
    scene = scene_from_coverage_metadata(
        f"s3://{GOES16_CONUS_BUCKET}/{GOES16_MCMIPC_PRODUCT}/2020/001/00/{misleading_filename}",
        {
            "time_coverage_start": "2020-01-01T00:04:30Z",
            "time_coverage_end": "2020-01-01T00:05:30Z",
        },
    )

    assert scene.filename_scene_time == _dt(30)
    assert scene.canonical_scene_time == target
    assert choose_nearest_scene([scene], target, tolerance_seconds=150) == scene


def test_nearest_scene_fails_closed_when_center_match_exceeds_tolerance() -> None:
    scene = scene_from_coverage_metadata(
        "s3://noaa-goes16/ABI-L2-MCMIPC/2020/001/00/OR_ABI-L2-MCMIPC-M6_G16_s20200010000000_e20200010001000_c20200010002000.nc",
        {
            "time_coverage_start": "2020-01-01T00:00:00Z",
            "time_coverage_end": "2020-01-01T00:01:00Z",
        },
    )

    assert choose_nearest_scene([scene], _dt(4), tolerance_seconds=150) is None


def test_temporal_window_selects_offsets_by_sorted_capture_order_without_duplication() -> None:
    scenes = tuple(
        GOES16ConusScene(
            key=f"scene-{index}.nc",
            time_coverage_start=_dt(index * 5),
            time_coverage_end=_dt(index * 5, 30),
            canonical_scene_time=_dt(index * 5, 15),
            filename_scene_time=None,
        )
        for index in range(5)
    )

    window = temporal_window_by_frame_offsets(scenes, scenes[2], (-1, 0, 1))

    assert [scene.key for scene in window] == ["scene-1.nc", "scene-2.nc", "scene-3.nc"]


def test_temporal_window_fails_closed_at_sequence_boundary_and_duplicate_scene_times() -> None:
    scenes = tuple(
        GOES16ConusScene(
            key=f"scene-{index}.nc",
            time_coverage_start=_dt(index * 5),
            time_coverage_end=_dt(index * 5, 30),
            canonical_scene_time=_dt(index * 5, 15),
            filename_scene_time=None,
        )
        for index in range(2)
    )
    assert temporal_window_by_frame_offsets(scenes, scenes[0], (-1, 0, 1)) is None

    duplicate_time = GOES16ConusScene(
        key="duplicate.nc",
        time_coverage_start=scenes[1].time_coverage_start,
        time_coverage_end=scenes[1].time_coverage_end,
        canonical_scene_time=scenes[1].canonical_scene_time,
        filename_scene_time=None,
    )
    with pytest.raises(ValueError, match="duplicate"):
        temporal_window_by_frame_offsets((*scenes, duplicate_time), scenes[1], (0,))
