"""Trusted temporal GOES-16 CONUS discovery and matching utilities.

These helpers are provider-owned building blocks for ABI temporal provisioning.
Filename timestamps are treated as discovery hints; scene matching uses canonical
NetCDF coverage metadata when available.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from abi_contrail.datasets import ABIPatchIndexRecord, temporal_record_identity_sha256

GOES16_CONUS_BUCKET = "noaa-goes16"
GOES16_MCMIPC_PRODUCT = "ABI-L2-MCMIPC"
GOES16_PLATFORM = "G16"
CENTER_MATCH_TOLERANCE_SECONDS = 150

_GOES_TIMESTAMP_RE = re.compile(r"[_.-](?P<tag>[sec])(?P<stamp>\d{14})")


@dataclass(frozen=True)
class GOES16ConusScene:
    """A GOES-16 ABI-L2-MCMIPC scene with trusted canonical coverage time."""

    key: str
    time_coverage_start: datetime
    time_coverage_end: datetime
    canonical_scene_time: datetime
    filename_scene_time: datetime | None = None


def goes16_mcmipc_hour_prefixes(target_time: datetime, *, hour_radius: int = 1) -> tuple[str, ...]:
    """Return S3 prefixes to scan around a target timestamp.

    The adjacent-hour scan lets center matching near an hour boundary find a
    scene whose filename hint or coverage midpoint falls outside the target
    hour. Returned prefixes include the canonical ``s3://`` bucket URI.
    """

    target = _ensure_aware_utc(target_time).replace(minute=0, second=0, microsecond=0)
    prefixes: list[str] = []
    for delta_hours in range(-hour_radius, hour_radius + 1):
        hour = target + timedelta(hours=delta_hours)
        prefixes.append(f"s3://{GOES16_CONUS_BUCKET}/{GOES16_MCMIPC_PRODUCT}/{hour:%Y}/{hour:%j}/{hour:%H}/")
    return tuple(prefixes)


def list_goes16_mcmipc_scene_keys(
    target_time: datetime,
    *,
    lister: Callable[[str], Iterable[str]] | None = None,
    hour_radius: int = 1,
) -> tuple[str, ...]:
    """List candidate GOES-16 CONUS MCMIPC NetCDF keys for a target time.

    ``lister`` is injectable for tests and offline manifests. Without it, an
    anonymous ``s3fs`` filesystem is used. This function only discovers key
    hints; callers must still load NetCDF coverage metadata before matching.
    """

    if lister is None:
        import s3fs

        fs = s3fs.S3FileSystem(anon=True)

        def lister(prefix: str) -> Iterable[str]:
            return fs.ls(prefix)

    keys: list[str] = []
    for prefix in goes16_mcmipc_hour_prefixes(target_time, hour_radius=hour_radius):
        for key in lister(prefix):
            uri = _normalise_s3_uri(str(key))
            if _is_goes16_mcmipc_netcdf_key(uri):
                keys.append(uri)
    return tuple(sorted(dict.fromkeys(keys)))


def parse_goes_abi_filename_scene_time(path_or_key: str | Path) -> datetime | None:
    """Parse the filename ``sYYYYJJJHHMMSSf`` timestamp as a discovery hint."""

    name = Path(str(path_or_key)).name
    match = _GOES_TIMESTAMP_RE.search(f"_{name}")
    if match is None:
        return None
    return _parse_goes_compact_timestamp(match.group("stamp"))


def scene_from_coverage_metadata(key: str, attrs: dict[str, Any]) -> GOES16ConusScene:
    """Build a scene from NetCDF coverage metadata attributes."""

    try:
        start = _parse_datetime(attrs["time_coverage_start"])
        end = _parse_datetime(attrs["time_coverage_end"])
    except KeyError as exc:
        raise ValueError("GOES ABI NetCDF metadata must include time_coverage_start and time_coverage_end") from exc
    if end < start:
        raise ValueError("GOES ABI time_coverage_end must not precede time_coverage_start")
    canonical = start + (end - start) / 2
    return GOES16ConusScene(
        key=str(key),
        time_coverage_start=start,
        time_coverage_end=end,
        canonical_scene_time=canonical,
        filename_scene_time=parse_goes_abi_filename_scene_time(str(key)),
    )


def read_scene_coverage_metadata(path_or_uri: str | Path) -> GOES16ConusScene:
    """Open a NetCDF scene and read trusted coverage metadata.

    This is intentionally a small boundary around ``xarray.open_dataset`` so
    provisioning code can be tested with ``scene_from_coverage_metadata`` without
    network or large files.
    """

    import xarray as xr

    with xr.open_dataset(path_or_uri) as ds:
        return scene_from_coverage_metadata(str(path_or_uri), dict(ds.attrs))


def choose_nearest_scene(
    scenes: Iterable[GOES16ConusScene],
    target_time: datetime,
    *,
    tolerance_seconds: int = CENTER_MATCH_TOLERANCE_SECONDS,
) -> GOES16ConusScene | None:
    """Return the nearest coverage-midpoint scene inside tolerance, else ``None``."""

    target = _ensure_aware_utc(target_time)
    ordered = sorted(scenes, key=lambda scene: (abs((scene.canonical_scene_time - target).total_seconds()), scene.key))
    if not ordered:
        return None
    nearest = ordered[0]
    delta = abs((nearest.canonical_scene_time - target).total_seconds())
    if delta > float(tolerance_seconds):
        return None
    return nearest


def temporal_window_by_frame_offsets(
    scenes: Sequence[GOES16ConusScene],
    center_scene: GOES16ConusScene,
    offsets: Sequence[int],
) -> tuple[GOES16ConusScene, ...] | None:
    """Select neighboring scenes by sorted CONUS capture order around center.

    Returns ``None`` when a requested neighbor is outside the known ordered
    sequence. Duplicate scene keys or duplicate canonical scene times are a
    provider-data error because they would make frame-offset semantics ambiguous.
    """

    ordered = tuple(sorted(scenes, key=lambda scene: (scene.canonical_scene_time, scene.key)))
    keys = [scene.key for scene in ordered]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate GOES ABI scene keys in temporal window candidates")
    times = [scene.canonical_scene_time for scene in ordered]
    if len(times) != len(set(times)):
        raise ValueError("duplicate GOES ABI canonical scene times in temporal window candidates")
    try:
        center_index = keys.index(center_scene.key)
    except ValueError as exc:
        raise ValueError("center scene is not present in temporal window candidates") from exc
    selected: list[GOES16ConusScene] = []
    for offset in sorted(offsets):
        neighbor_index = center_index + int(offset)
        if neighbor_index < 0 or neighbor_index >= len(ordered):
            return None
        selected.append(ordered[neighbor_index])
    if len({scene.key for scene in selected}) != len(selected):
        raise ValueError("temporal window selected duplicate GOES ABI frames")
    return tuple(selected)


def build_temporal_eligibility_manifest(
    records: Sequence[ABIPatchIndexRecord],
    scenes: Sequence[GOES16ConusScene],
    *,
    offsets: Sequence[int],
    tolerance_seconds: int = CENTER_MATCH_TOLERANCE_SECONDS,
    full_dataset_scan: bool = True,
) -> dict[str, object]:
    """Build a durable trusted temporal eligibility/provenance manifest.

    This manifest records which center ABI Patches have complete GOES-16 CONUS
    neighbor scenes for the requested frame-offset window. It does not imply the
    non-zero patch tensors have already been extracted; cache manifests add the
    per-offset patch paths after extraction.
    """

    sorted_offsets = sorted(int(offset) for offset in offsets)
    manifest_records: list[dict[str, object]] = []
    missing_goes_time_count = 0
    center_match_miss_count = 0
    neighbor_window_miss_count = 0
    for record in records:
        if not record.goes_time:
            missing_goes_time_count += 1
            continue
        target_time = _parse_datetime(record.goes_time)
        center_scene = choose_nearest_scene(scenes, target_time, tolerance_seconds=tolerance_seconds)
        if center_scene is None:
            center_match_miss_count += 1
            continue
        window = temporal_window_by_frame_offsets(scenes, center_scene, sorted_offsets)
        if window is None:
            neighbor_window_miss_count += 1
            continue
        source_scenes: dict[str, str] = {}
        for offset, scene in zip(sorted_offsets, window, strict=True):
            source_scenes[str(offset)] = "materialized_training_zarr" if offset == 0 else scene.key
        manifest_records.append(
            {
                "dataset_source": record.dataset_source,
                "split": record.split,
                "scene_name": record.scene_name,
                "scene_index": record.scene_index,
                "goes_time": record.goes_time,
                "row": record.row,
                "col": record.col,
                "sample_index": record.sample_index,
                "matched_conus_center_key": center_scene.key,
                "matched_conus_center_time": center_scene.canonical_scene_time.isoformat().replace("+00:00", "Z"),
                "temporal_source_scenes": source_scenes,
            }
        )
    return {
        "manifest_version": "abi_temporal_eligibility.v1",
        "full_dataset_scan": bool(full_dataset_scan),
        "dataset_scope": {
            "record_count": len(records),
            "record_identity_sha256": temporal_record_identity_sha256(records),
        },
        "temporal_frame_offsets": sorted_offsets,
        "matching_policy": {
            "target_time_field": "goes_time",
            "canonical_scene_time": "midpoint(time_coverage_start,time_coverage_end)",
            "center_match_tolerance_seconds": tolerance_seconds,
            "non_zero_offsets": "sorted_goes16_conus_capture_order_around_matched_center",
        },
        "source_product_policy": {
            "zero_offset_center": "materialized_training_zarr",
            "non_zero_offsets": "goes16_conus_abi_l2_mcmipc",
            "bucket": f"s3://{GOES16_CONUS_BUCKET}/",
            "key_family": f"{GOES16_MCMIPC_PRODUCT}/YYYY/DDD/HH/OR_ABI-L2-MCMIPC-*.nc",
            "fallback_platforms": [],
        },
        "summary": {
            "scanned_record_count": len(records),
            "eligible_record_count": len(manifest_records),
            "missing_goes_time_count": missing_goes_time_count,
            "center_match_miss_count": center_match_miss_count,
            "neighbor_window_miss_count": neighbor_window_miss_count,
        },
        "records": manifest_records,
    }


def build_temporal_cache_manifest_from_eligibility(
    eligibility_manifest: Mapping[str, object],
    *,
    patch_path_for: Callable[[Mapping[str, object], int], str],
) -> dict[str, object]:
    """Build an ``abi_temporal_cache.v1`` manifest from extracted patch paths."""

    if eligibility_manifest.get("manifest_version") != "abi_temporal_eligibility.v1":
        raise ValueError("eligibility manifest must have manifest_version 'abi_temporal_eligibility.v1'")
    offsets = eligibility_manifest.get("temporal_frame_offsets")
    if not isinstance(offsets, Sequence) or isinstance(offsets, (str, bytes)):
        raise ValueError("eligibility manifest temporal_frame_offsets must be a sequence")
    frame_offsets = [int(offset) for offset in offsets]
    records = eligibility_manifest.get("records")
    if not isinstance(records, Sequence) or isinstance(records, (str, bytes)):
        raise ValueError("eligibility manifest records must be a sequence")
    cache_records: list[dict[str, object]] = []
    for raw_record in records:
        if not isinstance(raw_record, Mapping):
            raise ValueError("eligibility manifest records must contain mappings")
        cache_record = {
            "dataset_source": raw_record.get("dataset_source"),
            "split": raw_record.get("split"),
            "scene_name": raw_record.get("scene_name"),
            "scene_index": raw_record.get("scene_index"),
            "goes_time": raw_record.get("goes_time"),
            "row": raw_record.get("row"),
            "col": raw_record.get("col"),
            "sample_index": raw_record.get("sample_index"),
            "matched_conus_center_key": raw_record.get("matched_conus_center_key"),
            "temporal_source_scenes": raw_record.get("temporal_source_scenes"),
            "patches": {},
        }
        patches: dict[str, str] = {}
        for offset in frame_offsets:
            if offset == 0:
                continue
            path = patch_path_for(raw_record, offset)
            if not isinstance(path, str) or not path:
                raise ValueError(f"patch_path_for returned an invalid path for offset {offset}")
            if Path(path).is_absolute() or ".." in Path(path).parts:
                raise ValueError("temporal cache patch paths must be relative paths beneath the cache root")
            patches[str(offset)] = path
        cache_record["patches"] = patches
        cache_records.append(cache_record)
    return {
        "manifest_version": "abi_temporal_cache.v1",
        "full_dataset_scan": bool(eligibility_manifest.get("full_dataset_scan", False)),
        "dataset_scope": dict(eligibility_manifest.get("dataset_scope", {})) if isinstance(eligibility_manifest.get("dataset_scope"), Mapping) else {},
        "temporal_frame_offsets": frame_offsets,
        "source_product_policy": dict(eligibility_manifest.get("source_product_policy", {})) if isinstance(eligibility_manifest.get("source_product_policy"), Mapping) else {},
        "matching_policy": dict(eligibility_manifest.get("matching_policy", {})) if isinstance(eligibility_manifest.get("matching_policy"), Mapping) else {},
        "summary": dict(eligibility_manifest.get("summary", {})) if isinstance(eligibility_manifest.get("summary"), Mapping) else {},
        "records": cache_records,
    }


def _parse_goes_compact_timestamp(stamp: str) -> datetime:
    year = int(stamp[0:4])
    day_of_year = int(stamp[4:7])
    hour = int(stamp[7:9])
    minute = int(stamp[9:11])
    second = int(stamp[11:13])
    tenth = int(stamp[13])
    start = datetime(year, 1, 1, tzinfo=UTC) + timedelta(days=day_of_year - 1)
    return start.replace(hour=hour, minute=minute, second=second, microsecond=tenth * 100_000)


def _parse_datetime(value: object) -> datetime:
    if isinstance(value, datetime):
        return _ensure_aware_utc(value)
    if not isinstance(value, str) or not value:
        raise ValueError(f"invalid GOES ABI coverage datetime: {value!r}")
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    return _ensure_aware_utc(datetime.fromisoformat(text))


def _ensure_aware_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def _normalise_s3_uri(key: str) -> str:
    if key.startswith("s3://"):
        return key
    if key.startswith(f"{GOES16_CONUS_BUCKET}/"):
        return f"s3://{key}"
    return key


def _is_goes16_mcmipc_netcdf_key(key: str) -> bool:
    return (
        key.startswith(f"s3://{GOES16_CONUS_BUCKET}/{GOES16_MCMIPC_PRODUCT}/")
        and key.endswith(".nc")
        and f"_{GOES16_PLATFORM}_" in key
        and "ABI-L2-MCMIPC" in Path(key).name
    )


__all__ = [
    "CENTER_MATCH_TOLERANCE_SECONDS",
    "GOES16_CONUS_BUCKET",
    "GOES16_MCMIPC_PRODUCT",
    "GOES16_PLATFORM",
    "GOES16ConusScene",
    "build_temporal_cache_manifest_from_eligibility",
    "build_temporal_eligibility_manifest",
    "choose_nearest_scene",
    "goes16_mcmipc_hour_prefixes",
    "list_goes16_mcmipc_scene_keys",
    "parse_goes_abi_filename_scene_time",
    "read_scene_coverage_metadata",
    "scene_from_coverage_metadata",
    "temporal_window_by_frame_offsets",
]
