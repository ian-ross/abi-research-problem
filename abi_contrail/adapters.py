"""Trusted adapters and ResearchProblemSpec declaration for GOES ABI Contrail Segmentation.

ABI-001 intentionally exposes only the declarative provider spec. Dataset loading,
training adapters, artifact filters, and baseline segmenters are added by later
backlog tasks so candidate code cannot take ownership of trusted boundaries.
"""

from __future__ import annotations

from collections.abc import Mapping


RESEARCH_PROBLEM_ID = "goes_abi_contrail_segmentation"
RESEARCH_PROBLEM_VERSION = "v0"
CONTRACT_VERSION = "v0"
INPUT_MODE_ABI_16CH = "abi_16ch"
OUTPUT_FORM_MASK_LOGITS = "mask_logits"


def build_spec(data_config: Mapping[str, object] | None = None):
    """Build the GOES ABI Contrail Segmentation Research Problem Spec.

    Parameters
    ----------
    data_config:
        Accepted for the ml-autoresearch provider interface. The v0 scaffold is
        declarative and does not inspect data configuration yet.
    """

    del data_config

    from ml_autoresearch.research_problems import ResearchProblemSpec

    return ResearchProblemSpec(
        id=RESEARCH_PROBLEM_ID,
        version=RESEARCH_PROBLEM_VERSION,
        contract_version=CONTRACT_VERSION,
        input_modes=(INPUT_MODE_ABI_16CH,),
        input_specs={
            INPUT_MODE_ABI_16CH: {
                "mode": INPUT_MODE_ABI_16CH,
                "shape": [16, 256, 256],
                "layout": "channel_first",
                "channel_set": "goes_abi_channels_1_16",
                "forbidden_channels": ["longitude", "latitude"],
            },
        },
        output_forms=(OUTPUT_FORM_MASK_LOGITS,),
        output_specs={
            OUTPUT_FORM_MASK_LOGITS: {
                "form": OUTPUT_FORM_MASK_LOGITS,
                "shape": [1, 256, 256],
                "target": "contrail_mask",
            },
        },
        losses=("bce_dice",),
        optimizers=("adamw",),
        sampling_policies=("sequential", "deterministic_shuffle"),
        frame_selection_policies=("all_target_frames",),
        input_mode_frame_selection_defaults={INPUT_MODE_ABI_16CH: "all_target_frames"},
        augmentation_policies=("none",),
        primary_metric="val/dice",
        brief_documents=(
            {
                "name": "goes_abi_contrail_segmentation",
                "role": "problem_brief",
                "path": "abi_contrail/brief/goes-abi-contrail-segmentation.md",
                "summary": "Initial GOES ABI Contrail Segmentation task contract and provider registration notes.",
                "required": True,
            },
        ),
        dataset_profile_artifacts=(
            {
                "name": "goes_abi_initial_dataset_profile",
                "role": "initial_dataset_profile_placeholder",
                "path": "abi_contrail/profile/initial-dataset-profile.md",
                "summary": "Placeholder dataset profile for the ABI provider scaffold; filled by later data-profile tasks.",
                "split_scope": "not yet data-backed in ABI-001 scaffold",
                "required": False,
            },
        ),
    )
