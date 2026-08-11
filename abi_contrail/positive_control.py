"""Provider-owned ABI-031 positive-control acceptance reporting."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Mapping

import torch

EXPECTED_CANDIDATE_ID = "abi031_mcast11_positive_control_v1"
EXPECTED_VALIDATION_SAMPLES = 3_088
PIXELS_PER_SAMPLE = 256 * 256
MIN_PREDICTED_POSITIVE_FRACTION = 0.00001
MAX_PREDICTED_POSITIVE_FRACTION = 0.10
MIN_DICE = 0.0001


def build_positive_control_report(
    *,
    run_dir: Path,
    evaluation_dir: Path,
    ledger_path: Path,
    expected_candidate_sha256: str,
) -> dict[str, object]:
    """Evaluate preregistered ABI-031 criteria from trusted Run artifacts."""

    run_dir = run_dir.resolve()
    evaluation_dir = evaluation_dir.resolve()
    run_metadata = _read_object(run_dir / "run_metadata.json")
    aggregate = _read_object(evaluation_dir / "aggregate_metrics.json")
    evaluation_metadata = _read_object(evaluation_dir / "evaluation_metadata.json")
    metrics = _mapping(aggregate.get("metrics"), "aggregate_metrics.metrics")
    run_id = str(run_metadata.get("run_id") or run_dir.name)
    sample_count = int(aggregate.get("sample_count", 0))
    total_pixels = sample_count * PIXELS_PER_SAMPLE
    min_positive_pixels = math.ceil(total_pixels * MIN_PREDICTED_POSITIVE_FRACTION)
    max_positive_pixels = math.floor(total_pixels * MAX_PREDICTED_POSITIVE_FRACTION)

    checkpoint_path = run_dir / "outputs" / "models" / "best_epoch_model.pt"
    checkpoint_finite, checkpoint_tensor_count, checkpoint_value_count = _checkpoint_finite(checkpoint_path)
    metrics_finite, metric_value_count = _jsonl_numbers_finite(run_dir / "outputs" / "metrics.jsonl")
    terminal_metrics_finite = _all_numbers_finite(_read_object(run_dir / "outputs" / "final_metrics.json")) and _all_numbers_finite(
        _read_object(run_dir / "outputs" / "best_metrics.json")
    )
    aggregate_finite = _all_numbers_finite(aggregate)

    raw_positive = _metric(metrics, "raw/predicted_positive_pixel_count")
    filtered_positive = _metric(metrics, "filtered/predicted_positive_pixel_count")
    dice_keys = (
        "raw/dice",
        "filtered/dice",
        "source/mit/raw/dice",
        "source/mit/filtered/dice",
        "source/google/raw/dice",
        "source/google/filtered/dice",
    )
    dice_values = {key: _metric(metrics, key) for key in dice_keys}

    candidate_dir = run_dir / "candidate"
    candidate_sha256 = candidate_tree_sha256(candidate_dir)
    source_text = (candidate_dir / "model.py").read_text()
    boundary_passed = all(
        token not in source_text
        for token in ("longitude", "latitude", "baseline", "torch.load", "open(", "Path(")
    )
    random_initialization_passed = "encoder_weights=None" in source_text and "load_state_dict" not in source_text

    required_artifacts = (
        run_dir / "run_metadata.json",
        run_dir / "execution.json",
        run_dir / "resolved_manifest.yaml",
        run_dir / "outputs" / "model_summary.json",
        run_dir / "outputs" / "resource_profile.json",
        run_dir / "outputs" / "metrics.jsonl",
        run_dir / "outputs" / "final_metrics.json",
        run_dir / "outputs" / "best_metrics.json",
        checkpoint_path,
        evaluation_dir / "evaluation_metadata.json",
        evaluation_dir / "aggregate_metrics.json",
        evaluation_dir / "per_sample_metrics.jsonl",
        evaluation_dir / "threshold_sweep.json",
        evaluation_dir / "diagnostic_samples" / "samples.json",
        evaluation_dir / "acceptance_report.json",
    )
    missing_artifacts = [str(path.relative_to(run_dir)) for path in required_artifacts if not path.is_file()]
    ledger_records = _ledger_records_for_run(ledger_path, run_id)
    terminal_events = [
        record for record in ledger_records if record.get("event_type") in {"run_completed", "run_failed"}
    ]
    evaluation_events = [record for record in ledger_records if record.get("event_type") == "evaluation_completed"]

    acceptance_report = _read_object(evaluation_dir / "acceptance_report.json") if (evaluation_dir / "acceptance_report.json").is_file() else {}
    registry_id = _mapping(acceptance_report.get("baseline_target_registry", {}), "baseline_target_registry").get("id")
    candidate_id = _candidate_id(run_dir)
    linked_evaluation_run_id = str(_mapping(evaluation_metadata.get("source_run"), "evaluation_metadata.source_run").get("run_id") or "")

    criteria = [
        _criterion("finite_numerical_state", metrics_finite and terminal_metrics_finite and aggregate_finite, {
            "logged_metric_value_count": metric_value_count,
            "terminal_metrics_finite": terminal_metrics_finite,
            "aggregate_metrics_finite": aggregate_finite,
        }),
        _criterion("finite_checkpoint", checkpoint_finite, {
            "checkpoint_tensor_count": checkpoint_tensor_count,
            "checkpoint_value_count": checkpoint_value_count,
        }),
        _criterion("raw_prediction_non_degeneracy", min_positive_pixels <= raw_positive <= max_positive_pixels, {
            "observed": raw_positive,
            "minimum": min_positive_pixels,
            "maximum": max_positive_pixels,
            "total_pixels": total_pixels,
        }),
        _criterion("filtered_prediction_non_degeneracy", 0 < filtered_positive <= raw_positive, {
            "observed": filtered_positive,
            "raw_observed": raw_positive,
        }),
        _criterion("aggregate_dice_above_floor", dice_values["raw/dice"] > MIN_DICE and dice_values["filtered/dice"] > MIN_DICE, {
            "minimum_exclusive": MIN_DICE,
            "raw/dice": dice_values["raw/dice"],
            "filtered/dice": dice_values["filtered/dice"],
        }),
        _criterion("source_stratified_dice_above_floor", all(dice_values[key] > MIN_DICE for key in dice_keys[2:]), {
            "minimum_exclusive": MIN_DICE,
            **{key: dice_values[key] for key in dice_keys[2:]},
        }),
        _criterion("artifact_and_ledger_completeness", not missing_artifacts and len(terminal_events) == 1 and len(evaluation_events) == 1, {
            "missing_artifacts": missing_artifacts,
            "terminal_event_count": len(terminal_events),
            "evaluation_completed_event_count": len(evaluation_events),
        }),
        _criterion("candidate_boundary_and_provenance", candidate_id == EXPECTED_CANDIDATE_ID and candidate_sha256 == expected_candidate_sha256 and boundary_passed and random_initialization_passed and linked_evaluation_run_id == run_id and registry_id == "abi-mcast-working-validation-v1" and sample_count == EXPECTED_VALIDATION_SAMPLES, {
            "candidate_id": candidate_id,
            "candidate_sha256": candidate_sha256,
            "expected_candidate_sha256": expected_candidate_sha256,
            "source_boundary_passed": boundary_passed,
            "random_initialization_source_passed": random_initialization_passed,
            "linked_evaluation_run_id": linked_evaluation_run_id,
            "registry_id": registry_id,
            "sample_count": sample_count,
        }),
    ]
    passed = all(bool(item["passed"]) for item in criteria)
    return {
        "report_type": "abi031_positive_control_report",
        "candidate_run_id": run_id,
        "evaluation_id": evaluation_metadata.get("evaluation_id"),
        "hypothesis_passed": passed,
        "decision": "positive_control_passed" if passed else "positive_control_failed",
        "beating_mcast_required": False,
        "criteria": criteria,
        "human_review_required": True,
    }


def write_positive_control_report(**kwargs: Any) -> Path:
    evaluation_dir = Path(kwargs["evaluation_dir"])
    report = build_positive_control_report(**kwargs)
    output = evaluation_dir / "positive_control_report.json"
    output.write_text(json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n")
    return output


def write_acceptance_report(*, workspace_root: Path, run_dir: Path, evaluation_dir: Path) -> Path:
    """Write the ordinary promotion-oriented provider acceptance report."""

    from ml_autoresearch.candidate_execution_config import load_candidate_execution_config
    from abi_contrail.research_problem import build_spec

    config = load_candidate_execution_config(workspace_root)
    provider = config.research_problem_provider
    if provider is None:
        raise ValueError("configured ABI Research Problem provider is required")
    spec = build_spec(provider.effective_data_config())
    adapter = spec.evaluation_adapter
    if adapter is None:
        raise ValueError("configured ABI evaluation adapter is required")
    aggregate = _read_object(evaluation_dir / "aggregate_metrics.json")
    metrics = _mapping(aggregate.get("metrics"), "aggregate_metrics.metrics")
    run_metadata = _read_object(run_dir / "run_metadata.json")
    output = evaluation_dir / "acceptance_report.json"
    adapter.build_acceptance_gate_report(
        candidate_metrics=metrics,
        candidate_run_id=str(run_metadata.get("run_id") or run_dir.name),
        output_path=output,
    )
    return output


def candidate_tree_sha256(candidate_dir: Path) -> str:
    """Hash the four contract source files, excluding interpreter caches."""

    digest = hashlib.sha256()
    for name in ("PROPOSAL.md", "README.md", "manifest.yaml", "model.py"):
        path = candidate_dir / name
        if not path.is_file():
            raise ValueError(f"required Candidate source file is missing: {path}")
        digest.update(name.encode() + b"\0" + path.read_bytes() + b"\0")
    return digest.hexdigest()


def _checkpoint_finite(path: Path) -> tuple[bool, int, int]:
    checkpoint = torch.load(path, map_location="cpu", weights_only=True)
    state = checkpoint.get("model_state_dict") if isinstance(checkpoint, dict) else None
    if not isinstance(state, dict) or not state:
        return False, 0, 0
    tensors = [value for value in state.values() if isinstance(value, torch.Tensor)]
    return all(bool(torch.isfinite(tensor).all()) for tensor in tensors), len(tensors), sum(tensor.numel() for tensor in tensors)


def _jsonl_numbers_finite(path: Path) -> tuple[bool, int]:
    count = 0
    finite = True
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        payload = json.loads(line)
        numbers = list(_numbers(payload))
        count += len(numbers)
        finite = finite and all(math.isfinite(value) for value in numbers)
    return finite, count


def _all_numbers_finite(value: object) -> bool:
    return all(math.isfinite(number) for number in _numbers(value))


def _numbers(value: object):
    if isinstance(value, bool):
        return
    if isinstance(value, (int, float)):
        yield float(value)
    elif isinstance(value, Mapping):
        for item in value.values():
            yield from _numbers(item)
    elif isinstance(value, list):
        for item in value:
            yield from _numbers(item)


def _ledger_records_for_run(path: Path, run_id: str) -> list[dict[str, object]]:
    records = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        if record.get("run_id") == run_id:
            records.append(record)
    return records


def _candidate_id(run_dir: Path) -> str:
    import yaml

    manifest = yaml.safe_load((run_dir / "resolved_manifest.yaml").read_text())
    return str(manifest.get("name") if isinstance(manifest, dict) else "")


def _metric(metrics: Mapping[str, object], key: str) -> float:
    value = metrics.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(float(value)):
        raise ValueError(f"required finite metric is missing: {key}")
    return float(value)


def _mapping(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be a mapping")
    return value


def _read_object(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _criterion(identifier: str, passed: bool, evidence: dict[str, object]) -> dict[str, object]:
    return {"id": identifier, "passed": bool(passed), "evidence": evidence}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--evaluation", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--workspace-root", type=Path, default=Path("."))
    parser.add_argument("--expected-candidate-sha256", required=True)
    args = parser.parse_args()
    write_acceptance_report(
        workspace_root=args.workspace_root,
        run_dir=args.run,
        evaluation_dir=args.evaluation,
    )
    output = write_positive_control_report(
        run_dir=args.run,
        evaluation_dir=args.evaluation,
        ledger_path=args.ledger,
        expected_candidate_sha256=args.expected_candidate_sha256,
    )
    print(output)


__all__ = [
    "EXPECTED_CANDIDATE_ID",
    "build_positive_control_report",
    "candidate_tree_sha256",
    "write_acceptance_report",
    "write_positive_control_report",
]
