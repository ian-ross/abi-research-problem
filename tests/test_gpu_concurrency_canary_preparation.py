import hashlib
import json
from pathlib import Path

import yaml

from ml_autoresearch.batches import validate_experiment_batch_directory
from ml_autoresearch.research_problems import ResearchProblemSpecRegistry

from abi_contrail.research_problem import build_spec
from scripts.prepare_abi029_concurrency_canary import prepare_concurrency_canary


SOURCE = Path("candidates/abi_spectral_resunet_scout_v1")


def test_prepare_concurrency_canary_writes_two_identical_valid_batch_candidates(tmp_path: Path) -> None:
    output = tmp_path / "canary"

    plan = prepare_concurrency_canary(SOURCE, output, batch_size=8, candidate_count=2)

    source_hash = hashlib.sha256((SOURCE / "model.py").read_bytes()).hexdigest()
    assert plan["batch_size"] == 8
    assert plan["candidate_count"] == plan["max_parallel_runs"] == 2
    assert plan["max_samples_per_source"] == 32
    assert json.loads((output / "CONCURRENCY_PLAN.json").read_text()) == plan
    proposal = (output / "BATCH_PROPOSAL.md").read_text()
    assert "Shared hypothesis" in proposal
    assert "Requested budget/concurrency" in proposal

    registry = ResearchProblemSpecRegistry(active_id="goes_abi_contrail_segmentation")
    registry.register(build_spec())
    validated = validate_experiment_batch_directory(output, research_problem_registry=registry)
    assert [item["candidate_id"] for item in validated] == [
        "abi_spectral_resunet_scout_v1_concurrency_a",
        "abi_spectral_resunet_scout_v1_concurrency_b",
    ]
    for item in validated:
        candidate = Path(item["source_path"])
        manifest = yaml.safe_load((candidate / "manifest.yaml").read_text())
        assert manifest["training"]["batch_size"] == 8
        assert manifest["training"]["max_epochs"] == 1
        assert hashlib.sha256((candidate / "model.py").read_bytes()).hexdigest() == source_hash
