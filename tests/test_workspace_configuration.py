from __future__ import annotations

import tomllib
from pathlib import Path


def test_committed_workspace_template_declares_abi_provider_data_and_runtime_requirements() -> None:
    template = Path("ml-autoresearch.toml.example")
    data = tomllib.loads(template.read_text())

    assert data["research_problem"]["id"] == "goes_abi_contrail_segmentation"
    assert data["research_problem"]["provider_target"] == "abi_contrail.research_problem:build_spec"
    data_config = data["research_problem"]["data_config"]
    assert data_config["geographic_filter_required"] is True
    assert data_config["geographic_ancillary_manifest"] == "ancillary/natural-earth/manifest.json"
    sources = data_config["sources"]
    assert {source["layout"] for source in sources} == {"mit", "google"}
    assert all(source["metadata_parquet"].endswith("metadata.parquet") for source in sources)
    requirements = data["runtime_images"]["runner_requirements"]
    assert any(requirement.startswith("zarr") for requirement in requirements)
    assert any(requirement.startswith("pandas") for requirement in requirements)
    assert any(requirement.startswith("pyarrow") for requirement in requirements)
    assert "mailjet" not in data


def test_workspace_bootstrap_files_exist() -> None:
    assert Path("EXPERIMENT_INDEX.md").is_file()
    assert Path("research-ledger.jsonl").is_file()
    for directory in (
        "candidates",
        "experiment-batches",
        "research-notes",
        "capability-requests",
        "evaluation-requests",
        "campaign-reports",
    ):
        assert Path(directory).is_dir()
