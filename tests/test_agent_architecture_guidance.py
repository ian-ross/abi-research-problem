from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_agent_visible_docs_name_underexplored_architecture_directions() -> None:
    agents = (ROOT / "AGENTS.md").read_text()
    brief = (ROOT / "abi_contrail" / "brief" / "goes-abi-contrail-segmentation.md").read_text()
    index = (ROOT / "EXPERIMENT_INDEX.md").read_text()

    for document in (agents, brief, index):
        lower_document = document.lower()
        assert "underexplored" in lower_document or "broadening guidance" in lower_document
        assert "abi-202" in lower_document
        assert "temporal" in lower_document
        assert "rotation-aware" in lower_document or "group-equivariant" in lower_document
        assert "hough/radon" in lower_document
        assert "modern" in lower_document and "backbone" in lower_document
        assert "mixture-of-experts" in lower_document
        assert "calibration" in lower_document


def test_agent_guidance_documents_temporal_manifest_and_guardrails() -> None:
    agents = (ROOT / "AGENTS.md").read_text()
    brief = (ROOT / "abi_contrail" / "brief" / "goes-abi-contrail-segmentation.md").read_text()

    for document in (agents, brief):
        assert "input_mode: abi_16ch_plus_sza_temporal" in document
        assert "frame_selection_policy: temporal_eligible_center" in document
        assert "temporal_frame_offsets: [-1, 0, 1]" in document
        assert "[-2, -1, 0, 1, 2]" in document
        assert "abi_16ch_plus_sza" in document
        assert "Matched single-frame controls" in document or "matched single-frame control" in document
        assert "Candidate code must not" in document
        assert "S3" in document
        assert "longitude" in document and "latitude" in document
        assert "run sequentially" in document
