from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from abi_contrail.adapters import build_spec
from ml_autoresearch.candidates import CandidateValidationError, validate_candidate_directory
from ml_autoresearch.research_problems import ResearchProblemSpecRegistry


def test_candidate_manifest_cannot_define_or_override_sampling_policy_parameters(tmp_path: Path) -> None:
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    (candidate / "manifest.yaml").write_text(
        yaml.safe_dump(
            {
                "name": "attempted_sampling_override",
                "research_problem": "goes_abi_contrail_segmentation",
                "input_mode": "abi_16ch",
                "output_form": "mask_logits",
                "data": {
                    "sampling_policy": "combined_source_balanced",
                    "augmentation_policy": "none",
                    "source_mixture": {"mit": 0.9, "google": 0.1},
                    "positive_patch_preference": 99,
                },
                "training": {
                    "loss": "bce_dice",
                    "optimizer": "adamw",
                    "learning_rate": 0.001,
                    "batch_size": 1,
                    "max_epochs": 1,
                },
            },
            sort_keys=False,
        )
    )
    (candidate / "model.py").write_text("def build_model(input_spec, output_spec):\n    raise RuntimeError('not used')\n")
    registry = ResearchProblemSpecRegistry(active_id="goes_abi_contrail_segmentation")
    registry.register(build_spec())

    with pytest.raises(CandidateValidationError, match="source_mixture|positive_patch_preference"):
        validate_candidate_directory(candidate, research_problem_registry=registry)


def test_candidate_manifest_cannot_define_or_override_artifact_filters(tmp_path: Path) -> None:
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    (candidate / "manifest.yaml").write_text(
        yaml.safe_dump(
            {
                "name": "attempted_filter_override",
                "research_problem": "goes_abi_contrail_segmentation",
                "input_mode": "abi_16ch",
                "output_form": "mask_logits",
                "data": {"sampling_policy": "sequential", "augmentation_policy": "none"},
                "training": {
                    "loss": "bce_dice",
                    "optimizer": "adamw",
                    "learning_rate": 0.001,
                    "batch_size": 1,
                    "max_epochs": 1,
                },
                "artifact_filters": {"scanline_min_length_pixels": 1},
            },
            sort_keys=False,
        )
    )
    (candidate / "model.py").write_text("def build_model(input_spec, output_spec):\n    raise RuntimeError('not used')\n")
    registry = ResearchProblemSpecRegistry(active_id="goes_abi_contrail_segmentation")
    registry.register(build_spec())

    with pytest.raises(CandidateValidationError, match="artifact_filters"):
        validate_candidate_directory(candidate, research_problem_registry=registry)
