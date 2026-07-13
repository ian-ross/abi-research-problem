from __future__ import annotations

import pytest

from abi_contrail.evaluation import AcceptanceGateConfig, build_acceptance_gate_report


def _baseline_a() -> dict[str, float | str]:
    return {
        "baseline/name": "mcast_detection_1_1",
        "filtered/dice": 0.70,
        "filtered/iou": 0.54,
        "filtered/recall": 0.75,
        "filtered/contrail_connectivity": 0.62,
        "source/mit/filtered/dice": 0.68,
        "source/google/filtered/dice": 0.72,
    }


def _passing_candidate() -> dict[str, float]:
    return {
        "raw/dice": 0.70,
        "raw/predicted_positive_pixel_count": 1000.0,
        "filtered/dice": 0.76,
        "filtered/iou": 0.61,
        "filtered/recall": 0.74,
        "filtered/contrail_connectivity": 0.66,
        "source/mit/filtered/dice": 0.70,
        "source/google/filtered/dice": 0.77,
        "artifact_filters/removed_pixel_count": 100.0,
    }


def test_acceptance_gate_report_compares_candidate_to_best_baseline() -> None:
    worse_baseline = {**_baseline_a(), "baseline/name": "mcast_detection_2_1", "filtered/dice": 0.65}

    report = build_acceptance_gate_report(
        candidate_metrics=_passing_candidate(),
        baseline_metrics=[_baseline_a(), worse_baseline],
        candidate_run_id="candidate-001",
    )

    assert report["candidate_run_id"] == "candidate-001"
    assert report["promotion_decision"] == "human_review_required"
    assert report["human_review_required"] is True
    assert report["best_baseline"]["name"] == "mcast_detection_1_1"
    assert report["aggregate_comparison"]["metric"] == "filtered/dice"
    assert report["aggregate_comparison"]["candidate"] == pytest.approx(0.76)
    assert report["aggregate_comparison"]["baseline"] == pytest.approx(0.70)
    assert report["aggregate_comparison"]["delta"] == pytest.approx(0.06)
    assert report["recall_regression"]["flagged"] is False
    assert report["contrail_connectivity_comparison"]["delta"] == pytest.approx(0.04)
    assert report["dataset_source_failures"] == []
    assert report["artifact_filter_dependence"]["flagged"] is False


def test_acceptance_gate_report_can_select_best_baseline_by_filtered_iou() -> None:
    best_iou = {**_baseline_a(), "baseline/name": "mcast_detection_2_1", "filtered/dice": 0.69, "filtered/iou": 0.60}

    report = build_acceptance_gate_report(
        candidate_metrics=_passing_candidate(),
        baseline_metrics=[_baseline_a(), best_iou],
        config=AcceptanceGateConfig(primary_metric="filtered/iou"),
    )

    assert report["best_baseline"]["name"] == "mcast_detection_2_1"
    assert report["aggregate_comparison"]["metric"] == "filtered/iou"
    assert report["aggregate_comparison"]["baseline"] == pytest.approx(0.60)


def test_acceptance_gate_report_flags_filtered_recall_regression_beyond_tolerance() -> None:
    candidate = {**_passing_candidate(), "filtered/recall": 0.65}

    report = build_acceptance_gate_report(
        candidate_metrics=candidate,
        baseline_metrics=[_baseline_a()],
        config=AcceptanceGateConfig(filtered_recall_tolerance=0.05),
    )

    assert report["recall_regression"]["flagged"] is True
    assert report["recall_regression"]["tolerance"] == pytest.approx(0.05)
    assert any(flag["id"] == "filtered_recall_regression" for flag in report["flags"])


def test_acceptance_gate_report_flags_dataset_source_catastrophic_failure() -> None:
    candidate = {**_passing_candidate(), "source/google/filtered/dice": 0.20}

    report = build_acceptance_gate_report(
        candidate_metrics=candidate,
        baseline_metrics=[_baseline_a()],
        config=AcceptanceGateConfig(source_failure_relative_drop=0.50, source_failure_absolute_floor=0.10),
    )

    assert report["dataset_source_failures"] == [
        {
            "source": "google",
            "metric": "source/google/filtered/dice",
            "candidate": pytest.approx(0.20),
            "baseline": pytest.approx(0.72),
            "relative_floor": pytest.approx(0.36),
            "absolute_floor": pytest.approx(0.10),
            "severity": "fail",
        }
    ]
    assert any(flag["id"] == "dataset_source_catastrophic_failure" for flag in report["flags"])


def test_acceptance_gate_report_flags_excessive_artifact_filter_dependence() -> None:
    candidate = {
        **_passing_candidate(),
        "raw/dice": 0.40,
        "filtered/dice": 0.76,
        "raw/predicted_positive_pixel_count": 1000.0,
        "artifact_filters/removed_pixel_count": 700.0,
    }

    report = build_acceptance_gate_report(
        candidate_metrics=candidate,
        baseline_metrics=[_baseline_a()],
        config=AcceptanceGateConfig(artifact_filter_removed_fraction_limit=0.50, artifact_filter_improvement_limit=0.20),
    )

    assert report["artifact_filter_dependence"]["flagged"] is True
    assert report["artifact_filter_dependence"]["removed_fraction"] == pytest.approx(0.70)
    assert report["artifact_filter_dependence"]["filtered_minus_raw_primary"] == pytest.approx(0.36)
    assert any(flag["id"] == "excessive_artifact_filter_dependence" for flag in report["flags"])
