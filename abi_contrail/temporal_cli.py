"""CLI for trusted ABI temporal eligibility/cache provisioning."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

from abi_contrail.adapters import ABITrainingAdapter
from abi_contrail.data_config import (
    ABIDataConfigError,
    TRAINING_DATA_ROOT,
    named_data_roots,
    resolve_root_relative_path,
    resolve_temporal_cache_root,
)
from abi_contrail.datasets import (
    ABIPatchArrays,
    ABIPatchIndexRecord,
    load_abi_metadata_rows,
    open_abi_patch_arrays,
    temporal_offsets_cache_token,
    temporal_record_key,
    temporal_record_key_from_mapping,
    validate_temporal_frame_offsets,
)
from abi_contrail.temporal import (
    GOES16ConusScene,
    build_temporal_cache_manifest_from_eligibility,
    build_temporal_eligibility_manifest,
    list_goes16_mcmipc_scene_keys,
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
) -> dict[str, object]:
    """Provision the current vertical slice: temporal eligibility manifest.

    The command scans the configured ABI Patch records, matches each record's
    ``goes_time`` to trusted GOES-16 CONUS scene coverage metadata, and writes a
    durable eligibility/provenance manifest under the trusted temporal cache
    root. Actual non-zero frame download/reprojection/cache-tensor extraction is
    intentionally a later provisioning phase.
    """

    frame_offsets = validate_temporal_frame_offsets(offsets)
    if subset_limit is not None and subset_limit < 1:
        raise ValueError("subset_limit must be positive")
    temporal_root = _resolve_temporal_root(data_config, temporal_cache_root)
    temporal_root.mkdir(parents=True, exist_ok=True)
    context_by_key = _configured_record_contexts(data_config)
    all_records = tuple(context.record for context in context_by_key.values())
    scanned_records = all_records[:subset_limit] if subset_limit is not None else all_records
    resolved_scenes = _load_scenes(scanned_records, scenes=scenes, scene_manifest_path=scene_manifest_path)
    manifest = build_temporal_eligibility_manifest(
        scanned_records,
        resolved_scenes,
        offsets=frame_offsets,
        full_dataset_scan=subset_limit is None,
    )
    filename = output_name or f"abi-temporal-eligibility-offsets-{temporal_offsets_cache_token(frame_offsets)}.json"
    manifest_path = _contained_output_path(temporal_root, filename)
    _write_json_atomic(manifest_path, manifest)
    report = {
        "status": "eligibility_manifest_written",
        "eligibility_manifest": str(manifest_path),
        "temporal_cache_root": str(temporal_root),
        "temporal_frame_offsets": list(frame_offsets),
        "subset_limit": subset_limit,
        "full_dataset_scan": subset_limit is None,
        "configured_record_count": len(all_records),
        "scanned_record_count": len(scanned_records),
        "eligible_record_count": manifest["summary"]["eligible_record_count"],
        "next_phase": "download_reproject_extract_non_zero_temporal_patches_and_write_abi_temporal_cache_v1_manifest",
    }
    if extract_patches:
        cache_manifest = _extract_temporal_patch_cache(
            manifest,
            context_by_key=context_by_key,
            scenes=resolved_scenes,
            temporal_root=temporal_root,
            frame_offsets=frame_offsets,
        )
        cache_filename = cache_manifest_name or f"abi-temporal-cache-offsets-{temporal_offsets_cache_token(frame_offsets)}.json"
        cache_manifest_path = _contained_output_path(temporal_root, cache_filename)
        _write_json_atomic(cache_manifest_path, cache_manifest)
        report.update(
            {
                "status": "cache_manifest_written",
                "cache_manifest": str(cache_manifest_path),
                "extracted_patch_count": cache_manifest["summary"].get("extracted_patch_count", 0),
                "next_phase": "candidate_training_can_use_temporal_cache_manifest",
            }
        )
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Provision trusted ABI temporal eligibility/cache metadata for provider-owned temporal inputs."
    )
    parser.add_argument("--workspace-root", type=Path, default=Path("."))
    parser.add_argument("--offsets", required=True, help="Comma-separated frame offsets, e.g. -1,0,1")
    parser.add_argument(
        "--scene-manifest",
        type=Path,
        help="Optional JSON scene metadata manifest for offline/test provisioning; otherwise GOES-16 S3 coverage metadata is discovered.",
    )
    parser.add_argument("--temporal-cache-root", type=Path, help="Override configured data_roots.temporal_cache.")
    parser.add_argument("--subset-limit", type=int, help="Trusted smoke/debug subset size; output manifest is marked full_dataset_scan=false.")
    parser.add_argument("--output-name", help="Eligibility manifest filename under the temporal cache root.")
    parser.add_argument("--extract-patches", action="store_true", help="Download/materialize non-zero GOES scenes, extract trusted patch tensors, and write an abi_temporal_cache.v1 manifest.")
    parser.add_argument("--cache-manifest-name", help="Cache manifest filename under the temporal cache root when --extract-patches is used.")
    args = parser.parse_args(argv)

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
    context_by_key: Mapping[tuple[object, ...], _RecordContext],
    scenes: Sequence[GOES16ConusScene],
    temporal_root: Path,
    frame_offsets: Sequence[int],
) -> dict[str, object]:
    patch_paths: dict[tuple[tuple[object, ...], int], str] = {}
    scene_cache_root = temporal_root / "source-scenes"
    patch_root = temporal_root / "patches" / temporal_offsets_cache_token(frame_offsets)
    source_grid_cache: dict[str, object] = {}
    scene_by_key = {scene.key: scene for scene in scenes}
    records = eligibility_manifest.get("records", ())
    if not isinstance(records, Sequence) or isinstance(records, (str, bytes)):
        raise ValueError("eligibility manifest records must be a sequence")
    written_paths: set[Path] = set()
    for raw_record in records:
        if not isinstance(raw_record, Mapping):
            raise ValueError("eligibility manifest records must contain mappings")
        record_key = temporal_record_key_from_mapping(raw_record)
        try:
            context = context_by_key[record_key]
        except KeyError as exc:
            raise ValueError(f"eligibility record is not present in configured dataset scope: {record_key!r}") from exc
        target_grid = _target_grid_for_context(context)
        source_scenes = raw_record.get("temporal_source_scenes")
        if not isinstance(source_scenes, Mapping):
            raise ValueError("eligibility record is missing temporal_source_scenes")
        for offset in frame_offsets:
            if offset == 0:
                continue
            scene_key = source_scenes.get(str(offset), source_scenes.get(offset))
            if not isinstance(scene_key, str) or not scene_key:
                raise ValueError(f"eligibility record is missing scene key for offset {offset}")
            if scene_key not in source_grid_cache:
                local_scene = materialize_goes_scene(scene_key, scene_cache_root)
                source_grid_cache[scene_key] = load_regular_source_grid_from_netcdf(local_scene)
            scene = scene_by_key.get(scene_key)
            observation_time = scene.canonical_scene_time if scene is not None else raw_record.get("goes_time")
            patch = extract_regular_source_patch(
                source_grid_cache[scene_key],  # type: ignore[arg-type]
                target_grid,
                observation_time=observation_time,
            )
            rel_path = _patch_relative_path(raw_record, offset, frame_offsets)
            output_path = (temporal_root / rel_path).resolve()
            try:
                output_path.relative_to(temporal_root)
            except ValueError as exc:
                raise ValueError("temporal cache patch output escaped temporal cache root") from exc
            if output_path in written_paths:
                raise ValueError(f"duplicate temporal cache patch output path: {output_path}")
            output_path.parent.mkdir(parents=True, exist_ok=True)
            _write_npy_atomic(output_path, patch)
            written_paths.add(output_path)
            patch_paths[(record_key, int(offset))] = rel_path
    cache_manifest = build_temporal_cache_manifest_from_eligibility(
        eligibility_manifest,
        patch_path_for=lambda record, offset: patch_paths[(temporal_record_key_from_mapping(record), int(offset))],
    )
    summary = dict(cache_manifest.get("summary", {})) if isinstance(cache_manifest.get("summary"), Mapping) else {}
    summary["extracted_patch_count"] = len(patch_paths)
    summary["source_scene_count"] = len(source_grid_cache)
    summary["patch_storage"] = "npy_hwc_19_provider_internal_channels"
    cache_manifest["summary"] = summary
    return cache_manifest


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


def _patch_relative_path(record: Mapping[str, object], offset: int, frame_offsets: Sequence[int]) -> str:
    import hashlib

    key_payload = json.dumps(list(temporal_record_key_from_mapping(record)), sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(key_payload.encode("utf-8")).hexdigest()[:24]
    dataset_source = str(record.get("dataset_source"))
    split = str(record.get("split"))
    token = temporal_offsets_cache_token(frame_offsets)
    return f"patches/{token}/{_safe_path_component(dataset_source)}/{_safe_path_component(split)}/{digest}_offset_{offset:+d}.npy"


def _safe_path_component(value: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in value)
    if not cleaned or cleaned in {".", ".."}:
        raise ValueError(f"invalid temporal cache path component: {value!r}")
    return cleaned


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
) -> tuple[GOES16ConusScene, ...]:
    if scenes is not None and scene_manifest_path is not None:
        raise ValueError("provide either scenes or scene_manifest_path, not both")
    if scenes is not None:
        return tuple(scenes)
    if scene_manifest_path is not None:
        return _load_scene_manifest(scene_manifest_path)
    keys: set[str] = set()
    for record in records:
        if not record.goes_time:
            continue
        from abi_contrail.temporal import _parse_datetime  # trusted internal parser reused by CLI discovery

        keys.update(list_goes16_mcmipc_scene_keys(_parse_datetime(record.goes_time)))
    return tuple(read_scene_coverage_metadata(key) for key in sorted(keys))


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


def _contained_output_path(root: Path, filename: str) -> Path:
    try:
        path = resolve_root_relative_path(root, filename, config_key="output_name", named_root="temporal_cache")
    except ABIDataConfigError as exc:
        raise ValueError(str(exc)) from exc
    return path


def _write_json_atomic(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w") as handle:
            handle.write(text)
        os.replace(tmp_name, path)
    finally:
        Path(tmp_name).unlink(missing_ok=True)


def _parse_offsets(value: str) -> tuple[int, ...]:
    try:
        return tuple(int(part.strip()) for part in value.split(",") if part.strip())
    except ValueError as exc:
        raise ValueError("--offsets must be comma-separated integers") from exc


__all__ = ["main", "provision_temporal_frames"]
