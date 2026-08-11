from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_operator_guidance_documents_managed_run_recovery_and_nonfinite_semantics() -> None:
    readme = (ROOT / "README.md").read_text()
    report = (ROOT / "campaign-reports" / "abi-030-run-reliability.md").read_text()

    for required in ["--detach", "run-status", "reconcile-run", "execution.json"]:
        assert required in readme
    assert "Caller disconnection is not authorization to rerun" in readme
    assert "Neither is a Resource Failure" in readme
    assert "nonfinite_diagnostic.json" in readme
    assert "does not authorize" in report
    assert "No ABI scientific Candidate or real training data" in report
