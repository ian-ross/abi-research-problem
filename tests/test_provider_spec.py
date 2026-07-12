from pathlib import Path

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
    assert spec.losses == ("bce_dice", "focal_tversky", "bce_dice_cldice")
    assert spec.primary_metric == "val/filtered_dice"
    assert spec.operation_capabilities.training is True
    assert spec.operation_capabilities.evaluation_modes == ("whole_validation_failure_analysis",)
    assert spec.evaluation_adapter is not None


def test_split_data_policy_metadata_records_leakage_safe_index_policy() -> None:
    metadata = split_data_policy_metadata()

    assert metadata["google_split_policy"] == "respect_google_scene_name_train_validation_provenance"
    assert metadata["mit_split_policy"] == "deterministic_whole_scene_train_validation_split_before_windowing"
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
