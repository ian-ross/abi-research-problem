import hashlib
import json
from pathlib import Path

import yaml

from ml_autoresearch.candidates import validate_candidate_directory
from ml_autoresearch.research_problems import ResearchProblemSpecRegistry

from abi_contrail.research_problem import build_spec
from scripts.prepare_abi029_gpu_profiles import prepare_profiles


SOURCE = Path("candidates/abi_spectral_resunet_scout_v1")


def test_prepare_profiles_copies_model_and_writes_bounded_valid_candidates(tmp_path: Path) -> None:
    output = tmp_path / "profiles"

    plan = prepare_profiles(SOURCE, output, (1, 4))

    source_hash = hashlib.sha256((SOURCE / "model.py").read_bytes()).hexdigest()
    assert plan["batch_sizes"] == [1, 4]
    assert plan["max_samples_per_source"] == 32
    assert plan["max_epochs"] == 1
    assert plan["source_model_sha256"] == source_hash
    assert json.loads((output / "PROFILE_PLAN.json").read_text()) == plan

    registry = ResearchProblemSpecRegistry(active_id="goes_abi_contrail_segmentation")
    registry.register(build_spec())
    for batch_size in (1, 4):
        candidate_id = f"abi_spectral_resunet_scout_v1_profile_bs{batch_size}"
        candidate = output / candidate_id
        assert hashlib.sha256((candidate / "model.py").read_bytes()).hexdigest() == source_hash
        manifest = yaml.safe_load((candidate / "manifest.yaml").read_text())
        assert manifest["name"] == candidate_id
        assert manifest["training"]["batch_size"] == batch_size
        assert manifest["training"]["max_epochs"] == 1
        assert "32 training and validation samples per Dataset Source" in (candidate / "PROPOSAL.md").read_text()
        validated = validate_candidate_directory(
            candidate,
            require_proposal=True,
            require_readme=True,
            research_problem_registry=registry,
        )
        assert validated.name == candidate_id
