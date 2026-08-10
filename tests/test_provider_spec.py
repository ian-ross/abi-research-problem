from pathlib import Path

import pytest

from ml_autoresearch.errors import ResearchProblemDataError
from ml_autoresearch.research_problems import (
    ResearchProblemProviderConfig,
    ResearchProblemSpecRegistry,
    load_research_problem_provider,
)

from abi_contrail.adapters import split_data_policy_metadata
from abi_contrail.research_problem import build_spec


def test_build_spec_declares_abi_v0_contract() -> None:
    spec = build_spec()

    assert spec.id == "goes_abi_contrail_segmentation"
    assert spec.version == "v0"
    assert spec.contract_version == "v0"
    assert spec.input_modes == ("abi_16ch", "abi_16ch_plus_sza", "abi_thermal_10ch")
    assert spec.input_specs["abi_16ch"]["shape"] == [16, 256, 256]
    assert spec.input_specs["abi_16ch"]["source_channel_indices"] == list(range(16))
    assert spec.input_specs["abi_16ch_plus_sza"]["shape"] == [17, 256, 256]
    assert spec.input_specs["abi_16ch_plus_sza"]["source_channel_indices"] == list(range(16)) + [18]
    assert spec.input_specs["abi_thermal_10ch"]["shape"] == [10, 256, 256]
    assert spec.input_specs["abi_thermal_10ch"]["source_channel_indices"] == list(range(6, 16))
    assert all(16 not in spec.input_specs[mode]["source_channel_indices"] for mode in spec.input_modes)
    assert all(17 not in spec.input_specs[mode]["source_channel_indices"] for mode in spec.input_modes)
    assert spec.output_forms == ("mask_logits",)
    assert spec.output_specs["mask_logits"]["shape"] == [1, 256, 256]
    assert spec.auxiliary_targets == ("line", "boundary", "centerline")
    assert spec.auxiliary_outputs == {
        "line": "line_logits",
        "boundary": "boundary_logits",
        "centerline": "centerline_logits",
    }
    assert spec.auxiliary_output_shapes == {
        "line": [1, 256, 256],
        "boundary": [1, 256, 256],
        "centerline": [1, 256, 256],
    }
    assert spec.losses == ("bce_dice", "focal_tversky", "bce_dice_cldice")
    assert spec.sampling_policies == (
        "sequential",
        "deterministic_shuffle",
        "mit_only",
        "google_only",
        "combined_source_balanced",
    )
    assert spec.augmentation_policies == ("none", "random_mirroring")
    assert spec.auxiliary_losses == ("weighted_bce",)
    assert spec.primary_metric == "val/filtered_dice"
    assert spec.operation_capabilities.training is True
    assert spec.operation_capabilities.evaluation_modes == ("whole_validation_failure_analysis",)
    assert spec.evaluation_adapter is not None
    for document in spec.brief_documents:
        assert Path(str(document.path)).is_file()
    assert {artifact.name for artifact in spec.dataset_profile_artifacts} == {
        "goes_abi_initial_dataset_profile",
        "goes_abi_agent_campaign_context_v1",
    }
    for artifact in spec.dataset_profile_artifacts:
        assert Path(str(artifact.path)).is_file()
        assert artifact.role == "operator_generated_dataset_profile_or_generator"


def test_build_spec_allows_static_contract_loading_without_unmounted_data_roots() -> None:
    data_config = {
        "geographic_filter_required": True,
        "geographic_ancillary_manifest": "natural-earth/manifest.json",
        "postprocessing_batch_size": 8,
        "sources": [
            {"layout": "mit", "patch_size": 256},
            {"layout": "google", "patch_size": 256},
        ],
    }

    spec = build_spec(data_config=data_config)

    assert spec.id == "goes_abi_contrail_segmentation"
    geographic_filter = spec.training_adapter.filter_pipeline.provenance()["geographic_feature_filter"]
    assert geographic_filter["active"] is False
    assert geographic_filter["required"] is False
    assert geographic_filter["reason"] == "not_configured"
    assert geographic_filter["sources"] == []
    with pytest.raises(ResearchProblemDataError, match="requires data_roots or legacy dataset_root/data_root"):
        spec.training_adapter.validate_data_root(data_config)


def test_named_roots_do_not_change_candidate_longitude_latitude_boundary(tmp_path: Path) -> None:
    training = tmp_path / "training"
    ancillary = tmp_path / "ancillary"
    training.mkdir()
    ancillary.mkdir()

    spec = build_spec(
        data_config={
            "data_roots": {
                "training": str(training),
                "ancillary": str(ancillary),
            }
        }
    )

    for mode in spec.input_modes:
        input_spec = spec.input_specs[mode]
        assert input_spec["forbidden_channels"] == ["longitude", "latitude"]
        assert 16 not in input_spec["source_channel_indices"]
        assert 17 not in input_spec["source_channel_indices"]


def test_output_spec_includes_manifest_declared_auxiliary_outputs() -> None:
    spec = build_spec()

    output_spec = spec.build_output_spec(
        {
            "output_form": "mask_logits",
            "auxiliary_targets": [
                {"name": "line", "output": "line_logits", "loss": "weighted_bce", "weight": 0.1},
                {"name": "boundary", "output": "boundary_logits", "loss": "weighted_bce", "weight": 0.1},
                {"name": "centerline", "output": "centerline_logits", "loss": "weighted_bce", "weight": 0.1},
            ],
        }
    )

    assert output_spec["auxiliary_outputs"] == [
        {"target": "line", "name": "line_logits", "shape": [1, 256, 256]},
        {"target": "boundary", "name": "boundary_logits", "shape": [1, 256, 256]},
        {"target": "centerline", "name": "centerline_logits", "shape": [1, 256, 256]},
    ]


def test_split_data_policy_metadata_records_leakage_safe_index_policy() -> None:
    metadata = split_data_policy_metadata()

    assert metadata["google_split_policy"] == "respect_google_scene_name_train_validation_provenance"
    assert metadata["mit_split_policy"] == "deterministic_whole_scene_train_validation_split_before_windowing"
    assert metadata["sampling_policy_owner"] == "provider/harness"
    assert "combined_source_balanced" in metadata["sampling_policies"]
    assert "positive" in metadata["records_include"]


def test_provider_is_loadable_by_ml_autoresearch() -> None:
    config = ResearchProblemProviderConfig(
        id="goes_abi_contrail_segmentation",
        expected_contract_version="v0",
        package_root=Path("."),
        provider_target="abi_contrail.research_problem:build_spec",
    )
    registry = ResearchProblemSpecRegistry(active_id=config.id)

    loaded = load_research_problem_provider(config, registry=registry)

    assert loaded.spec.id == "goes_abi_contrail_segmentation"
    assert loaded.provenance.provider_target == "abi_contrail.research_problem:build_spec"
