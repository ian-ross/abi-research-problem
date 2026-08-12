"""Provider-owned conservative assessment of bounded ABI scout evidence."""

from __future__ import annotations

import json
import math
from collections import defaultdict
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path

SCHEMA_VERSION = "abi_scout_assessment.v1"
DEFAULT_SCOUT_EPOCH_BUDGET = 12
RECENT_TREND_EPOCHS = 4
PERSISTENT_DEGENERACY_EPOCHS = 3
_DEGENERATE_FRACTION = 1e-6
_TREND_TOLERANCE = 1e-6


def build_scout_assessment(
    metric_records: Iterable[Mapping[str, object]],
    *,
    resource_state: Mapping[str, object] | None = None,
    scout_epoch_budget: int = DEFAULT_SCOUT_EPOCH_BUDGET,
) -> dict[str, object]:
    """Summarize trusted scout evidence without ranking architectures by score.

    The recommendation is deliberately asymmetric: hard/non-finite failures and
    persistent prediction collapse support elimination. Low scores alone never
    do. Improving, source-balanced, novel, noisy, or otherwise ambiguous finite
    trajectories remain extension-eligible.
    """

    if scout_epoch_budget < 1:
        raise ValueError("scout_epoch_budget must be positive")
    records = [dict(record) for record in metric_records]
    finite_state = _finite_state(records)
    validation_records = sorted(
        (record for record in records if record.get("split") == "val" and _epoch(record) is not None),
        key=lambda record: int(record["epoch"]),
    )
    train_losses = _epoch_train_losses(records)
    primary_values = _series(validation_records, "val/filtered_dice")
    loss_values = [(epoch, value) for epoch, value in train_losses]
    latest = validation_records[-1] if validation_records else {}
    epochs_observed = int(latest.get("epoch", 0)) if latest else 0

    loss_trend = _trend_summary(loss_values, lower_is_better=True)
    metric_trend = _trend_summary(primary_values, lower_is_better=False)
    source_behavior = {
        source: _source_summary(validation_records, source)
        for source in ("mit", "google")
    }
    degeneracy = _prediction_degeneracy(validation_records)
    resource = _resource_summary(resource_state or {})

    strong_negative_evidence: list[str] = []
    if not finite_state["all_finite"]:
        strong_negative_evidence.append("non_finite_evidence")
    if resource["hard_failure"]:
        strong_negative_evidence.append("hard_failure")
    if degeneracy["persistent"]:
        strong_negative_evidence.append("persistent_prediction_collapse")

    at_budget = epochs_observed >= scout_epoch_budget
    convincing_divergence = bool(
        at_budget
        and loss_trend["direction"] == "worsening"
        and metric_trend["direction"] == "worsening"
        and int(loss_trend["points"]) >= RECENT_TREND_EPOCHS
        and int(metric_trend["points"]) >= RECENT_TREND_EPOCHS
    )
    if convincing_divergence:
        strong_negative_evidence.append("convincing_loss_metric_divergence_at_budget")

    plateau_review = bool(
        at_budget
        and _is_recent_plateau(loss_values)
        and _is_recent_plateau(primary_values)
        and not strong_negative_evidence
    )
    improving = loss_trend["direction"] == "improving" or metric_trend["direction"] == "improving"
    source_signal = all(summary["latest_filtered_dice"] is not None for summary in source_behavior.values())
    ambiguous = not strong_negative_evidence and (
        epochs_observed < scout_epoch_budget
        or improving
        or metric_trend["direction"] == "ambiguous"
        or loss_trend["direction"] == "ambiguous"
        or source_signal
    )

    elimination_supported = bool(strong_negative_evidence)
    if elimination_supported:
        recommendation = "elimination_supported"
    elif plateau_review:
        recommendation = "human_review_at_scout_budget"
    else:
        recommendation = "extension_eligible"

    return {
        "schema_version": SCHEMA_VERSION,
        "policy": {
            "kind": "conservative_feasibility_assessment",
            "strict_top_k": False,
            "absolute_dice_elimination_threshold": None,
            "scout_epoch_budget": scout_epoch_budget,
            "recent_trend_epochs": RECENT_TREND_EPOCHS,
            "persistent_degeneracy_epochs": PERSISTENT_DEGENERACY_EPOCHS,
        },
        "finite_state": finite_state,
        "resource_state": resource,
        "epochs_observed": epochs_observed,
        "at_scout_budget": at_budget,
        "recent_trends": {
            "train_loss": loss_trend,
            "filtered_dice": metric_trend,
        },
        "latest_metrics": _latest_metric_summary(latest),
        "source_behavior": source_behavior,
        "prediction_degeneracy": degeneracy,
        "decision_support": {
            "recommendation": recommendation,
            "elimination_supported": elimination_supported,
            "strong_negative_evidence": strong_negative_evidence,
            "plateau_requires_human_review": plateau_review,
            "improving_trajectory": improving,
            "ambiguous_or_source_informative": ambiguous,
            "low_score_alone_supports_elimination": False,
        },
    }


def assess_scout_run(run_dir: str | Path) -> dict[str, object]:
    """Build an assessment from trusted Run artifacts without changing the Run."""

    root = Path(run_dir)
    records = [
        json.loads(line)
        for line in (root / "outputs" / "metrics.jsonl").read_text().splitlines()
        if line.strip()
    ]
    metadata_path = root / "run_metadata.json"
    metadata = json.loads(metadata_path.read_text()) if metadata_path.is_file() else {}
    resource_state = {
        "run_status": metadata.get("status"),
        "failure_classification": metadata.get("failure_classification"),
    }
    lifecycle = metadata.get("training_lifecycle")
    if isinstance(lifecycle, Mapping):
        resource_state.update(lifecycle)
    resource_profile_path = root / "outputs" / "resource_profile.json"
    if resource_profile_path.is_file():
        profile = json.loads(resource_profile_path.read_text())
        resource_state["resource_profile_status"] = profile.get("status")
        resource_state["batch_size"] = profile.get("batch_size")
        performance = profile.get("performance")
        if isinstance(performance, Mapping):
            resource_state.update(performance)
        hardware = profile.get("hardware")
        if isinstance(hardware, Mapping):
            resource_state.update(hardware)
    return build_scout_assessment(records, resource_state=resource_state)


def write_scout_assessment(run_dir: str | Path) -> Path:
    """Write the provider-owned assessment artifact for an existing Run."""

    root = Path(run_dir)
    output = root / "outputs" / "scout_assessment.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(assess_scout_run(root), indent=2, sort_keys=True, allow_nan=False) + "\n")
    return output


def _finite_state(records: Sequence[Mapping[str, object]]) -> dict[str, object]:
    non_finite_fields: list[str] = []
    numeric_value_count = 0
    for record_index, record in enumerate(records):
        for key, value in record.items():
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                continue
            numeric_value_count += 1
            if not math.isfinite(float(value)):
                non_finite_fields.append(f"records[{record_index}].{key}")
    return {
        "all_finite": not non_finite_fields,
        "numeric_value_count": numeric_value_count,
        "non_finite_fields": non_finite_fields[:20],
        "non_finite_field_count": len(non_finite_fields),
    }


def _resource_summary(state: Mapping[str, object]) -> dict[str, object]:
    run_status = state.get("run_status", state.get("status"))
    failure_classification = state.get("failure_classification")
    timeout_requested = bool(state.get("timeout_requested", state.get("run/timeout_requested", False)))
    resource_profile_status = state.get("resource_profile_status")
    hard_failure = (
        run_status in {"failed", "smoke_failed", "rejected"}
        or resource_profile_status == "failed"
        or failure_classification in {
            "candidate_bug",
            "contract_violation",
            "resource_failure",
            "harness_failure",
        }
    )
    return {
        "run_status": run_status,
        "failure_classification": failure_classification,
        "timeout_requested": timeout_requested,
        "hard_failure": hard_failure,
        "resource_profile_status": resource_profile_status,
        "batch_size": _finite_optional(state.get("batch_size")),
        "peak_cuda_memory_allocated_bytes": _finite_optional(state.get("cuda_peak_memory_allocated_bytes")),
        "peak_cuda_memory_reserved_bytes": _finite_optional(state.get("cuda_peak_memory_reserved_bytes")),
        "run_wall_seconds": _finite_optional(state.get("run_wall_seconds")),
        "training_wall_seconds": _finite_optional(state.get("training_wall_seconds")),
        "validation_wall_seconds": _finite_optional(state.get("validation_wall_seconds")),
    }


def _epoch_train_losses(records: Sequence[Mapping[str, object]]) -> list[tuple[int, float]]:
    grouped: dict[int, list[float]] = defaultdict(list)
    for record in records:
        if record.get("split") != "train" or _epoch(record) is None:
            continue
        value = record.get("loss")
        if isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value)):
            grouped[int(record["epoch"])].append(float(value))
    return [(epoch, sum(values) / len(values)) for epoch, values in sorted(grouped.items()) if values]


def _series(records: Sequence[Mapping[str, object]], key: str) -> list[tuple[int, float]]:
    result: list[tuple[int, float]] = []
    for record in records:
        value = record.get(key)
        if isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value)):
            result.append((int(record["epoch"]), float(value)))
    return result


def _trend_summary(values: Sequence[tuple[int, float]], *, lower_is_better: bool) -> dict[str, object]:
    recent = list(values[-RECENT_TREND_EPOCHS:])
    if len(recent) < 2:
        return {"points": len(recent), "slope_per_epoch": None, "direction": "insufficient_evidence"}
    epoch_delta = recent[-1][0] - recent[0][0]
    slope = (recent[-1][1] - recent[0][1]) / max(1, epoch_delta)
    if abs(slope) <= _TREND_TOLERANCE:
        direction = "ambiguous"
    elif (slope < 0) == lower_is_better:
        direction = "improving"
    else:
        direction = "worsening"
    return {
        "points": len(recent),
        "first_epoch": recent[0][0],
        "last_epoch": recent[-1][0],
        "first_value": recent[0][1],
        "last_value": recent[-1][1],
        "slope_per_epoch": slope,
        "direction": direction,
    }


def _source_summary(records: Sequence[Mapping[str, object]], source: str) -> dict[str, object]:
    key = f"val/source/{source}/filtered_dice"
    values = _series(records, key)
    latest = values[-1][1] if values else None
    raw_fraction = _latest_number(records, f"val/source/{source}/raw_predicted_positive_fraction")
    filtered_fraction = _latest_number(records, f"val/source/{source}/filtered_predicted_positive_fraction")
    return {
        "latest_filtered_dice": latest,
        "filtered_dice_trend": _trend_summary(values, lower_is_better=False),
        "latest_raw_predicted_positive_fraction": raw_fraction,
        "latest_filtered_predicted_positive_fraction": filtered_fraction,
    }


def _prediction_degeneracy(records: Sequence[Mapping[str, object]]) -> dict[str, object]:
    recent = list(records[-PERSISTENT_DEGENERACY_EPOCHS:])
    states = [_epoch_degeneracy(record) for record in recent]
    known = [state for state in states if state != "unknown"]
    persistent = len(known) == PERSISTENT_DEGENERACY_EPOCHS and len(set(known)) == 1 and known[0] != "non_degenerate"
    latest_state = states[-1] if states else "unknown"
    return {
        "latest_state": latest_state,
        "recent_states": states,
        "persistent": persistent,
        "raw_predicted_positive_fraction": _latest_number(records, "val/raw_predicted_positive_fraction"),
        "filtered_predicted_positive_fraction": _latest_number(records, "val/filtered_predicted_positive_fraction"),
    }


def _epoch_degeneracy(record: Mapping[str, object]) -> str:
    fractions = [
        _number(record.get("val/raw_predicted_positive_fraction")),
        _number(record.get("val/filtered_predicted_positive_fraction")),
    ]
    known = [value for value in fractions if value is not None]
    if not known:
        counts = [
            _number(record.get("val/raw_predicted_positive_pixel_count")),
            _number(record.get("val/filtered_predicted_positive_pixel_count")),
        ]
        known_counts = [value for value in counts if value is not None]
        return "collapsed_all_negative" if known_counts and all(value <= 0.0 for value in known_counts) else "unknown"
    if all(value <= _DEGENERATE_FRACTION for value in known):
        return "collapsed_all_negative"
    if all(value >= 1.0 - _DEGENERATE_FRACTION for value in known):
        return "saturated_all_positive"
    return "non_degenerate"


def _latest_metric_summary(record: Mapping[str, object]) -> dict[str, object]:
    keys = (
        "epoch",
        "val/loss",
        "val/raw_dice",
        "val/filtered_dice",
        "val/raw_predicted_positive_pixel_count",
        "val/raw_predicted_positive_fraction",
        "val/filtered_predicted_positive_pixel_count",
        "val/filtered_predicted_positive_fraction",
    )
    return {key: record[key] for key in keys if key in record}


def _latest_number(records: Sequence[Mapping[str, object]], key: str) -> float | None:
    for record in reversed(records):
        value = _number(record.get(key))
        if value is not None:
            return value
    return None


def _is_recent_plateau(values: Sequence[tuple[int, float]]) -> bool:
    recent = [value for _epoch_value, value in values[-RECENT_TREND_EPOCHS:]]
    if len(recent) < RECENT_TREND_EPOCHS:
        return False
    scale = max(1.0, max(abs(value) for value in recent))
    return max(recent) - min(recent) <= 1e-4 * scale


def _epoch(record: Mapping[str, object]) -> int | None:
    value = record.get("epoch")
    return int(value) if isinstance(value, int) and not isinstance(value, bool) and value >= 1 else None


def _number(value: object) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    converted = float(value)
    return converted if math.isfinite(converted) else None


def _finite_optional(value: object) -> float | None:
    return _number(value)


__all__ = [
    "DEFAULT_SCOUT_EPOCH_BUDGET",
    "SCHEMA_VERSION",
    "assess_scout_run",
    "build_scout_assessment",
    "write_scout_assessment",
]
