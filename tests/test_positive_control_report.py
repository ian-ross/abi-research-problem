import json
import shutil
from pathlib import Path

import torch

from abi_contrail.positive_control import build_positive_control_report, candidate_tree_sha256


CANDIDATE = Path("candidates/abi031_mcast11_positive_control_v1")


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload) + "\n")


def _positive_control_fixture(tmp_path: Path) -> tuple[Path, Path, Path, str]:
    run_dir = tmp_path / "run_abi031"
    evaluation_dir = run_dir / "outputs" / "evaluations" / "eval_abi031"
    shutil.copytree(CANDIDATE, run_dir / "candidate")
    (run_dir / "resolved_manifest.yaml").write_text((CANDIDATE / "manifest.yaml").read_text())
    _write_json(run_dir / "run_metadata.json", {"run_id": "run_abi031", "status": "completed"})
    _write_json(run_dir / "execution.json", {"state": "completed"})
    _write_json(run_dir / "outputs" / "model_summary.json", {"parameter_count": 14_328_209})
    _write_json(run_dir / "outputs" / "resource_profile.json", {"status": "completed"})
    _write_json(run_dir / "outputs" / "final_metrics.json", {"train/loss": 0.2, "val/loss": 0.3})
    _write_json(run_dir / "outputs" / "best_metrics.json", {"selection_value": 0.01})
    (run_dir / "outputs" / "metrics.jsonl").write_text('{"train/loss":0.2,"val/loss":0.3}\n')
    checkpoint = run_dir / "outputs" / "models" / "best_epoch_model.pt"
    checkpoint.parent.mkdir(parents=True)
    torch.save({"model_state_dict": {"weight": torch.tensor([1.0])}}, checkpoint)

    metrics = {
        "raw/predicted_positive_pixel_count": 500_000.0,
        "filtered/predicted_positive_pixel_count": 450_000.0,
        "raw/dice": 0.01,
        "filtered/dice": 0.009,
        "source/mit/raw/dice": 0.011,
        "source/mit/filtered/dice": 0.01,
        "source/google/raw/dice": 0.009,
        "source/google/filtered/dice": 0.008,
    }
    _write_json(
        evaluation_dir / "aggregate_metrics.json",
        {"sample_count": 3_088, "metrics": metrics},
    )
    _write_json(
        evaluation_dir / "evaluation_metadata.json",
        {
            "evaluation_id": "eval_abi031",
            "source_run": {"run_id": "run_abi031"},
        },
    )
    _write_json(
        evaluation_dir / "acceptance_report.json",
        {"baseline_target_registry": {"id": "abi-mcast-working-validation-v1"}},
    )
    (evaluation_dir / "per_sample_metrics.jsonl").write_text("{}\n")
    _write_json(evaluation_dir / "threshold_sweep.json", {})
    _write_json(evaluation_dir / "diagnostic_samples" / "samples.json", {})

    ledger = tmp_path / "research-ledger.jsonl"
    ledger.write_text(
        '{"event_type":"run_completed","run_id":"run_abi031"}\n'
        '{"event_type":"evaluation_completed","run_id":"run_abi031","evaluation_id":"eval_abi031"}\n'
    )
    return run_dir, evaluation_dir, ledger, candidate_tree_sha256(run_dir / "candidate")


def test_positive_control_report_passes_complete_finite_non_degenerate_fixture(tmp_path: Path) -> None:
    run_dir, evaluation_dir, ledger, checksum = _positive_control_fixture(tmp_path)

    report = build_positive_control_report(
        run_dir=run_dir,
        evaluation_dir=evaluation_dir,
        ledger_path=ledger,
        expected_candidate_sha256=checksum,
    )

    assert report["hypothesis_passed"] is True
    assert report["decision"] == "positive_control_passed"
    assert all(criterion["passed"] for criterion in report["criteria"])
    assert report["beating_mcast_required"] is False


def test_positive_control_report_fails_all_negative_predictions(tmp_path: Path) -> None:
    run_dir, evaluation_dir, ledger, checksum = _positive_control_fixture(tmp_path)
    aggregate_path = evaluation_dir / "aggregate_metrics.json"
    aggregate = json.loads(aggregate_path.read_text())
    aggregate["metrics"]["raw/predicted_positive_pixel_count"] = 0.0
    aggregate["metrics"]["filtered/predicted_positive_pixel_count"] = 0.0
    _write_json(aggregate_path, aggregate)

    report = build_positive_control_report(
        run_dir=run_dir,
        evaluation_dir=evaluation_dir,
        ledger_path=ledger,
        expected_candidate_sha256=checksum,
    )

    criteria = {criterion["id"]: criterion for criterion in report["criteria"]}
    assert report["hypothesis_passed"] is False
    assert criteria["raw_prediction_non_degeneracy"]["passed"] is False
    assert criteria["filtered_prediction_non_degeneracy"]["passed"] is False
