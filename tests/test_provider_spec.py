from pathlib import Path

from ml_autoresearch.research_problems import (
    ResearchProblemProviderConfig,
    ResearchProblemSpecRegistry,
    load_research_problem_provider,
)

from abi_contrail.research_problem import build_spec


def test_build_spec_declares_abi_v0_contract() -> None:
    spec = build_spec()

    assert spec.id == "goes_abi_contrail_segmentation"
    assert spec.version == "v0"
    assert spec.contract_version == "v0"
    assert spec.input_modes == ("abi_16ch",)
    assert spec.input_specs["abi_16ch"]["shape"] == [16, 256, 256]
    assert spec.output_forms == ("mask_logits",)
    assert spec.output_specs["mask_logits"]["shape"] == [1, 256, 256]
    assert spec.losses == ("bce_dice",)
    assert spec.primary_metric == "val/dice"


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
