from __future__ import annotations

import inspect
from pathlib import Path

import pytest
import yaml

from abi_contrail.adapters import ABITrainingAdapter, build_spec
from abi_contrail.record_selection import select_representative_records
from ml_autoresearch.candidates import CandidateTrainingPolicy, CandidateValidationError, validate_candidate_directory
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
                    "bounded_record_selection": "candidate_prefix",
                    "record_selection_seed": 1,
                    "max_samples": 999999,
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

    with pytest.raises(
        CandidateValidationError,
        match="source_mixture|positive_patch_preference|bounded_record_selection|record_selection_seed|max_samples",
    ):
        validate_candidate_directory(candidate, research_problem_registry=registry)


def test_agent_may_choose_preregistered_allowlisted_candidate_parameters(tmp_path: Path) -> None:
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    (candidate / "manifest.yaml").write_text(
        yaml.safe_dump(
            {
                "name": "allowlisted_scout_choice",
                "research_problem": "goes_abi_contrail_segmentation",
                "input_mode": "abi_thermal_10ch",
                "output_form": "mask_logits",
                "data": {
                    "sampling_policy": "combined_source_balanced",
                    "augmentation_policy": "random_mirroring",
                },
                "training": {
                    "loss": "focal_tversky",
                    "optimizer": "adamw",
                    "learning_rate": 0.0003,
                    "batch_size": 4,
                    "max_epochs": 12,
                    "scheduler": {"policy": "constant_lr"},
                    "early_stopping": {"enabled": False},
                },
            },
            sort_keys=False,
        )
    )
    (candidate / "model.py").write_text("def build_model(input_spec, output_spec):\n    raise RuntimeError('not used')\n")
    registry = ResearchProblemSpecRegistry(active_id="goes_abi_contrail_segmentation")
    registry.register(build_spec())

    manifest = validate_candidate_directory(
        candidate,
        research_problem_registry=registry,
        training_policy=CandidateTrainingPolicy(
            max_epochs=12,
            max_batch_size=4,
            allowed_scheduler_policies=("constant_lr",),
            early_stopping_policy="disabled",
        ),
    )

    assert manifest.training.learning_rate == 0.0003
    assert manifest.training.loss == "focal_tversky"
    assert manifest.data.augmentation_policy == "random_mirroring"


def test_trusted_record_selector_exposes_no_candidate_policy_seed_or_record_callback() -> None:
    selector_parameters = set(inspect.signature(select_representative_records).parameters)
    adapter_parameters = set(inspect.signature(ABITrainingAdapter.build_datasets).parameters)

    assert selector_parameters == {"records", "max_samples", "dataset_source", "split"}
    assert adapter_parameters == {"self", "data_config", "resolved_manifest_path", "max_samples"}
    assert "seed" not in selector_parameters
    assert "policy" not in selector_parameters
    assert "candidate" not in adapter_parameters
    assert "record_selector" not in adapter_parameters


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
