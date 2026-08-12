import json
from pathlib import Path

from abi_contrail.scout_assessment import assess_scout_run, build_scout_assessment, write_scout_assessment


def _trajectory(
    filtered_dice: list[float],
    *,
    losses: list[float] | None = None,
    raw_fraction: float = 0.02,
    filtered_fraction: float = 0.015,
) -> list[dict[str, object]]:
    losses = losses or [1.0 - 0.02 * index for index in range(len(filtered_dice))]
    records: list[dict[str, object]] = []
    for epoch, (metric, loss) in enumerate(zip(filtered_dice, losses, strict=True), start=1):
        records.append({"split": "train", "epoch": epoch, "batch": 0, "loss": loss})
        records.append(
            {
                "split": "val",
                "epoch": epoch,
                "val/filtered_dice": metric,
                "val/raw_dice": metric * 0.9,
                "val/raw_predicted_positive_pixel_count": raw_fraction * 1000,
                "val/raw_predicted_positive_fraction": raw_fraction,
                "val/filtered_predicted_positive_pixel_count": filtered_fraction * 1000,
                "val/filtered_predicted_positive_fraction": filtered_fraction,
                "val/source/mit/filtered_dice": metric * 1.1,
                "val/source/google/filtered_dice": metric * 0.9,
                "val/source/mit/raw_predicted_positive_fraction": raw_fraction,
                "val/source/mit/filtered_predicted_positive_fraction": filtered_fraction,
                "val/source/google/raw_predicted_positive_fraction": raw_fraction,
                "val/source/google/filtered_predicted_positive_fraction": filtered_fraction,
            }
        )
    return records


def test_low_scoring_slow_starter_remains_extension_eligible() -> None:
    assessment = build_scout_assessment(_trajectory([0.001, 0.002, 0.004, 0.008]))

    assert assessment["recent_trends"]["filtered_dice"]["direction"] == "improving"
    assert assessment["source_behavior"]["mit"]["latest_filtered_dice"] > 0
    assert assessment["source_behavior"]["google"]["latest_filtered_dice"] > 0
    assert assessment["decision_support"]["recommendation"] == "extension_eligible"
    assert assessment["decision_support"]["elimination_supported"] is False
    assert assessment["decision_support"]["low_score_alone_supports_elimination"] is False
    assert assessment["policy"]["strict_top_k"] is False
    assert assessment["policy"]["absolute_dice_elimination_threshold"] is None


def test_noisy_ambiguous_trajectory_remains_extension_eligible_at_budget() -> None:
    values = [0.04, 0.05, 0.045, 0.052, 0.047, 0.053, 0.049, 0.054, 0.051, 0.055, 0.052, 0.056]
    assessment = build_scout_assessment(_trajectory(values), scout_epoch_budget=12)

    assert assessment["at_scout_budget"] is True
    assert assessment["finite_state"]["all_finite"] is True
    assert assessment["prediction_degeneracy"]["latest_state"] == "non_degenerate"
    assert assessment["decision_support"]["recommendation"] == "extension_eligible"
    assert assessment["decision_support"]["ambiguous_or_source_informative"] is True


def test_persistent_prediction_collapse_supports_elimination() -> None:
    records = _trajectory(
        [0.03, 0.01, 0.0],
        losses=[0.8, 0.8, 0.8],
        raw_fraction=0.0,
        filtered_fraction=0.0,
    )
    assessment = build_scout_assessment(records)

    assert assessment["prediction_degeneracy"]["persistent"] is True
    assert assessment["prediction_degeneracy"]["latest_state"] == "collapsed_all_negative"
    assert assessment["decision_support"]["recommendation"] == "elimination_supported"
    assert "persistent_prediction_collapse" in assessment["decision_support"]["strong_negative_evidence"]


def test_non_finite_curve_supports_elimination() -> None:
    records = _trajectory([0.02])
    records[0]["loss"] = float("nan")

    assessment = build_scout_assessment(records)

    assert assessment["finite_state"]["all_finite"] is False
    assert assessment["finite_state"]["non_finite_field_count"] == 1
    assert "non_finite_evidence" in assessment["decision_support"]["strong_negative_evidence"]


def test_hard_resource_failure_supports_elimination_without_metric_cutoff() -> None:
    assessment = build_scout_assessment(
        _trajectory([0.02]),
        resource_state={"run_status": "failed", "failure_classification": "resource_failure"},
    )

    assert assessment["resource_state"]["hard_failure"] is True
    assert assessment["decision_support"]["elimination_supported"] is True
    assert "hard_failure" in assessment["decision_support"]["strong_negative_evidence"]


def test_run_assessment_reads_and_optionally_writes_trusted_artifact(tmp_path: Path) -> None:
    run_dir = tmp_path / "run_1"
    outputs = run_dir / "outputs"
    outputs.mkdir(parents=True)
    records = _trajectory([0.01, 0.02])
    (outputs / "metrics.jsonl").write_text("".join(json.dumps(record) + "\n" for record in records))
    (run_dir / "run_metadata.json").write_text(json.dumps({"status": "completed"}))
    (outputs / "resource_profile.json").write_text(
        json.dumps(
            {
                "status": "completed",
                "batch_size": 4,
                "hardware": {"cuda_peak_memory_reserved_bytes": 2048},
                "performance": {"training_wall_seconds": 12.5, "validation_wall_seconds": 3.0},
            }
        )
    )

    assessment = assess_scout_run(run_dir)
    output = write_scout_assessment(run_dir)

    assert assessment["resource_state"]["run_status"] == "completed"
    assert assessment["resource_state"]["training_wall_seconds"] == 12.5
    assert assessment["resource_state"]["validation_wall_seconds"] == 3.0
    assert assessment["resource_state"]["batch_size"] == 4.0
    assert assessment["resource_state"]["peak_cuda_memory_reserved_bytes"] == 2048.0
    assert output == outputs / "scout_assessment.json"
    assert json.loads(output.read_text()) == assessment
