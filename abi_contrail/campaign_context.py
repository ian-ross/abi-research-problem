"""Trusted generator for the Agent-visible ABI campaign context artifact."""

from __future__ import annotations

import argparse
import hashlib
import json
import tomllib
from collections.abc import Mapping
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import abi_contrail.profile as dataset_profile_module
from abi_contrail.adapters import RESEARCH_PROBLEM_ID, RESEARCH_PROBLEM_VERSION
from abi_contrail.baseline_segmenters import MCAST_BASELINE_NAMES
from abi_contrail.baseline_targets import (
    load_canonical_baseline_targets,
    resolve_canonical_baseline_targets_path,
)
from abi_contrail.profile import generate_dataset_profile

CAMPAIGN_CONTEXT_SCHEMA = "abi_agent_campaign_context/v1"
GENERATOR_VERSION = "abi_contrail.campaign_context.v1"
_METRIC_NAMES = ("dice", "precision", "recall", "contrail_connectivity")
_FORBIDDEN_KEYS = {
    "asset",
    "assets",
    "candidate_source",
    "data_roots",
    "host_data_path",
    "longitude",
    "latitude",
    "model_artifact",
    "model_weights",
    "predictions",
    "raw_samples",
}
_FORBIDDEN_FILE_SUFFIXES = (".pt", ".pth", ".ckpt", ".tif", ".npy")


def generate_agent_campaign_context(
    data_config: Mapping[str, object],
    *,
    registry_path: str | Path,
    run_dir: str | Path,
    evaluation_dir: str | Path,
    workspace_config_sha256: str | None = None,
    generation_timestamp: str | None = None,
) -> dict[str, Any]:
    """Generate the whitelisted context without executing candidate code."""

    registry_file = Path(registry_path).expanduser().resolve(strict=True)
    run_root = Path(run_dir).expanduser().resolve(strict=True)
    evaluation_root = Path(evaluation_dir).expanduser().resolve(strict=True)
    registry = load_canonical_baseline_targets(registry_file, verify_artifacts=True)
    dataset_profile = generate_dataset_profile(data_config)

    artifact = {
        "artifact_type": "agent_campaign_context",
        "schema": CAMPAIGN_CONTEXT_SCHEMA,
        "provenance": {
            "research_problem_id": RESEARCH_PROBLEM_ID,
            "research_problem_version": RESEARCH_PROBLEM_VERSION,
            "generation_timestamp": generation_timestamp or _timestamp(),
            "generation_version": GENERATOR_VERSION,
            "generator_source_sha256": _file_sha256(Path(__file__).resolve()),
            "dataset_profile_generator_source_sha256": _file_sha256(
                Path(str(dataset_profile_module.__file__)).resolve()
            ),
            "generation_command": (
                "uv run abi-campaign-context --workspace-config ml-autoresearch.toml "
                "--run <ABI-025_RUN_DIR> --evaluation <ABI-025_EVALUATION_DIR> "
                "--output abi_contrail/profile/agent-campaign-context.v1.json"
            ),
            "workspace_configuration_sha256": workspace_config_sha256,
            "input_checksums": {
                "canonical_registry_sha256": _file_sha256(registry_file),
                **_canary_input_checksums(run_root, evaluation_root),
            },
        },
        "safety_contract": {
            "content_policy": "aggregate summaries and immutable identities only",
            "candidate_input_policy": "ABI channels 1-16 only; coordinate source channels 16 and 17 are excluded",
            "excluded_content": [
                "raw training samples and qualitative sample pixels",
                "coordinate arrays or coordinate-derived candidate features",
                "baseline or candidate model weights",
                "unrestricted training, ancillary, baseline, Run, or evaluation artifact roots",
                "candidate-owned data loading, losses, metrics, Artifact Filters, or sampling logic",
            ],
            "authority_note": "Summary context only; not a new authoritative Run Result or promotion decision.",
        },
        "dataset_profile": dataset_profile,
        "canonical_mcast": _canonical_mcast_context(registry_file, registry),
        "abi_025_manual_canary": _manual_canary_context(
            run_root, evaluation_root, expected_registry_id=str(registry["registry_id"])
        ),
    }
    validate_agent_campaign_context(artifact)
    return artifact


def validate_agent_campaign_context(artifact: Mapping[str, object]) -> None:
    """Validate the schema and reject boundary-sensitive serialized content."""

    if artifact.get("schema") != CAMPAIGN_CONTEXT_SCHEMA:
        raise ValueError(f"unsupported Agent Campaign Context schema: {artifact.get('schema')!r}")
    required = {
        "artifact_type",
        "schema",
        "provenance",
        "safety_contract",
        "dataset_profile",
        "canonical_mcast",
        "abi_025_manual_canary",
    }
    if set(artifact) != required:
        raise ValueError(f"Agent Campaign Context top-level fields must be exactly {sorted(required)}")
    if artifact.get("artifact_type") != "agent_campaign_context":
        raise ValueError("Agent Campaign Context artifact_type is invalid")

    def inspect(value: object, location: str) -> None:
        if isinstance(value, Mapping):
            for raw_key, item in value.items():
                key = str(raw_key)
                lowered_key = key.lower()
                if (
                    lowered_key in _FORBIDDEN_KEYS
                    or lowered_key.startswith(("longitude_", "latitude_"))
                    or "per_sample" in lowered_key
                    or "diagnostic_sample" in lowered_key
                ):
                    raise ValueError(f"forbidden Agent Campaign Context field at {location}.{key}")
                inspect(item, f"{location}.{key}")
        elif isinstance(value, list):
            for index, item in enumerate(value):
                inspect(item, f"{location}[{index}]")
        elif isinstance(value, str):
            if value.startswith(("/", "file://")) or "\\" in value or ".." in Path(value).parts:
                raise ValueError(f"host-only or escaping path leaked at {location}")
            lowered = value.lower()
            if lowered.endswith(_FORBIDDEN_FILE_SUFFIXES) or "model-assets/" in lowered:
                raise ValueError(f"model or unrestricted artifact reference leaked at {location}")

    inspect(artifact, "artifact")
    json.dumps(artifact, allow_nan=False)


def load_agent_campaign_context(path: str | Path) -> dict[str, Any]:
    payload = _read_json_object(Path(path).expanduser().resolve(strict=True))
    validate_agent_campaign_context(payload)
    return payload


def load_workspace_data_config(path: str | Path) -> tuple[dict[str, object], str]:
    config_path = Path(path).expanduser().resolve(strict=True)
    workspace = tomllib.loads(config_path.read_text())
    research_problem = workspace.get("research_problem")
    if not isinstance(research_problem, Mapping):
        raise ValueError("Workspace Configuration is missing [research_problem]")
    raw_data_config = research_problem.get("data_config", {})
    raw_data_roots = research_problem.get("data_roots", {})
    if not isinstance(raw_data_config, Mapping) or not isinstance(raw_data_roots, Mapping):
        raise ValueError("Workspace Configuration research_problem data_config/data_roots must be tables")
    data_config = dict(raw_data_config)
    data_config["data_roots"] = dict(raw_data_roots)
    return data_config, _file_sha256(config_path)


def _canonical_mcast_context(
    registry_path: Path, registry: Mapping[str, object]
) -> dict[str, Any]:
    baselines = _required_mapping(registry, "baselines", registry_path)
    records = {}
    for baseline_name in MCAST_BASELINE_NAMES:
        record = _required_mapping(baselines, baseline_name, registry_path)
        artifacts = _required_mapping(record, "artifacts", registry_path)
        aggregate_ref = _required_mapping(artifacts, "aggregate_metrics", registry_path)
        threshold_ref = _required_mapping(artifacts, "threshold_sweep", registry_path)
        aggregate = _read_json_object(
            _resolve_registry_artifact(registry_path, aggregate_ref)
        )
        threshold = _read_json_object(
            _resolve_registry_artifact(registry_path, threshold_ref)
        )
        metrics = _required_mapping(record, "metrics", registry_path)
        raw = _metric_view(metrics, "raw")
        filtered = _metric_view(metrics, "filtered")
        records[baseline_name] = {
            "name": baseline_name,
            "version": record.get("version"),
            "sample_count": record.get("sample_count"),
            "completed_at": record.get("completed_at"),
            "default_threshold": aggregate.get("threshold", threshold.get("default_threshold")),
            "aggregate_metrics": {
                "raw": raw,
                "artifact_filtered": filtered,
                "by_dataset_source": {
                    source: {
                        "raw": _metric_view(metrics, f"source/{source}/raw"),
                        "artifact_filtered": _metric_view(
                            metrics, f"source/{source}/filtered"
                        ),
                    }
                    for source in ("mit", "google")
                },
            },
            "threshold_behavior": _threshold_behavior(threshold),
            "artifact_filter_effect": {
                "removed_pixel_counts": dict(
                    _required_mapping(record, "filter_removed_pixel_counts", registry_path)
                ),
                "removed_area_km2": metrics.get("artifact_filters/removed_area_km2"),
                "filtered_minus_raw": {
                    metric: _numeric_delta(filtered.get(metric), raw.get(metric))
                    for metric in _METRIC_NAMES
                },
            },
            "artifact_checksums": {
                "aggregate_metrics_sha256": aggregate_ref.get("sha256"),
                "aggregate_metrics_size_bytes": aggregate_ref.get("size_bytes"),
                "threshold_sweep_sha256": threshold_ref.get("sha256"),
                "threshold_sweep_size_bytes": threshold_ref.get("size_bytes"),
            },
        }

    return {
        "registry": {
            "id": registry.get("registry_id"),
            "schema": registry.get("schema"),
            "generated_at": registry.get("generated_at"),
            "sha256": _file_sha256(registry_path),
        },
        "sample_set": registry.get("sample_set"),
        "comparison_modes": registry.get("comparison_modes"),
        "provenance": _safe_git_provenance(registry.get("provenance")),
        "baselines": records,
    }


def _manual_canary_context(
    run_dir: Path, evaluation_dir: Path, *, expected_registry_id: str
) -> dict[str, Any]:
    run_metadata = _read_json_object(run_dir / "run_metadata.json")
    evaluation_metadata = _read_json_object(evaluation_dir / "evaluation_metadata.json")
    aggregate = _read_json_object(evaluation_dir / "aggregate_metrics.json")
    threshold = _read_json_object(evaluation_dir / "threshold_sweep.json")
    acceptance = _read_json_object(evaluation_dir / "acceptance_report.json")

    run_id = _required_string(run_metadata, "run_id", run_dir)
    evaluation_id = _required_string(evaluation_metadata, "evaluation_id", evaluation_dir)
    if run_metadata.get("status") != "completed" or evaluation_metadata.get("status") != "completed":
        raise ValueError("ABI-025 Run and Post-Run Evaluation must both be completed")
    source_run = _required_mapping(evaluation_metadata, "source_run", evaluation_dir)
    if source_run.get("run_id") != run_id or acceptance.get("candidate_run_id") != run_id:
        raise ValueError("ABI-025 Run/Evaluation/acceptance-report identity mismatch")
    if aggregate.get("evaluation_id") != evaluation_id:
        raise ValueError("ABI-025 aggregate metrics evaluation identity mismatch")
    registry_summary = _required_mapping(acceptance, "baseline_target_registry", evaluation_dir)
    if registry_summary.get("id") != expected_registry_id:
        raise ValueError("ABI-025 acceptance report canonical registry identity mismatch")

    metrics = _required_mapping(aggregate, "metrics", evaluation_dir)
    candidate_source = _required_mapping(run_metadata, "candidate_source", run_dir)
    candidate_name = Path(str(candidate_source.get("path", "unknown"))).name
    dataset = _required_mapping(run_metadata, "dataset", run_dir)
    flags = acceptance.get("flags", [])
    if not isinstance(flags, list):
        raise ValueError("ABI-025 acceptance report flags must be a list")

    return {
        "task_id": "ABI-025",
        "purpose": "manual end-to-end lifecycle canary; scientific quality was not the success criterion",
        "candidate_name": candidate_name,
        "run": {
            "id": run_id,
            "status": run_metadata.get("status"),
            "created_at": run_metadata.get("created_at"),
            "updated_at": run_metadata.get("updated_at"),
            "input_mode": dataset.get("input_mode"),
            "bounded_sample_counts": run_metadata.get("sample_counts"),
            "training_policy": run_metadata.get("training_policy"),
        },
        "post_run_evaluation": {
            "id": evaluation_id,
            "status": evaluation_metadata.get("status"),
            "completed_at": evaluation_metadata.get("completed_at"),
            "mode": evaluation_metadata.get("mode"),
            "sample_count": aggregate.get("sample_count"),
            "threshold": aggregate.get("threshold"),
            "aggregate_metrics": {
                "raw": _metric_view(metrics, "raw"),
                "artifact_filtered": _metric_view(metrics, "filtered"),
                "by_dataset_source": {
                    source: {
                        "raw": _metric_view(metrics, f"source/{source}/raw"),
                        "artifact_filtered": _metric_view(
                            metrics, f"source/{source}/filtered"
                        ),
                    }
                    for source in ("mit", "google")
                },
            },
            "threshold_behavior": _threshold_behavior(threshold),
        },
        "acceptance_context": {
            "canonical_registry_id": expected_registry_id,
            "overall_status": acceptance.get("overall_status"),
            "promotion_decision": acceptance.get("promotion_decision"),
            "human_review_required": acceptance.get("human_review_required"),
            "human_review_note": acceptance.get("human_review_note"),
            "best_baseline": _whitelist_fields(
                acceptance.get("best_baseline"),
                ("name", "selection_metric", "selection_value", "target_registry_id"),
            ),
            "aggregate_comparison": _whitelist_fields(
                acceptance.get("aggregate_comparison"),
                ("baseline", "baseline_name", "candidate", "candidate_beats_baseline", "delta", "metric", "target_registry_id"),
            ),
            "connectivity_comparison": acceptance.get(
                "contrail_connectivity_comparison"
            ),
            "recall_regression": acceptance.get("recall_regression"),
            "dataset_source_failures": acceptance.get("dataset_source_failures"),
            "artifact_filter_dependence": acceptance.get("artifact_filter_dependence"),
            "flags": [
                _whitelist_fields(
                    flag,
                    ("id", "severity", "message", "metric", "source", "candidate", "baseline", "delta"),
                )
                for flag in flags
            ],
        },
    }


def _threshold_behavior(threshold: Mapping[str, object]) -> dict[str, Any]:
    values = threshold.get("thresholds", [])
    if not isinstance(values, list):
        raise ValueError("threshold_sweep thresholds must be a list")
    return {
        "evaluated_threshold_count": len(values),
        "evaluated_threshold_min": min(values) if values else None,
        "evaluated_threshold_max": max(values) if values else None,
        "best_by_raw_dice": threshold.get("best_threshold_by_raw_dice"),
        "best_by_artifact_filtered_dice": threshold.get(
            "best_threshold_by_filtered_dice"
        ),
        "precision_recall_balance_raw": threshold.get(
            "precision_recall_equal_threshold_raw"
        ),
        "precision_recall_balance_artifact_filtered": threshold.get(
            "precision_recall_equal_threshold"
        ),
        "interpretation": threshold.get("primary_metric_note"),
    }


def _metric_view(metrics: Mapping[str, object], prefix: str) -> dict[str, object]:
    return {
        name: metrics.get(f"{prefix}/{name}")
        for name in _METRIC_NAMES
        if f"{prefix}/{name}" in metrics
    }


def _numeric_delta(filtered: object, raw: object) -> float | None:
    if isinstance(filtered, (int, float)) and isinstance(raw, (int, float)):
        return float(filtered) - float(raw)
    return None


def _safe_git_provenance(value: object) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        return {}
    result = {}
    for name in ("workspace_git", "harness_git"):
        record = value.get(name)
        if isinstance(record, Mapping):
            result[name] = {
                key: record.get(key) for key in ("commit", "dirty") if key in record
            }
    return result


def _canary_input_checksums(run_dir: Path, evaluation_dir: Path) -> dict[str, str]:
    files = {
        "abi_025_run_metadata_sha256": run_dir / "run_metadata.json",
        "abi_025_evaluation_metadata_sha256": evaluation_dir / "evaluation_metadata.json",
        "abi_025_aggregate_metrics_sha256": evaluation_dir / "aggregate_metrics.json",
        "abi_025_threshold_sweep_sha256": evaluation_dir / "threshold_sweep.json",
        "abi_025_acceptance_report_sha256": evaluation_dir / "acceptance_report.json",
    }
    return {name: _file_sha256(path.resolve(strict=True)) for name, path in files.items()}


def _resolve_registry_artifact(
    registry_path: Path, artifact: Mapping[str, object]
) -> Path:
    relative = artifact.get("path")
    if not isinstance(relative, str) or not relative:
        raise ValueError("canonical registry artifact reference is missing")
    resolved = (registry_path.parent / relative).resolve(strict=True)
    try:
        resolved.relative_to(registry_path.parent)
    except ValueError as exc:
        raise ValueError("canonical registry artifact reference escapes its root") from exc
    return resolved


def _whitelist_fields(value: object, fields: tuple[str, ...]) -> dict[str, object]:
    if not isinstance(value, Mapping):
        return {}
    return {field: value[field] for field in fields if field in value}


def _required_mapping(
    payload: Mapping[str, object], key: str, location: Path
) -> Mapping[str, Any]:
    value = payload.get(key)
    if not isinstance(value, Mapping):
        raise ValueError(f"{key} must be an object in {location}")
    return value


def _required_string(payload: Mapping[str, object], key: str, location: Path) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{key} must be a non-empty string in {location}")
    return value


def _read_json_object(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text())
    except FileNotFoundError as exc:
        raise ValueError(f"required campaign-context input is missing: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON campaign-context input: {path}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"campaign-context input must be a JSON object: {path}")
    return payload


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
        description="Generate and validate the trusted Agent-visible ABI campaign context."
    )
    parser.add_argument("--workspace-config", type=Path, default=Path("ml-autoresearch.toml"))
    parser.add_argument("--run", type=Path, required=True, help="Completed ABI-025 Run directory")
    parser.add_argument(
        "--evaluation", type=Path, required=True, help="Completed ABI-025 Post-Run Evaluation directory"
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)

    data_config, workspace_sha = load_workspace_data_config(args.workspace_config)
    registry_path = resolve_canonical_baseline_targets_path(data_config)
    artifact = generate_agent_campaign_context(
        data_config,
        registry_path=registry_path,
        run_dir=args.run,
        evaluation_dir=args.evaluation,
        workspace_config_sha256=workspace_sha,
    )
    output = args.output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(f".{output.name}.tmp")
    temporary.write_text(json.dumps(artifact, indent=2, sort_keys=True, allow_nan=False) + "\n")
    temporary.replace(output)
    load_agent_campaign_context(output)
    print(
        json.dumps(
            {
                "status": "generated_and_validated",
                "schema": CAMPAIGN_CONTEXT_SCHEMA,
                "output": str(output),
                "sha256": _file_sha256(output),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "CAMPAIGN_CONTEXT_SCHEMA",
    "generate_agent_campaign_context",
    "load_agent_campaign_context",
    "load_workspace_data_config",
    "main",
    "validate_agent_campaign_context",
]
