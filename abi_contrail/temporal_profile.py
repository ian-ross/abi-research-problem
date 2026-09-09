"""Agent-visible temporal eligibility profile generation for ABI temporal caches."""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
from collections import defaultdict
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from ml_autoresearch.errors import ResearchProblemDataError

from abi_contrail.adapters import RESEARCH_PROBLEM_ID, RESEARCH_PROBLEM_VERSION
from abi_contrail.data_config import ABIDataConfigError, named_data_roots, resolve_root_relative_path, resolve_temporal_cache_root
from abi_contrail.datasets import (
    ABI_INPUT_MODE_SOURCE_INDICES,
    ABI_TEMPORAL_ALLOWED_FRAME_OFFSETS,
    ABI_TEMPORAL_CACHE_SQLITE_FILENAME,
    ABI_TEMPORAL_CACHE_SQLITE_SCHEMA_VERSION,
    INPUT_MODE_ABI_16CH_PLUS_SZA_TEMPORAL,
    ABIPatchIndexRecord,
    temporal_record_identity_sha256,
)
from abi_contrail.record_selection import (
    BOUNDED_SELECTION_POLICY_NAME,
    BOUNDED_SELECTION_POLICY_SEED,
    BOUNDED_SELECTION_POLICY_VERSION,
    select_representative_records,
)

GENERATOR_VERSION = "abi_contrail.temporal_eligibility_profile.v1"
SCHEMA_VERSION = "abi-temporal-eligibility-profile.v1"


def generate_temporal_eligibility_profile(
    *,
    temporal_cache_root: str | Path,
    database_name: str | Path = ABI_TEMPORAL_CACHE_SQLITE_FILENAME,
    max_samples: int | None = None,
) -> dict[str, Any]:
    """Generate a leakage-safe temporal eligibility summary from SQLite cache metadata.

    The SQLite database remains the operational source of truth. This profile is
    the agent-visible aggregate view: it discloses counts, bounded selector audit
    metadata, and cache provenance, but no ABI tensors, coordinates, record lists,
    scene identities, patch paths, or unrestricted cache roots.
    """

    cache_root = Path(temporal_cache_root).expanduser().resolve()
    database_path = _resolve_database_path(cache_root, database_name)
    if not database_path.is_file():
        raise ResearchProblemDataError(f"ABI temporal cache SQLite database is missing: {database_path}")

    database_sha256 = _file_sha256(database_path)
    records, scope, sqlite_schema_version, patch_rows, source_scene_count = _load_cache_rows(database_path)
    if sqlite_schema_version != ABI_TEMPORAL_CACHE_SQLITE_SCHEMA_VERSION:
        raise ResearchProblemDataError(
            f"ABI temporal cache SQLite schema_version must be {ABI_TEMPORAL_CACHE_SQLITE_SCHEMA_VERSION!r}, got {sqlite_schema_version!r}"
        )
    expected_scope_digest = temporal_record_identity_sha256(tuple(records.values()))
    scope_digest = str(scope.get("record_identity_sha256") or "")
    scope_status = "matches_records" if scope_digest == expected_scope_digest else "digest_mismatch"

    patches_by_record = _patches_by_record(patch_rows)
    patch_status_summary = _patch_status_summary(patch_rows, cache_root=cache_root)
    windows = []
    for offsets in ABI_TEMPORAL_ALLOWED_FRAME_OFFSETS:
        eligible = tuple(record for record_id, record in records.items() if _is_eligible(record_id, offsets, patches_by_record))
        windows.append(_window_summary(offsets, eligible, max_samples=max_samples, all_records=tuple(records.values())))

    return {
        "artifact_type": "temporal_eligibility_profile",
        "schema_version": SCHEMA_VERSION,
        "provenance": {
            "research_problem_id": RESEARCH_PROBLEM_ID,
            "research_problem_version": RESEARCH_PROBLEM_VERSION,
            "generation_version": GENERATOR_VERSION,
            "generation_timestamp": _timestamp(),
            "generation_command": "uv run abi-temporal-eligibility-profile --workspace-root . --output abi_contrail/profile/temporal-eligibility-profile.v1.json",
            "source_policy": "trusted Research Problem package-generated from provider-owned SQLite temporal cache",
            "split_scope": "Google source provenance plus MIT deterministic whole-scene split before windowing",
            "candidate_authority": "none",
        },
        "temporal_input_boundary": {
            "input_mode": INPUT_MODE_ABI_16CH_PLUS_SZA_TEMPORAL,
            "allowed_temporal_frame_offsets": [list(window) for window in ABI_TEMPORAL_ALLOWED_FRAME_OFFSETS],
            "target_frame_offset": 0,
            "candidate_visible_channels_per_frame": 17,
            "source_channel_indices_per_frame": list(ABI_INPUT_MODE_SOURCE_INDICES[INPUT_MODE_ABI_16CH_PLUS_SZA_TEMPORAL]),
            "goes_abi_channel_numbers_per_frame": list(range(1, 17)),
            "extra_inputs_per_frame": [{"name": "solar_zenith_angle", "source_channel_index": 18}],
            "forbidden_source_channel_indices": [16, 17],
            "longitude_latitude_exposed_to_candidates": False,
            "patch_paths_disclosed": False,
            "record_identities_disclosed": False,
        },
        "cache_provenance": {
            "sqlite_filename": database_path.name,
            "sqlite_sha256": database_sha256,
            "sqlite_schema_version": sqlite_schema_version,
            "cache_root_disclosed": False,
            "dataset_scope": {
                "record_count": int(scope.get("record_count") or 0),
                "record_identity_sha256": scope_digest,
                "record_identity_status": scope_status,
                "expected_record_identity_sha256_from_sqlite_records": expected_scope_digest,
                "full_dataset_scan": bool(scope.get("full_dataset_scan")),
                "updated_at": scope.get("updated_at"),
            },
            "source_scene_count": source_scene_count,
            "temporal_patch_status_by_offset": patch_status_summary,
        },
        "bounded_record_selection": {
            "policy_name": BOUNDED_SELECTION_POLICY_NAME,
            "policy_version": BOUNDED_SELECTION_POLICY_VERSION,
            "seed": BOUNDED_SELECTION_POLICY_SEED,
            "requested_cap_per_source_split": max_samples,
            "cap_scope": "independent_per_dataset_source_and_leakage_safe_split",
            "record_identities_disclosed": False,
        },
        "windows": windows,
        "known_caveats": [
            "The SQLite temporal cache is the operational source of truth; this artifact is an aggregate agent-visible profile.",
            "Eligibility for non-zero offsets requires SQLite status='extracted' and a non-null patch_path for every required non-zero offset.",
            "Patch path values and individual ABI Patch identities are intentionally not serialized.",
            "Capped counts use the trusted representative selector and are feasibility-context summaries, not full-data promotion evidence.",
        ],
    }


def generate_temporal_eligibility_profile_from_data_config(
    data_config: Mapping[str, object],
    *,
    max_samples: int | None = None,
    temporal_cache_root: str | Path | None = None,
    database_name: str | Path | None = None,
) -> dict[str, Any]:
    """Resolve trusted temporal cache config and generate the profile."""

    try:
        root = Path(temporal_cache_root).expanduser().resolve() if temporal_cache_root is not None else resolve_temporal_cache_root(data_config)
    except ABIDataConfigError as exc:
        raise ResearchProblemDataError(str(exc)) from exc
    name = database_name if database_name is not None else data_config.get("temporal_cache_database", ABI_TEMPORAL_CACHE_SQLITE_FILENAME)
    return generate_temporal_eligibility_profile(temporal_cache_root=root, database_name=name, max_samples=max_samples)  # type: ignore[arg-type]


def write_temporal_eligibility_profile(profile: Mapping[str, object], output: str | Path) -> None:
    """Atomically write a temporal eligibility profile JSON artifact."""

    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(profile, indent=2, sort_keys=True) + "\n"
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(payload)
    temporary.replace(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate agent-visible ABI temporal eligibility profile from trusted SQLite cache metadata.")
    parser.add_argument("--workspace-root", type=Path, default=Path("."))
    parser.add_argument("--temporal-cache-root", type=Path, help="Override configured data_roots.temporal_cache.")
    parser.add_argument("--temporal-cache-database", help="Override configured temporal cache database name/path.")
    parser.add_argument("--max-samples", type=int, help="Per-source/split cap for selected-count summaries; defaults to Workspace Configuration.")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)

    from ml_autoresearch.candidate_execution_config import load_candidate_execution_config

    workspace_root = args.workspace_root.expanduser().resolve()
    config = load_candidate_execution_config(workspace_root)
    provider = config.research_problem_provider
    if provider is None:
        raise RuntimeError("workspace has no configured Research Problem provider")
    max_samples = args.max_samples if args.max_samples is not None else config.max_samples
    profile = generate_temporal_eligibility_profile_from_data_config(
        provider.effective_data_config(),
        max_samples=max_samples,
        temporal_cache_root=args.temporal_cache_root,
        database_name=args.temporal_cache_database,
    )
    write_temporal_eligibility_profile(profile, args.output)
    print(json.dumps({"status": "temporal_eligibility_profile_written", "output": str(args.output), "windows": [window["temporal_frame_offsets"] for window in profile["windows"]]}, indent=2, sort_keys=True))
    return 0


def _resolve_database_path(cache_root: Path, database_name: str | Path) -> Path:
    try:
        return resolve_root_relative_path(
            cache_root,
            str(database_name),
            config_key="temporal_cache_database",
            named_root="temporal_cache" if named_data_roots({"data_roots": {"temporal_cache": str(cache_root)}}) is not None else None,
        )
    except ABIDataConfigError as exc:
        raise ResearchProblemDataError(str(exc)) from exc


def _load_cache_rows(database_path: Path) -> tuple[dict[int, ABIPatchIndexRecord], dict[str, object], str | None, list[dict[str, object]], int]:
    with sqlite3.connect(database_path) as connection:
        connection.row_factory = sqlite3.Row
        try:
            schema_row = connection.execute("SELECT value FROM cache_metadata WHERE key = 'schema_version'").fetchone()
            scope_row = connection.execute("SELECT record_count, record_identity_sha256, full_dataset_scan, updated_at FROM dataset_scope WHERE id = 1").fetchone()
            record_rows = connection.execute(
                """
                SELECT id, dataset_source, split, scene_name, scene_index, goes_time, row, col, positive, sample_index
                FROM abi_patch_records
                ORDER BY id
                """
            ).fetchall()
            patch_rows = connection.execute("SELECT record_id, offset, status, patch_path FROM temporal_patches ORDER BY offset, status").fetchall()
            source_scene_count = int(connection.execute("SELECT count(*) FROM source_scenes").fetchone()[0])
        except sqlite3.Error as exc:
            raise ResearchProblemDataError(f"invalid ABI temporal cache SQLite database: {exc}") from exc
    if schema_row is None:
        raise ResearchProblemDataError("ABI temporal cache SQLite database is missing cache_metadata.schema_version")
    if scope_row is None:
        raise ResearchProblemDataError("ABI temporal cache SQLite database is missing dataset_scope")
    records = {
        int(row["id"]): ABIPatchIndexRecord(
            dataset_source=str(row["dataset_source"]),  # type: ignore[arg-type]
            split=str(row["split"]),  # type: ignore[arg-type]
            scene_name=str(row["scene_name"]),
            scene_index=int(row["scene_index"]),
            goes_time=None if row["goes_time"] is None else str(row["goes_time"]),
            row=int(row["row"]),
            col=int(row["col"]),
            positive=bool(row["positive"]),
            sample_index=None if row["sample_index"] is None else int(row["sample_index"]),
        )
        for row in record_rows
    }
    scope = {
        "record_count": int(scope_row["record_count"]),
        "record_identity_sha256": str(scope_row["record_identity_sha256"]),
        "full_dataset_scan": bool(scope_row["full_dataset_scan"]),
        "updated_at": str(scope_row["updated_at"]),
    }
    return records, scope, str(schema_row["value"]), [dict(row) for row in patch_rows], source_scene_count


def _patches_by_record(patch_rows: Sequence[Mapping[str, object]]) -> dict[int, dict[int, Mapping[str, object]]]:
    patches: dict[int, dict[int, Mapping[str, object]]] = defaultdict(dict)
    for row in patch_rows:
        patches[int(row["record_id"])][int(row["offset"])] = row
    return patches


def _is_eligible(record_id: int, offsets: Sequence[int], patches_by_record: Mapping[int, Mapping[int, Mapping[str, object]]]) -> bool:
    for offset in offsets:
        if int(offset) == 0:
            continue
        patch = patches_by_record.get(record_id, {}).get(int(offset))
        if patch is None or str(patch.get("status")) != "extracted" or not patch.get("patch_path"):
            return False
    return True


def _window_summary(
    offsets: Sequence[int],
    eligible_records: Sequence[ABIPatchIndexRecord],
    *,
    max_samples: int | None,
    all_records: Sequence[ABIPatchIndexRecord],
) -> dict[str, object]:
    records_by_source_split: dict[tuple[str, str], list[ABIPatchIndexRecord]] = defaultdict(list)
    all_by_source_split: dict[tuple[str, str], list[ABIPatchIndexRecord]] = defaultdict(list)
    for record in eligible_records:
        records_by_source_split[(record.dataset_source, record.split)].append(record)
    for record in all_records:
        all_by_source_split[(record.dataset_source, record.split)].append(record)
    source_split_keys = sorted(set(all_by_source_split) | set(records_by_source_split))
    by_source: dict[str, dict[str, object]] = {}
    total = positive = negative = selected_total = selected_positive = selected_negative = 0
    zero_reasons: list[str] = []
    for source, split in source_split_keys:
        split_records = tuple(records_by_source_split.get((source, split), ()))
        selected = select_representative_records(split_records, max_samples, dataset_source=source, split=split)  # type: ignore[arg-type]
        split_positive = sum(record.positive for record in split_records)
        split_negative = len(split_records) - split_positive
        split_summary = {
            "eligible_count": len(split_records),
            "eligible_positive_count": split_positive,
            "eligible_negative_count": split_negative,
            "selected_count": selected.metadata["selected_count"],
            "selected_positive_count": selected.metadata["selected_positive_count"],
            "selected_negative_count": selected.metadata["selected_negative_count"],
            "selected_record_identity_sha256": selected.metadata["selected_record_identity_sha256"],
            "record_identities_disclosed": False,
        }
        if len(split_records) == 0:
            split_summary["unavailable_reason"] = "no_records_have_all_required_extracted_nonzero_offsets" if any(offset != 0 for offset in offsets) else "no_center_records_in_dataset_scope"
            zero_reasons.append(f"{source}/{split}: {split_summary['unavailable_reason']}")
        by_source.setdefault(source, {})[split] = split_summary
        total += len(split_records)
        positive += split_positive
        negative += split_negative
        selected_total += int(selected.metadata["selected_count"])
        selected_positive += int(selected.metadata["selected_positive_count"])
        selected_negative += int(selected.metadata["selected_negative_count"])
    summary: dict[str, object] = {
        "temporal_frame_offsets": list(offsets),
        "required_non_zero_offsets": [offset for offset in offsets if offset != 0],
        "eligible_count": total,
        "eligible_positive_count": positive,
        "eligible_negative_count": negative,
        "selected_count": selected_total,
        "selected_positive_count": selected_positive,
        "selected_negative_count": selected_negative,
        "by_source": by_source,
    }
    if total == 0:
        summary["unavailable_reason"] = "no_records_have_all_required_extracted_nonzero_offsets" if any(offset != 0 for offset in offsets) else "no_center_records_in_dataset_scope"
    elif zero_reasons:
        summary["partial_unavailable_reasons"] = zero_reasons
    return summary


def _patch_status_summary(patch_rows: Sequence[Mapping[str, object]], *, cache_root: Path) -> dict[str, object]:
    summary: dict[int, dict[str, int]] = defaultdict(lambda: defaultdict(int))  # type: ignore[assignment]
    missing_extracted_files: dict[int, int] = defaultdict(int)
    invalid_relative_paths: dict[int, int] = defaultdict(int)
    for row in patch_rows:
        offset = int(row["offset"])
        status = str(row["status"])
        summary[offset][status] += 1
        patch_path = row.get("patch_path")
        if status == "extracted":
            if not isinstance(patch_path, str) or not patch_path:
                missing_extracted_files[offset] += 1
                continue
            path = (cache_root / patch_path).resolve()
            try:
                path.relative_to(cache_root)
            except ValueError:
                invalid_relative_paths[offset] += 1
                continue
            if not path.is_file():
                missing_extracted_files[offset] += 1
    result = {}
    for offset in sorted(summary):
        result[str(offset)] = {
            "status_counts": dict(sorted(summary[offset].items())),
            "extracted_patch_files_missing_count": missing_extracted_files.get(offset, 0),
            "invalid_relative_patch_path_count": invalid_relative_paths.get(offset, 0),
        }
    return result


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _timestamp() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


__all__ = [
    "GENERATOR_VERSION",
    "SCHEMA_VERSION",
    "generate_temporal_eligibility_profile",
    "generate_temporal_eligibility_profile_from_data_config",
    "write_temporal_eligibility_profile",
]
