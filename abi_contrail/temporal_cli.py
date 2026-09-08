"""CLI for trusted ABI temporal eligibility/cache provisioning."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from collections import OrderedDict
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

from abi_contrail.adapters import ABITrainingAdapter
from abi_contrail.data_config import (
    ABIDataConfigError,
    TRAINING_DATA_ROOT,
    named_data_roots,
    resolve_temporal_cache_root,
)
from abi_contrail.datasets import (
    ABIPatchArrays,
    ABIPatchIndexRecord,
    ABI_TEMPORAL_CACHE_SQLITE_FILENAME,
    load_abi_metadata_rows,
    mark_temporal_patch_extracted,
    open_abi_patch_arrays,
    temporal_patch_relative_path,
    temporal_record_key,
    temporal_record_key_from_mapping,
    validate_temporal_frame_offsets,
    write_temporal_cache_database,
)
from abi_contrail.temporal import (
    GOES16ConusScene,
    build_temporal_eligibility_manifest,
    goes16_mcmipc_hour_prefixes,
    read_scene_coverage_metadata,
    scene_from_coverage_metadata,
)
from abi_contrail.temporal_grids import (
    extract_regular_source_patch,
    google_temporal_patch_grid,
    mit_temporal_patch_grid,
    validate_google_center_grid_against_materialized_patch,
)
from abi_contrail.temporal_netcdf import load_regular_source_grid_from_netcdf, materialize_goes_scene


@dataclass(frozen=True)
class _RecordContext:
    record: ABIPatchIndexRecord
    arrays: ABIPatchArrays
    location: object | None = None


def provision_temporal_frames(
    *,
    data_config: Mapping[str, object],
    offsets: Sequence[int],
    scenes: Sequence[GOES16ConusScene] | None = None,
    scene_manifest_path: str | Path | None = None,
    temporal_cache_root: str | Path | None = None,
    subset_limit: int | None = None,
    output_name: str | None = None,
    extract_patches: bool = False,
    cache_manifest_name: str | None = None,
    log_interval: int = 100,
) -> dict[str, object]:
    """Provision trusted ABI temporal SQLite cache metadata and patch tensors.

    The command scans the configured ABI Patch records, matches each record's
    ``goes_time`` to trusted GOES-16 CONUS scene coverage metadata, and writes a
    durable SQLite cache database under the trusted temporal cache root. With
    ``extract_patches=True`` it also materializes non-zero frame tensors into
    reusable per-offset patch directories.
    """

    frame_offsets = validate_temporal_frame_offsets(offsets)
    if subset_limit is not None and subset_limit < 1:
        raise ValueError("subset_limit must be positive")
    temporal_root = _resolve_temporal_root(data_config, temporal_cache_root)
    temporal_root.mkdir(parents=True, exist_ok=True)
    _progress(log_interval, f"loading configured ABI Patch records from data root into temporal provisioning scope")
    context_by_key = _configured_record_contexts(data_config)
    all_records = tuple(context.record for context in context_by_key.values())
    scanned_records = all_records[:subset_limit] if subset_limit is not None else all_records
    _progress(
        log_interval,
        f"configured_records={len(all_records)} scanned_records={len(scanned_records)} offsets={list(frame_offsets)} extract_patches={extract_patches}",
    )
    resolved_scenes = _load_scenes(scanned_records, scenes=scenes, scene_manifest_path=scene_manifest_path, log_interval=log_interval)
    _progress(log_interval, f"building temporal eligibility metadata using {len(resolved_scenes)} discovered CONUS scenes")
    manifest = build_temporal_eligibility_manifest(
        scanned_records,
        resolved_scenes,
        offsets=frame_offsets,
        full_dataset_scan=subset_limit is None,
    )
    del output_name, cache_manifest_name  # JSON manifests were replaced by the issue-5 SQLite cache layout.
    database_path = temporal_root / ABI_TEMPORAL_CACHE_SQLITE_FILENAME
    write_temporal_cache_database(
        database_path,
        cache_root=temporal_root,
        records=scanned_records,
        scenes=resolved_scenes,
        eligibility=manifest,
    )
    _progress(
        log_interval,
        f"wrote temporal cache database {database_path} time_eligible_records={manifest['summary']['eligible_record_count']}",
    )
    report = {
        "status": "temporal_cache_database_written",
        "temporal_cache_database": str(database_path),
        "temporal_cache_root": str(temporal_root),
        "temporal_frame_offsets": list(frame_offsets),
        "subset_limit": subset_limit,
        "full_dataset_scan": subset_limit is None,
        "configured_record_count": len(all_records),
        "scanned_record_count": len(scanned_records),
        "eligible_record_count": manifest["summary"]["eligible_record_count"],
        "next_phase": "download_reproject_extract_non_zero_temporal_patches_and_update_sqlite_cache",
    }
    if extract_patches:
        extraction_summary = _extract_temporal_patch_cache(
            manifest,
            database_path=database_path,
            context_by_key=context_by_key,
            scenes=resolved_scenes,
            temporal_root=temporal_root,
            frame_offsets=frame_offsets,
            log_interval=log_interval,
        )
        report.update(
            {
                "status": "temporal_cache_database_updated",
                "cache_eligible_record_count": extraction_summary.get("eligible_record_count", 0),
                "coverage_rejected_record_count": extraction_summary.get("coverage_rejected_record_count", 0),
                "extracted_patch_count": extraction_summary.get("extracted_patch_count", 0),
                "reused_patch_count": extraction_summary.get("reused_patch_count", 0),
                "next_phase": "candidate_training_can_use_temporal_cache_sqlite_database",
            }
        )
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Provision trusted ABI temporal SQLite cache metadata for provider-owned temporal inputs."
    )
    parser.add_argument("--workspace-root", type=Path, default=Path("."))
    parser.add_argument("--offsets", required=True, help="Comma-separated frame offsets, e.g. -1,0,1")
    parser.add_argument(
        "--scene-manifest",
        type=Path,
        help="Optional JSON scene metadata manifest for offline/test provisioning; otherwise GOES-16 S3 coverage metadata is discovered.",
    )
    parser.add_argument("--temporal-cache-root", type=Path, help="Override configured data_roots.temporal_cache.")
    parser.add_argument("--subset-limit", type=int, help="Trusted smoke/debug subset size; SQLite cache scope is marked full_dataset_scan=false.")
    parser.add_argument("--output-name", help="Deprecated; JSON manifests were replaced by abi-temporal-cache.sqlite.")
    parser.add_argument("--extract-patches", action="store_true", help="Download/materialize non-zero GOES scenes, extract trusted patch tensors, and update abi-temporal-cache.sqlite.")
    parser.add_argument("--cache-manifest-name", help="Deprecated; JSON manifests were replaced by abi-temporal-cache.sqlite.")
    parser.add_argument("--log-interval", type=int, default=100, help="Progress logging interval; use 0 to disable progress logs.")
    args = parser.parse_args(_normalise_negative_offsets_option(argv))

    from ml_autoresearch.candidate_execution_config import load_candidate_execution_config

    workspace_root = args.workspace_root.expanduser().resolve()
    config = load_candidate_execution_config(workspace_root)
    provider = config.research_problem_provider
    if provider is None:
        raise RuntimeError("workspace has no configured Research Problem provider")
    report = provision_temporal_frames(
        data_config=provider.effective_data_config(),
        offsets=_parse_offsets(args.offsets),
        scene_manifest_path=args.scene_manifest,
        temporal_cache_root=args.temporal_cache_root,
        subset_limit=args.subset_limit,
        output_name=args.output_name,
        extract_patches=args.extract_patches,
        cache_manifest_name=args.cache_manifest_name,
        log_interval=args.log_interval,
    )
    report["workspace_root"] = str(workspace_root)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


def _configured_records(data_config: Mapping[str, object]) -> tuple[ABIPatchIndexRecord, ...]:
    return tuple(context.record for context in _configured_record_contexts(data_config).values())


def _configured_record_contexts(data_config: Mapping[str, object]) -> dict[tuple[object, ...], _RecordContext]:
    adapter = ABITrainingAdapter(data_config)
    root = adapter.validate_data_root(data_config)
    contexts: dict[tuple[object, ...], _RecordContext] = {}
    for source_config in adapter._source_data_configs(root, data_config):
        layout = str(source_config["layout"])
        inputs_path = adapter._resolve_required_path(root, source_config, "inputs_zarr")
        labels_path = adapter._resolve_required_path(root, source_config, "labels_zarr")
        arrays = open_abi_patch_arrays(inputs_path, labels_path, layout=layout)  # type: ignore[arg-type]
        metadata_rows = load_abi_metadata_rows(root, source_config) or ()
        metadata_by_sample_index = _metadata_by_sample_index(metadata_rows)
        split_index = adapter._build_split_index(arrays.labels, root=root, layout=layout, data_config=source_config)
        for record in split_index.records:
            location = None
            if record.dataset_source == "google" and record.sample_index is not None:
                metadata = metadata_by_sample_index.get(record.sample_index, {})
                location = metadata.get("location", metadata.get("location_json"))
            key = temporal_record_key(record)
            if key in contexts:
                raise ValueError(f"duplicate ABI temporal record key: {key!r}")
            contexts[key] = _RecordContext(record=record, arrays=arrays, location=location)
    return contexts


def _metadata_by_sample_index(rows: Sequence[Mapping[str, object]]) -> dict[int, Mapping[str, object]]:
    result: dict[int, Mapping[str, object]] = {}
    for fallback_index, row in enumerate(rows):
        raw_index = row.get("sample_index", row.get("index", row.get("patch_index", fallback_index)))
        result[int(raw_index)] = row
    return result


def _extract_temporal_patch_cache(
    eligibility_manifest: Mapping[str, object],
    *,
    database_path: Path,
    context_by_key: Mapping[tuple[object, ...], _RecordContext],
    scenes: Sequence[GOES16ConusScene],
    temporal_root: Path,
    frame_offsets: Sequence[int],
    log_interval: int = 100,
) -> dict[str, object]:
    scene_cache_root = temporal_root / "source-scenes"
    source_grid_cache: OrderedDict[str, object] = OrderedDict()
    loaded_source_scene_keys: set[str] = set()
    scene_by_key = {scene.key: scene for scene in scenes}
    records = eligibility_manifest.get("records", ())
    if not isinstance(records, Sequence) or isinstance(records, (str, bytes)):
        raise ValueError("eligibility metadata records must be a sequence")
    written_paths: set[Path] = set()
    extracted_record_count = 0
    coverage_rejected_record_count = 0
    extracted_patch_count = 0
    reused_patch_count = 0
    _progress(log_interval, f"extracting temporal patch cache for time_eligible_records={len(records)}")
    for record_index, raw_record in enumerate(records, start=1):
        if not isinstance(raw_record, Mapping):
            raise ValueError("eligibility metadata records must contain mappings")
        record_key = temporal_record_key_from_mapping(raw_record)
        try:
            context = context_by_key[record_key]
        except KeyError as exc:
            raise ValueError(f"eligibility record is not present in configured dataset scope: {record_key!r}") from exc
        target_grid = _target_grid_for_context(context)
        source_scenes = raw_record.get("temporal_source_scenes")
        if not isinstance(source_scenes, Mapping):
            raise ValueError("eligibility record is missing temporal_source_scenes")
        record_patches: dict[int, np.ndarray] = {}
        coverage_rejected = False
        for offset in frame_offsets:
            if offset == 0:
                continue
            rel_path = temporal_patch_relative_path(raw_record, int(offset))
            output_path = (temporal_root / rel_path).resolve()
            try:
                output_path.relative_to(temporal_root)
            except ValueError as exc:
                raise ValueError("temporal cache patch output escaped temporal cache root") from exc
            if _temporal_patch_already_extracted(database_path, raw_record, int(offset), rel_path) and output_path.is_file():
                reused_patch_count += 1
                continue
            scene_key = source_scenes.get(str(offset), source_scenes.get(offset))
            if not isinstance(scene_key, str) or not scene_key:
                raise ValueError(f"eligibility record is missing scene key for offset {offset}")
            if scene_key not in source_grid_cache:
                local_scene = materialize_goes_scene(scene_key, scene_cache_root)
                source_grid_cache[scene_key] = load_regular_source_grid_from_netcdf(local_scene)
                loaded_source_scene_keys.add(scene_key)
                _progress(
                    log_interval,
                    f"source scene load progress unique_source_scenes={len(loaded_source_scene_keys)} memory_cache_entries={len(source_grid_cache)}",
                    every=max(log_interval, 50),
                    count=len(loaded_source_scene_keys),
                )
                while len(source_grid_cache) > 4:
                    source_grid_cache.popitem(last=False)
            else:
                source_grid_cache.move_to_end(scene_key)
            scene = scene_by_key.get(scene_key)
            observation_time = scene.canonical_scene_time if scene is not None else raw_record.get("goes_time")
            try:
                record_patches[int(offset)] = extract_regular_source_patch(
                    source_grid_cache[scene_key],  # type: ignore[arg-type]
                    target_grid,
                    observation_time=observation_time,
                )
            except ValueError as exc:
                if "does not fully cover requested temporal ABI Patch footprint" not in str(exc):
                    raise
                coverage_rejected = True
                coverage_rejected_record_count += 1
                break
        if coverage_rejected:
            _progress(
                log_interval,
                f"extract progress records={record_index}/{len(records)} extracted_records={extracted_record_count} coverage_rejected={coverage_rejected_record_count}",
                every=log_interval,
                count=record_index,
            )
            continue
        for offset, patch in record_patches.items():
            rel_path = temporal_patch_relative_path(raw_record, offset)
            output_path = (temporal_root / rel_path).resolve()
            if output_path in written_paths:
                raise ValueError(f"duplicate temporal cache patch output path: {output_path}")
            output_path.parent.mkdir(parents=True, exist_ok=True)
            _write_npy_atomic(output_path, patch)
            written_paths.add(output_path)
            mark_temporal_patch_extracted(database_path, raw_record, offset, rel_path)
            extracted_patch_count += 1
        extracted_record_count += 1
        _progress(
            log_interval,
            f"extract progress records={record_index}/{len(records)} extracted_records={extracted_record_count} coverage_rejected={coverage_rejected_record_count}",
            every=log_interval,
            count=record_index,
        )
    return {
        "time_eligible_record_count": len(records),
        "coverage_rejected_record_count": coverage_rejected_record_count,
        "eligible_record_count": extracted_record_count,
        "extracted_patch_count": extracted_patch_count,
        "reused_patch_count": reused_patch_count,
        "source_scene_count": len(loaded_source_scene_keys),
        "source_grid_memory_cache_limit": 4,
        "patch_storage": "npy_hwc_19_provider_internal_channels",
    }


def _target_grid_for_context(context: _RecordContext):
    if context.record.dataset_source == "mit":
        return mit_temporal_patch_grid(context.record)
    if context.location is None:
        raise ValueError("Google temporal extraction requires trusted location metadata")
    raw_center = _raw_center_inputs(context)
    validate_google_center_grid_against_materialized_patch(raw_center, context.location)
    return google_temporal_patch_grid(context.location)


def _raw_center_inputs(context: _RecordContext) -> np.ndarray:
    record = context.record
    if record.sample_index is not None:
        return np.asarray(context.arrays.inputs[record.sample_index, :, :, :])
    row_end = record.row + 256
    col_end = record.col + 256
    return np.asarray(context.arrays.inputs[record.scene_index, record.row : row_end, record.col : col_end, :])


def _temporal_patch_already_extracted(database_path: Path, record: Mapping[str, object], offset: int, patch_path: str) -> bool:
    import sqlite3
    from abi_contrail.datasets import temporal_record_key_sha256

    record_digest = temporal_record_key_sha256(temporal_record_key_from_mapping(record))
    with sqlite3.connect(database_path) as connection:
        row = connection.execute(
            """
            SELECT p.status, p.patch_path
            FROM temporal_patches p
            JOIN abi_patch_records r ON r.id = p.record_id
            WHERE r.record_key_sha256 = ? AND p.offset = ?
            """,
            (record_digest, int(offset)),
        ).fetchone()
    return row is not None and row[0] == "extracted" and row[1] == patch_path


def _write_npy_atomic(path: Path, array: np.ndarray) -> None:
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            np.save(handle, array)
        os.replace(tmp_name, path)
    finally:
        Path(tmp_name).unlink(missing_ok=True)


def _load_scenes(
    records: Sequence[ABIPatchIndexRecord],
    *,
    scenes: Sequence[GOES16ConusScene] | None,
    scene_manifest_path: str | Path | None,
    log_interval: int = 100,
) -> tuple[GOES16ConusScene, ...]:
    if scenes is not None and scene_manifest_path is not None:
        raise ValueError("provide either scenes or scene_manifest_path, not both")
    if scenes is not None:
        _progress(log_interval, f"using caller-provided scene metadata count={len(scenes)}")
        return tuple(scenes)
    if scene_manifest_path is not None:
        loaded = _load_scene_manifest(scene_manifest_path)
        _progress(log_interval, f"loaded scene metadata manifest {scene_manifest_path} scenes={len(loaded)}")
        return loaded
    keys = _discover_scene_keys_for_records(records, log_interval=log_interval)
    sorted_keys = sorted(keys)
    _progress(log_interval, f"resolving coverage metadata for discovered_scene_keys={len(sorted_keys)}")
    resolved: list[GOES16ConusScene] = []
    for index, key in enumerate(sorted_keys, start=1):
        resolved.append(read_scene_coverage_metadata(key))
        _progress(
            log_interval,
            f"coverage metadata progress scenes={index}/{len(sorted_keys)}",
            every=max(log_interval, 500),
            count=index,
        )
    return tuple(resolved)


def _discover_scene_keys_for_records(
    records: Sequence[ABIPatchIndexRecord],
    *,
    lister: Callable[[str], Iterable[str]] | None = None,
    log_interval: int = 100,
) -> set[str]:
    from abi_contrail.temporal import _is_goes16_mcmipc_netcdf_key, _normalise_s3_uri, _parse_datetime

    if lister is None:
        import s3fs

        fs = s3fs.S3FileSystem(anon=True)

        def lister(prefix: str) -> Iterable[str]:
            return fs.ls(prefix)

    prefixes: set[str] = set()
    missing_goes_time_count = 0
    for record in records:
        if not record.goes_time:
            missing_goes_time_count += 1
            continue
        prefixes.update(goes16_mcmipc_hour_prefixes(_parse_datetime(record.goes_time)))
    sorted_prefixes = sorted(prefixes)
    _progress(
        log_interval,
        f"discovering GOES-16 CONUS scene keys unique_hour_prefixes={len(sorted_prefixes)} missing_goes_time_records={missing_goes_time_count}",
    )
    keys: set[str] = set()
    missing_prefix_count = 0
    for index, prefix in enumerate(sorted_prefixes, start=1):
        try:
            listed_keys = lister(prefix)
        except FileNotFoundError:
            missing_prefix_count += 1
            listed_keys = ()
        before = len(keys)
        for key in listed_keys:
            uri = _normalise_s3_uri(str(key))
            if _is_goes16_mcmipc_netcdf_key(uri):
                keys.add(uri)
        _progress(
            log_interval,
            f"S3 discovery progress prefixes={index}/{len(sorted_prefixes)} scene_keys={len(keys)} missing_prefixes={missing_prefix_count}",
            every=log_interval,
            count=index,
        )
    _progress(
        log_interval,
        f"S3 discovery complete unique_hour_prefixes={len(sorted_prefixes)} scene_keys={len(keys)} missing_prefixes={missing_prefix_count}",
    )
    return keys


def _load_scene_manifest(path: str | Path) -> tuple[GOES16ConusScene, ...]:
    payload = json.loads(Path(path).read_text())
    raw_scenes = payload.get("scenes", payload) if isinstance(payload, Mapping) else payload
    if not isinstance(raw_scenes, Sequence) or isinstance(raw_scenes, (str, bytes)):
        raise ValueError("scene manifest must contain a scenes sequence")
    scenes: list[GOES16ConusScene] = []
    for item in raw_scenes:
        if not isinstance(item, Mapping):
            raise ValueError("scene manifest scenes must be mappings")
        key = str(item.get("key", item.get("path", "")))
        if not key:
            raise ValueError("scene manifest scene is missing key")
        attrs = item.get("attrs")
        if isinstance(attrs, Mapping):
            scenes.append(scene_from_coverage_metadata(key, dict(attrs)))
        else:
            scenes.append(
                scene_from_coverage_metadata(
                    key,
                    {
                        "time_coverage_start": item.get("time_coverage_start"),
                        "time_coverage_end": item.get("time_coverage_end"),
                    },
                )
            )
    return tuple(scenes)


def _resolve_temporal_root(data_config: Mapping[str, object], override: str | Path | None) -> Path:
    if override is not None:
        return Path(override).expanduser().resolve()
    try:
        return resolve_temporal_cache_root(data_config)
    except ABIDataConfigError:
        roots = named_data_roots(data_config)
        if roots is not None and TRAINING_DATA_ROOT in roots:
            return (roots[TRAINING_DATA_ROOT] / "temporal-cache").resolve()
        raise


def _normalise_negative_offsets_option(argv: list[str] | None) -> list[str]:
    """Let documented ``--offsets -1,0,1`` syntax survive argparse option parsing.

    ``argparse`` treats values beginning with ``-`` as potential options before
    handing them to the option's type/parser. ABI temporal offsets commonly
    begin with a negative frame offset, so normalize the separated form to the
    unambiguous ``--offsets=-1,0,1`` spelling.
    """

    raw = list(sys.argv[1:] if argv is None else argv)
    normalised: list[str] = []
    index = 0
    while index < len(raw):
        item = raw[index]
        if item == "--offsets" and index + 1 < len(raw):
            value = raw[index + 1]
            if value.startswith("-") and value not in {"-h", "--help"}:
                normalised.append(f"--offsets={value}")
                index += 2
                continue
        normalised.append(item)
        index += 1
    return normalised


def _parse_offsets(value: str) -> tuple[int, ...]:
    try:
        return tuple(int(part.strip()) for part in value.split(",") if part.strip())
    except ValueError as exc:
        raise ValueError("--offsets must be comma-separated integers") from exc


def _progress(log_interval: int, message: str, *, every: int | None = None, count: int | None = None) -> None:
    if log_interval <= 0:
        return
    if count is not None:
        interval = every if every is not None else log_interval
        if count % interval != 0:
            return
    print(f"[abi-temporal] {message}", file=sys.stderr, flush=True)


__all__ = ["main", "provision_temporal_frames"]
