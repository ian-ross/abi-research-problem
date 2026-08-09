"""Canonical trusted MCAST comparison-target registry.

The registry is a small machine-readable index over immutable baseline evaluation
artifacts.  It keeps external evaluation outputs outside the repository while
making their raw and Artifact-Filtered metric namespaces discoverable and
verifiable by trusted candidate acceptance reporting.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from collections import Counter
from collections.abc import Mapping
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from abi_contrail.baseline_segmenters import (
    MCAST_BASELINE_1_1,
    MCAST_BASELINE_2_1,
    MCAST_BASELINE_METADATA,
    MCAST_BASELINE_NAMES,
)
from abi_contrail.data_config import (
    ABIDataConfigError,
    BASELINES_DATA_ROOT,
    named_data_roots,
    resolve_root_relative_path,
)

REGISTRY_SCHEMA = "abi_canonical_baseline_targets/v1"
DEFAULT_REGISTRY_ID = "abi-mcast-working-validation-v1"
CANONICAL_TARGETS_CONFIG_KEY = "canonical_baseline_targets"
_CANONICAL_MODEL_ASSETS = {
    MCAST_BASELINE_1_1: Path("model-assets/detection-1.1.pt"),
    MCAST_BASELINE_2_1: Path("model-assets/detection-2.1"),
}
_REQUIRED_METRICS = (
    "dice",
    "iou",
    "precision",
    "recall",
    "contrail_connectivity",
)


def generate_canonical_baseline_targets(
    *,
    source_root: str | Path,
    output_path: str | Path,
    registry_id: str = DEFAULT_REGISTRY_ID,
) -> dict[str, object]:
    """Validate one full-filter baseline run and write its canonical registry."""

    source = Path(source_root).expanduser().resolve(strict=True)
    output = Path(output_path).expanduser().resolve()
    if not registry_id.strip():
        raise ValueError("registry_id must be non-empty")

    baseline_records: dict[str, dict[str, object]] = {}
    common_sample_set: dict[str, object] | None = None
    common_filter_pipeline: list[dict[str, object]] | None = None
    common_workspace_git: object | None = None
    common_harness_git: object | None = None
    common_sources: object | None = None

    for baseline_name in MCAST_BASELINE_NAMES:
        evaluation_dir = source / baseline_name
        manifest_path = evaluation_dir / "run_manifest.json"
        manifest = _read_json_object(manifest_path)
        if manifest.get("status") != "completed":
            raise ValueError(f"baseline run is not completed: {manifest_path}")
        baseline = _required_mapping(manifest, "baseline", manifest_path)
        if baseline.get("name") != baseline_name:
            raise ValueError(
                f"baseline identity mismatch in {manifest_path}: expected {baseline_name!r}"
            )

        artifacts = _required_mapping(manifest, "artifacts", manifest_path)
        artifact_records: dict[str, dict[str, object]] = {}
        for artifact_name in (
            "aggregate_metrics",
            "per_sample_metrics",
            "threshold_sweep",
            "diagnostic_samples",
        ):
            relative_value = artifacts.get(artifact_name)
            if not isinstance(relative_value, str) or not relative_value:
                raise ValueError(f"missing artifacts.{artifact_name} in {manifest_path}")
            relative_path = Path(relative_value)
            if relative_path.is_absolute():
                raise ValueError(f"artifacts.{artifact_name} must be relative in {manifest_path}")
            artifact_path = (evaluation_dir / relative_path).resolve(strict=True)
            try:
                artifact_path.relative_to(evaluation_dir.resolve())
            except ValueError as exc:
                raise ValueError(
                    f"artifacts.{artifact_name} escapes the baseline evaluation directory in {manifest_path}"
                ) from exc
            artifact_records[artifact_name] = {
                "path": f"{baseline_name}/{relative_path.as_posix()}",
                "sha256": _file_sha256(artifact_path),
                "size_bytes": artifact_path.stat().st_size,
            }
        artifact_records["run_manifest"] = {
            "path": f"{baseline_name}/run_manifest.json",
            "sha256": _file_sha256(manifest_path),
            "size_bytes": manifest_path.stat().st_size,
        }

        aggregate_path = (evaluation_dir / str(artifacts["aggregate_metrics"])).resolve()
        aggregate = _read_json_object(aggregate_path)
        metrics = _required_mapping(aggregate, "metrics", aggregate_path)
        manifest_metrics = _required_mapping(manifest, "metrics", manifest_path)
        if metrics != manifest_metrics:
            raise ValueError(
                f"aggregate metrics do not match run manifest for {baseline_name}"
            )
        _validate_metric_namespaces(metrics, baseline_name=baseline_name)

        asset = baseline.get("asset")
        if not isinstance(asset, Mapping) or not isinstance(asset.get("sha256"), str) or not asset.get("sha256"):
            raise ValueError(f"baseline asset checksum is missing in {manifest_path}")
        asset_path_value = asset.get("path")
        if not isinstance(asset_path_value, str) or not asset_path_value:
            raise ValueError(f"baseline asset path is missing in {manifest_path}")
        raw_asset_path = Path(asset_path_value).expanduser()
        source_asset_path = (
            source / raw_asset_path if not raw_asset_path.is_absolute() else raw_asset_path
        ).resolve(strict=True)
        _verify_model_asset(source_asset_path, asset, baseline_name=baseline_name)

        sample_count = _required_positive_int(manifest.get("sample_count"), "sample_count", manifest_path)
        aggregate_sample_count = _required_positive_int(
            aggregate.get("sample_count"), "sample_count", aggregate_path
        )
        if aggregate_sample_count != sample_count:
            raise ValueError(f"sample-count mismatch for {baseline_name}")

        per_sample_path = (evaluation_dir / str(artifacts["per_sample_metrics"])).resolve()
        sample_set, filter_pipeline = _inspect_per_sample_metrics(
            per_sample_path,
            expected_count=sample_count,
        )
        removed_total = sum(
            int(item["removed_pixel_count"]) for item in filter_pipeline
        )
        aggregate_removed_value = float(metrics.get("artifact_filters/removed_pixel_count", -1))
        if not aggregate_removed_value.is_integer():
            raise ValueError(f"aggregate removed-pixel count is not integral for {baseline_name}")
        aggregate_removed = int(aggregate_removed_value)
        if removed_total != aggregate_removed:
            raise ValueError(
                f"per-filter removed-pixel total does not match aggregate metrics for {baseline_name}"
            )

        geographic = filter_pipeline[0]
        if (
            geographic.get("name") != "geographic_feature_filter"
            or geographic.get("active") is not True
            or geographic.get("required") is not True
        ):
            raise ValueError(f"canonical filtered target requires active, required geographic filtering for {baseline_name}")
        expected_source_ids = {
            "natural_earth_10m_coastline",
            "natural_earth_10m_rivers_north_america",
        }
        actual_source_ids = {
            source_record.get("id")
            for source_record in geographic.get("sources", [])
            if isinstance(source_record, Mapping)
        }
        source_records = [
            source_record
            for source_record in geographic.get("sources", [])
            if isinstance(source_record, Mapping)
        ]
        if actual_source_ids != expected_source_ids or any(
            not isinstance(source_record.get("version"), str)
            or not source_record.get("version")
            or not isinstance(source_record.get("sha256"), str)
            or not source_record.get("sha256")
            or not isinstance(source_record.get("size_bytes"), int)
            or int(source_record["size_bytes"]) <= 0
            for source_record in source_records
        ):
            raise ValueError(f"canonical geographic provenance is incomplete for {baseline_name}")
        scanline = filter_pipeline[1]
        if (
            scanline.get("name") != "scanline_artifact_filter"
            or int(scanline.get("min_length_pixels", 0)) <= 0
            or float(scanline.get("max_probability_std", -1.0)) < 0.0
        ):
            raise ValueError(f"canonical filtered target requires configured scanline filtering for {baseline_name}")

        data_config = _required_mapping(manifest, "data_config", manifest_path)
        sources = data_config.get("sources")
        if common_sample_set is None:
            common_sample_set = sample_set
            common_filter_pipeline = _pipeline_without_counts(filter_pipeline)
            common_workspace_git = manifest.get("workspace_git")
            common_harness_git = manifest.get("harness_git")
            common_sources = sources
        else:
            if sample_set != common_sample_set:
                raise ValueError("MCAST baseline targets do not use the same validation sample set")
            if _pipeline_without_counts(filter_pipeline) != common_filter_pipeline:
                raise ValueError("MCAST baseline targets do not use the same Artifact Filter pipeline")
            if sources != common_sources:
                raise ValueError("MCAST baseline targets do not use the same source/split configuration")
            if manifest.get("workspace_git") != common_workspace_git:
                raise ValueError("MCAST baseline targets do not use the same workspace provenance")
            if manifest.get("harness_git") != common_harness_git:
                raise ValueError("MCAST baseline targets do not use the same Harness provenance")

        baseline_records[baseline_name] = {
            "name": baseline_name,
            "version": str(baseline.get("version", "")),
            "sample_count": sample_count,
            "asset": dict(asset),
            "_source_asset_path": str(source_asset_path),
            "completed_at": manifest.get("completed_at"),
            "metrics": dict(metrics),
            "filter_removed_pixel_counts": {
                str(item["name"]): int(item["removed_pixel_count"])
                for item in filter_pipeline
            },
            "artifacts": artifact_records,
        }

    assert common_sample_set is not None
    assert common_filter_pipeline is not None
    output.parent.mkdir(parents=True, exist_ok=True)
    _install_canonical_artifacts(source=source, canonical_root=output.parent)
    _install_canonical_model_assets(
        baseline_records=baseline_records,
        canonical_root=output.parent,
    )
    _rewrite_canonical_model_asset_paths(
        baseline_records=baseline_records,
        canonical_root=output.parent,
    )
    _refresh_canonical_artifact_provenance(
        baseline_records=baseline_records,
        canonical_root=output.parent,
    )

    registry: dict[str, object] = {
        "schema": REGISTRY_SCHEMA,
        "registry_id": registry_id,
        "generated_at": _timestamp(),
        "research_problem_id": "goes_abi_contrail_segmentation",
        "canonical_artifact_root": ".",
        "sample_set": common_sample_set,
        "source_split_config": common_sources,
        "comparison_modes": {
            "unfiltered": {
                "metric_namespace": "raw",
                "artifact_filters": [],
                "description": "Provider metrics before Geographic Feature and Scanline Artifact Filters.",
            },
            "artifact_filtered": {
                "metric_namespace": "filtered",
                "artifact_filters": common_filter_pipeline,
                "description": "Provider metrics after the ordered Geographic Feature and Scanline Artifact Filter pipeline.",
            },
        },
        "provenance": {
            "workspace_git": common_workspace_git,
            "harness_git": common_harness_git,
        },
        "baselines": baseline_records,
    }
    temporary_output = output.with_name(f".{output.name}.tmp")
    temporary_output.write_text(json.dumps(registry, indent=2, sort_keys=True) + "\n")
    try:
        load_canonical_baseline_targets(temporary_output, verify_artifacts=True)
        temporary_output.replace(output)
    finally:
        temporary_output.unlink(missing_ok=True)
    return registry


def load_canonical_baseline_targets(
    path: str | Path,
    *,
    verify_artifacts: bool = True,
) -> dict[str, object]:
    """Load and validate a canonical target registry and its artifact references."""

    registry_path = Path(path).expanduser().resolve(strict=True)
    registry = _read_json_object(registry_path)
    if registry.get("schema") != REGISTRY_SCHEMA:
        raise ValueError(
            f"unsupported canonical baseline registry schema in {registry_path}: {registry.get('schema')!r}"
        )
    registry_id = registry.get("registry_id")
    if not isinstance(registry_id, str) or not registry_id:
        raise ValueError(f"canonical baseline registry_id is missing in {registry_path}")
    if registry.get("canonical_artifact_root") != "." or "source_evaluation_root" in registry:
        raise ValueError(
            "canonical baseline registry must be self-contained and must not reference a source evaluation root"
        )

    modes = _required_mapping(registry, "comparison_modes", registry_path)
    expected_modes = {"unfiltered": "raw", "artifact_filtered": "filtered"}
    for mode, namespace in expected_modes.items():
        mode_config = modes.get(mode)
        if not isinstance(mode_config, Mapping) or mode_config.get("metric_namespace") != namespace:
            raise ValueError(
                f"canonical baseline registry mode {mode!r} must use {namespace!r} metrics"
            )
    filtered_pipeline = modes["artifact_filtered"].get("artifact_filters")
    if (
        not isinstance(filtered_pipeline, list)
        or len(filtered_pipeline) != 2
        or not all(isinstance(item, Mapping) for item in filtered_pipeline)
        or [item.get("name") for item in filtered_pipeline] != [
            "geographic_feature_filter",
            "scanline_artifact_filter",
        ]
    ):
        raise ValueError("canonical filtered mode must record geographic then scanline filtering")

    baselines = _required_mapping(registry, "baselines", registry_path)
    if set(baselines) != set(MCAST_BASELINE_NAMES):
        raise ValueError(
            f"canonical registry must contain exactly {sorted(MCAST_BASELINE_NAMES)}"
        )
    expected_sample_count = _required_positive_int(
        _required_mapping(registry, "sample_set", registry_path).get("sample_count"),
        "sample_set.sample_count",
        registry_path,
    )
    for baseline_name in MCAST_BASELINE_NAMES:
        record = baselines[baseline_name]
        if not isinstance(record, Mapping) or record.get("name") != baseline_name:
            raise ValueError(f"invalid canonical baseline record for {baseline_name}")
        if _required_positive_int(record.get("sample_count"), "sample_count", registry_path) != expected_sample_count:
            raise ValueError(f"canonical baseline sample-count mismatch for {baseline_name}")
        metrics = record.get("metrics")
        if not isinstance(metrics, Mapping):
            raise ValueError(f"canonical baseline metrics are missing for {baseline_name}")
        _validate_metric_namespaces(metrics, baseline_name=baseline_name)
        asset = record.get("asset")
        if not isinstance(asset, Mapping):
            raise ValueError(f"canonical baseline model asset is missing for {baseline_name}")
        asset_path = _resolve_artifact_path(registry_path, asset)
        if verify_artifacts:
            _verify_model_asset(asset_path, asset, baseline_name=baseline_name)
        artifacts = record.get("artifacts")
        if not isinstance(artifacts, Mapping):
            raise ValueError(f"canonical baseline artifacts are missing for {baseline_name}")
        if verify_artifacts:
            _verify_registry_artifacts(
                registry_path=registry_path,
                baseline_name=baseline_name,
                record=record,
            )
    return registry


def canonical_baseline_metrics(
    registry_path: str | Path,
    *,
    verify_artifacts: bool = True,
) -> dict[str, dict[str, object]]:
    """Return acceptance-report metric records with canonical source references."""

    path = Path(registry_path).expanduser().resolve(strict=True)
    registry = load_canonical_baseline_targets(path, verify_artifacts=verify_artifacts)
    registry_id = str(registry["registry_id"])
    records: dict[str, dict[str, object]] = {}
    for baseline_name, raw_record in _required_mapping(registry, "baselines", path).items():
        assert isinstance(raw_record, Mapping)
        metrics = dict(_required_mapping(raw_record, "metrics", path))
        artifacts = _required_mapping(raw_record, "artifacts", path)
        metrics.update(
            {
                "baseline/name": str(baseline_name),
                "baseline/version": raw_record.get("version"),
                "baseline/target_registry_id": registry_id,
                "baseline/target_registry_path": str(path),
                "baseline/run_manifest_path": str(
                    _resolve_artifact_path(path, _required_mapping(artifacts, "run_manifest", path))
                ),
                "baseline/aggregate_metrics_path": str(
                    _resolve_artifact_path(path, _required_mapping(artifacts, "aggregate_metrics", path))
                ),
            }
        )
        records[str(baseline_name)] = metrics
    return records


def resolve_canonical_baseline_targets_path(data_config: Mapping[str, object]) -> Path:
    """Resolve the configured registry under the named trusted baselines root."""

    value = data_config.get(CANONICAL_TARGETS_CONFIG_KEY)
    roots = named_data_roots(data_config)
    if roots is not None:
        try:
            root = roots[BASELINES_DATA_ROOT]
        except KeyError as exc:
            raise ABIDataConfigError(
                "ABI data_config.data_roots.baselines is required for canonical baseline targets"
            ) from exc
        return resolve_root_relative_path(
            root,
            value,
            config_key=CANONICAL_TARGETS_CONFIG_KEY,
            named_root=BASELINES_DATA_ROOT,
        )
    if not isinstance(value, str) or not value:
        raise ABIDataConfigError(
            f"ABI data_config.{CANONICAL_TARGETS_CONFIG_KEY} must be a non-empty path string"
        )
    return Path(value).expanduser().resolve()


def _inspect_per_sample_metrics(
    path: Path,
    *,
    expected_count: int,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    sample_digest = hashlib.sha256()
    source_counts: Counter[str] = Counter()
    sample_ids: set[str] = set()
    filter_signature: list[dict[str, object]] | None = None
    filter_removed: Counter[str] = Counter()
    count = 0

    with path.open() as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid JSON at {path}:{line_number}") from exc
            if not isinstance(record, Mapping):
                raise ValueError(f"per-sample record must be an object at {path}:{line_number}")
            sample_id = record.get("sample_id")
            if not isinstance(sample_id, str) or not sample_id:
                raise ValueError(f"missing sample_id at {path}:{line_number}")
            if sample_id in sample_ids:
                raise ValueError(f"duplicate sample_id {sample_id!r} in {path}")
            sample_ids.add(sample_id)
            sample_digest.update(sample_id.encode("utf-8") + b"\n")
            source = record.get("sample/dataset_source", record.get("Dataset Source"))
            if not isinstance(source, str) or not source:
                raise ValueError(f"missing Dataset Source at {path}:{line_number}")
            source_counts[source] += 1

            diagnostics = record.get("artifact_filters/diagnostics")
            if not isinstance(diagnostics, Mapping):
                raise ValueError(f"missing Artifact Filter diagnostics at {path}:{line_number}")
            filters = diagnostics.get("filters")
            if not isinstance(filters, list) or len(filters) != 2:
                raise ValueError(f"expected two Artifact Filters at {path}:{line_number}")
            signature = _filter_signature(filters, path=path, line_number=line_number)
            signature_without_counts = _pipeline_without_counts(signature)
            if filter_signature is None:
                filter_signature = signature_without_counts
            elif signature_without_counts != filter_signature:
                raise ValueError(f"Artifact Filter settings changed within {path}")
            for item in signature:
                filter_removed[str(item["name"])] += int(item["removed_pixel_count"])
            count += 1

    if count != expected_count:
        raise ValueError(f"expected {expected_count} per-sample records in {path}, found {count}")
    assert filter_signature is not None
    pipeline = [
        {**item, "removed_pixel_count": filter_removed[str(item["name"])]}
        for item in filter_signature
    ]
    return (
        {
            "sample_count": count,
            "sample_ids_sha256": sample_digest.hexdigest(),
            "dataset_source_counts": dict(sorted(source_counts.items())),
        },
        pipeline,
    )


def _filter_signature(
    filters: list[object],
    *,
    path: Path,
    line_number: int,
) -> list[dict[str, object]]:
    geographic, scanline = filters
    if not isinstance(geographic, Mapping) or geographic.get("filter") != "geographic_feature_filter":
        raise ValueError(f"first filter must be Geographic Feature Filter at {path}:{line_number}")
    if not isinstance(scanline, Mapping) or scanline.get("filter") != "scanline_artifact_filter":
        raise ValueError(f"second filter must be Scanline Artifact Filter at {path}:{line_number}")
    sources = geographic.get("ancillary_sources")
    source_identities = []
    if isinstance(sources, list):
        for source in sources:
            if isinstance(source, Mapping):
                source_identities.append(
                    {
                        "id": source.get("id"),
                        "version": source.get("version"),
                        "sha256": source.get("sha256"),
                        "size_bytes": source.get("size_bytes"),
                    }
                )
    return [
        {
            "name": "geographic_feature_filter",
            "active": geographic.get("active"),
            "required": geographic.get("required"),
            "bundle_id": geographic.get("bundle_id"),
            "sources": source_identities,
            "removed_pixel_count": int(geographic.get("removed_pixel_count", 0)),
        },
        {
            "name": "scanline_artifact_filter",
            "active": True,
            "min_length_pixels": int(scanline.get("min_length_pixels", -1)),
            "max_probability_std": float(scanline.get("max_probability_std", -1.0)),
            "removed_pixel_count": int(scanline.get("removed_pixel_count", 0)),
        },
    ]


def _pipeline_without_counts(pipeline: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {key: value for key, value in item.items() if key != "removed_pixel_count"}
        for item in pipeline
    ]


def _install_canonical_artifacts(*, source: Path, canonical_root: Path) -> None:
    """Copy complete evaluation directories into the self-contained canonical root."""

    # Shared source logs embed their original output-root path and are not
    # comparison artifacts. Keep the canonical bundle free of that dependency.
    (canonical_root / "baseline_evaluation.log").unlink(missing_ok=True)

    for baseline_name in MCAST_BASELINE_NAMES:
        source_dir = (source / baseline_name).resolve(strict=True)
        destination = (canonical_root / baseline_name).resolve()
        if source_dir == destination:
            continue
        staging = canonical_root / f".{baseline_name}.tmp"
        backup = canonical_root / f".{baseline_name}.backup"
        if backup.exists():
            raise RuntimeError(f"stale canonical baseline backup requires operator review: {backup}")
        if staging.exists():
            shutil.rmtree(staging)
        shutil.copytree(source_dir, staging, copy_function=shutil.copy2)
        if _directory_inventory(staging) != _directory_inventory(source_dir):
            shutil.rmtree(staging, ignore_errors=True)
            raise ValueError(f"canonical baseline copy verification failed for {baseline_name}")
        if destination.exists():
            destination.replace(backup)
        try:
            staging.replace(destination)
        except Exception:
            if backup.exists() and not destination.exists():
                backup.replace(destination)
            raise
        else:
            shutil.rmtree(backup, ignore_errors=True)


def _install_canonical_model_assets(
    *,
    baseline_records: Mapping[str, dict[str, object]],
    canonical_root: Path,
) -> None:
    """Copy model assets into ``canonical/model-assets`` and rewrite provenance paths."""

    for baseline_name, relative_path in _CANONICAL_MODEL_ASSETS.items():
        record = baseline_records[baseline_name]
        source_path = Path(str(record.pop("_source_asset_path"))).resolve(strict=True)
        destination = (canonical_root / relative_path).resolve()
        destination.parent.mkdir(parents=True, exist_ok=True)
        asset = record["asset"]
        assert isinstance(asset, dict)
        if source_path != destination:
            if source_path.is_file():
                staging_file = destination.with_name(f".{destination.name}.tmp")
                shutil.copy2(source_path, staging_file)
                _verify_model_asset(staging_file, asset, baseline_name=baseline_name)
                staging_file.replace(destination)
            elif source_path.is_dir():
                staging_dir = destination.with_name(f".{destination.name}.tmp")
                backup_dir = destination.with_name(f".{destination.name}.backup")
                if backup_dir.exists():
                    raise RuntimeError(
                        f"stale canonical model-asset backup requires operator review: {backup_dir}"
                    )
                if staging_dir.exists():
                    shutil.rmtree(staging_dir)
                shutil.copytree(source_path, staging_dir, copy_function=shutil.copy2)
                _verify_model_asset(staging_dir, asset, baseline_name=baseline_name)
                if destination.exists():
                    destination.replace(backup_dir)
                try:
                    staging_dir.replace(destination)
                except Exception:
                    if backup_dir.exists() and not destination.exists():
                        backup_dir.replace(destination)
                    raise
                else:
                    shutil.rmtree(backup_dir, ignore_errors=True)
            else:  # pragma: no cover - resolve(strict=True) plus source provenance prevents this
                raise ValueError(f"unsupported model asset type for {baseline_name}: {source_path}")
        _verify_model_asset(destination, asset, baseline_name=baseline_name)
        asset["path"] = relative_path.as_posix()


def _rewrite_canonical_model_asset_paths(
    *,
    baseline_records: Mapping[str, dict[str, object]],
    canonical_root: Path,
) -> None:
    """Make copied evaluation metadata refer only to contained model assets."""

    config_paths = {
        MCAST_BASELINE_METADATA[name].asset_config_key: (
            Path(canonical_root.name) / _CANONICAL_MODEL_ASSETS[name]
        ).as_posix()
        for name in MCAST_BASELINE_NAMES
    }
    for baseline_name in MCAST_BASELINE_NAMES:
        asset_path = _CANONICAL_MODEL_ASSETS[baseline_name].as_posix()
        evaluation_dir = canonical_root / baseline_name

        run_manifest_path = evaluation_dir / "run_manifest.json"
        run_manifest = _read_json_object(run_manifest_path)
        baseline = _required_mapping(run_manifest, "baseline", run_manifest_path)
        baseline_asset = _required_mapping(baseline, "asset", run_manifest_path)
        assert isinstance(baseline_asset, dict)
        baseline_asset["path"] = asset_path
        data_config = _required_mapping(run_manifest, "data_config", run_manifest_path)
        assert isinstance(data_config, dict)
        data_config.update(config_paths)
        _write_json_atomic(run_manifest_path, run_manifest)

        for filename in ("aggregate_metrics.json", "baseline_evaluation_metadata.json"):
            metadata_path = evaluation_dir / filename
            metadata = _read_json_object(metadata_path)
            metadata_baseline = _required_mapping(metadata, "baseline", metadata_path)
            assert isinstance(metadata_baseline, dict)
            metadata_baseline["asset_path"] = asset_path
            _write_json_atomic(metadata_path, metadata)


def _refresh_canonical_artifact_provenance(
    *,
    baseline_records: Mapping[str, dict[str, object]],
    canonical_root: Path,
) -> None:
    """Recompute checksums after canonical metadata path rewriting."""

    for record in baseline_records.values():
        artifacts = record["artifacts"]
        assert isinstance(artifacts, dict)
        for artifact in artifacts.values():
            assert isinstance(artifact, dict)
            artifact_path = (canonical_root / str(artifact["path"])).resolve(strict=True)
            artifact["sha256"] = _file_sha256(artifact_path)
            artifact["size_bytes"] = artifact_path.stat().st_size


def _verify_model_asset(
    path: Path,
    provenance: Mapping[str, object],
    *,
    baseline_name: str,
) -> None:
    kind = provenance.get("kind")
    expected_sha = provenance.get("sha256")
    expected_size = provenance.get("size_bytes")
    if not isinstance(expected_sha, str) or not isinstance(expected_size, int):
        raise ValueError(f"model asset provenance is incomplete for {baseline_name}")
    if kind == "file":
        if not path.is_file():
            raise ValueError(f"canonical model asset is not a file for {baseline_name}: {path}")
        actual_sha = _file_sha256(path)
        actual_size = path.stat().st_size
    elif kind == "directory":
        if not path.is_dir():
            raise ValueError(f"canonical model asset is not a directory for {baseline_name}: {path}")
        actual_sha, actual_size, actual_files = _directory_asset_provenance(path)
        expected_files = provenance.get("files")
        if isinstance(expected_files, list) and actual_files != expected_files:
            raise ValueError(f"model asset file provenance mismatch for {baseline_name}: {path}")
    else:
        raise ValueError(f"unsupported model asset kind for {baseline_name}: {kind!r}")
    if actual_sha != expected_sha or actual_size != expected_size:
        raise ValueError(f"model asset checksum mismatch for {baseline_name}: {path}")


def _directory_asset_provenance(
    root: Path,
) -> tuple[str, int, list[dict[str, object]]]:
    digest = hashlib.sha256()
    total_size = 0
    entries: list[dict[str, object]] = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root).as_posix()
        file_sha = _file_sha256(path)
        size = path.stat().st_size
        total_size += size
        digest.update(relative.encode("utf-8") + b"\0" + file_sha.encode("ascii") + b"\n")
        entries.append({"path": relative, "size_bytes": size, "sha256": file_sha})
    return digest.hexdigest(), total_size, entries


def _directory_inventory(root: Path) -> dict[str, tuple[int, str]]:
    return {
        path.relative_to(root).as_posix(): (path.stat().st_size, _file_sha256(path))
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _verify_registry_artifacts(
    *,
    registry_path: Path,
    baseline_name: str,
    record: Mapping[str, object],
) -> None:
    artifacts = _required_mapping(record, "artifacts", registry_path)
    for artifact_name in ("run_manifest", "aggregate_metrics", "per_sample_metrics", "threshold_sweep", "diagnostic_samples"):
        artifact = _required_mapping(artifacts, artifact_name, registry_path)
        artifact_path = _resolve_artifact_path(registry_path, artifact)
        if not artifact_path.is_file():
            raise ValueError(
                f"canonical baseline artifact does not exist for {baseline_name}: {artifact_path}"
            )
        expected_sha = artifact.get("sha256")
        if not isinstance(expected_sha, str) or _file_sha256(artifact_path) != expected_sha:
            raise ValueError(
                f"canonical baseline artifact checksum mismatch for {baseline_name}: {artifact_path}"
            )
    aggregate_path = _resolve_artifact_path(
        registry_path,
        _required_mapping(artifacts, "aggregate_metrics", registry_path),
    )
    aggregate_metrics = _required_mapping(
        _read_json_object(aggregate_path), "metrics", aggregate_path
    )
    if dict(aggregate_metrics) != dict(_required_mapping(record, "metrics", registry_path)):
        raise ValueError(f"canonical metric snapshot mismatch for {baseline_name}")


def _resolve_artifact_path(registry_path: Path, artifact: Mapping[str, object]) -> Path:
    value = artifact.get("path")
    if not isinstance(value, str) or not value:
        raise ValueError(f"canonical artifact path is missing in {registry_path}")
    path = Path(value).expanduser()
    if path.is_absolute():
        raise ValueError(f"canonical artifact path must be relative in {registry_path}: {value}")
    resolved = (registry_path.parent / path).resolve()
    try:
        resolved.relative_to(registry_path.parent)
    except ValueError as exc:
        raise ValueError(
            f"canonical artifact path must stay beneath {registry_path.parent}: {value}"
        ) from exc
    return resolved


def _validate_metric_namespaces(metrics: Mapping[str, object], *, baseline_name: str) -> None:
    missing = [
        f"{namespace}/{metric}"
        for namespace in ("raw", "filtered")
        for metric in _REQUIRED_METRICS
        if f"{namespace}/{metric}" not in metrics
    ]
    if missing:
        raise ValueError(f"baseline {baseline_name} is missing canonical metrics: {missing}")


def _required_mapping(payload: Mapping[str, object], key: str, path: Path) -> Mapping[str, Any]:
    value = payload.get(key)
    if not isinstance(value, Mapping):
        raise ValueError(f"{key} must be an object in {path}")
    return value


def _required_positive_int(value: object, key: str, path: Path) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{key} must be a positive integer in {path}")
    return value


def _read_json_object(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text())
    except FileNotFoundError as exc:
        raise ValueError(f"required baseline artifact does not exist: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON baseline artifact: {path}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"baseline artifact must contain a JSON object: {path}")
    return payload


def _write_json_atomic(path: Path, payload: Mapping[str, object]) -> None:
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate or verify canonical ABI MCAST comparison targets."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    generate_parser = subparsers.add_parser("generate")
    generate_parser.add_argument("--source-root", type=Path, required=True)
    generate_parser.add_argument("--output", type=Path, required=True)
    generate_parser.add_argument("--registry-id", default=DEFAULT_REGISTRY_ID)
    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("--registry", type=Path, required=True)
    args = parser.parse_args(argv)

    if args.command == "generate":
        registry = generate_canonical_baseline_targets(
            source_root=args.source_root,
            output_path=args.output,
            registry_id=args.registry_id,
        )
        result = {
            "status": "generated_and_verified",
            "registry": str(args.output.expanduser().resolve()),
            "registry_id": registry["registry_id"],
            "baselines": sorted(registry["baselines"]),
        }
    else:
        registry = load_canonical_baseline_targets(args.registry, verify_artifacts=True)
        result = {
            "status": "verified",
            "registry": str(args.registry.expanduser().resolve()),
            "registry_id": registry["registry_id"],
            "baselines": sorted(registry["baselines"]),
        }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


__all__ = [
    "CANONICAL_TARGETS_CONFIG_KEY",
    "DEFAULT_REGISTRY_ID",
    "REGISTRY_SCHEMA",
    "canonical_baseline_metrics",
    "generate_canonical_baseline_targets",
    "load_canonical_baseline_targets",
    "main",
    "resolve_canonical_baseline_targets_path",
]


if __name__ == "__main__":
    raise SystemExit(main())
