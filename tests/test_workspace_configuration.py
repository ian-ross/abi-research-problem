from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path
from urllib.parse import unquote


def test_committed_workspace_template_declares_abi_provider_data_and_runtime_requirements() -> None:
    template = Path("ml-autoresearch.toml.example")
    data = tomllib.loads(template.read_text())

    assert data["research_problem"]["id"] == "goes_abi_contrail_segmentation"
    assert data["research_problem"]["provider_target"] == "abi_contrail.research_problem:build_spec"
    data_roots = data["research_problem"]["data_roots"]
    assert set(data_roots) == {"training", "ancillary", "baselines"}
    assert data_roots["training"].endswith("contrail-detection")
    assert data_roots["ancillary"].endswith("ancillary")
    assert data_roots["baselines"].endswith("baselines")
    data_config = data["research_problem"]["data_config"]
    assert "dataset_root" not in data_config
    assert "data_root" not in data_config
    assert data_config["canonical_baseline_targets"] == "canonical/mcast-working-validation-v1.json"
    assert data_config["mcast_detection_1_1_path"] == "canonical/model-assets/detection-1.1.pt"
    assert data_config["mcast_detection_2_1_path"] == "canonical/model-assets/detection-2.1"
    assert data_config["geographic_filter_required"] is True
    assert data_config["geographic_ancillary_manifest"] == "natural-earth/manifest.json"
    assert data_config["coastline_geojson"].startswith("natural-earth/")
    assert data_config["rivers_geojson"].startswith("natural-earth/")
    sources = data_config["sources"]
    assert {source["layout"] for source in sources} == {"mit", "google"}
    assert all(source["metadata_parquet"].endswith("metadata.parquet") for source in sources)
    execution = data["candidate_execution"]
    assert execution["backend"] == "docker"
    assert execution["docker_enable_gpu"] is True
    assert execution["docker_gpu_device"] == "0"
    assert execution["docker_rootless_container_root"] is True
    assert execution["max_samples"] == 1024
    assert execution["max_parameters"] == 25_000_000
    assert execution["max_epochs"] == 12
    assert execution["max_batch_size"] == 4
    assert execution["allowed_scheduler_policies"] == ["constant_lr"]
    assert execution["early_stopping_policy"] == "disabled"
    assert execution["training_wall_clock_timeout_seconds"] == 3600
    assert execution["max_parallel_runs"] == 1
    assert execution["max_prediction_samples"] == 4
    assert execution["prediction_sample_policy"] == "first_n"
    requirements = data["runtime_images"]["runner_requirements"]
    assert any(requirement.startswith("zarr") for requirement in requirements)
    assert any(requirement.startswith("pandas") for requirement in requirements)
    assert any(requirement.startswith("pyarrow") for requirement in requirements)
    assert any(requirement.startswith("scipy") for requirement in requirements)
    assert "mailjet" not in data


def test_operator_invocation_is_sufficient_authority_under_trusted_bounds() -> None:
    instructions = Path("AGENTS.md").read_text()
    readme = Path("README.md").read_text()
    index = Path("EXPERIMENT_INDEX.md").read_text()
    brief = Path("abi_contrail/brief/goes-abi-contrail-segmentation.md").read_text()

    for document in (instructions, readme, index, brief):
        assert "autonomy-step" in document
        assert "run-autonomous-iteration" in document
        assert "sufficient authority" in document

    assert "Work should start from a backlog task" not in instructions
    assert "task-specific human gate" not in readme
    assert "campaign_paused" in instructions
    assert "longitude or latitude" in instructions
    assert "Candidate source" in index
    assert "generated Agent Workspace Configuration is authoritative" in brief

    scoped_guidance = "\n".join((instructions, readme, index, brief))
    assert "GVCCS" not in scoped_guidance
    assert "gvccs-research-problem" not in scoped_guidance
    assert not re.search(r"ABI-0(?:34|35|36|37|38|39|40|41|42|43|44)", scoped_guidance)


def test_campaign_reports_use_issue_independent_names_and_valid_ledger_paths() -> None:
    report_root = Path("campaign-reports")
    reports = sorted(report_root.glob("*.md"))

    assert reports
    assert all(not re.match(r"abi-\d{3}-", report.name, re.IGNORECASE) for report in reports)
    for report in reports:
        text = report.read_text()
        assert not re.search(r"\bABI[-_]\d{3}\b", text, re.IGNORECASE)
        assert "backlog/tasks/" not in text
        assert not re.search(r"separately? authoriz|human gate|human-gated", text, re.IGNORECASE)
        assert not re.search(r"(?:\A|\n\n)the ", text)
        assert not re.search(r"\bGate \d+\b", text)

    candidate_documents = [*Path("candidates").glob("*/README.md"), *Path("candidates").glob("*/PROPOSAL.md")]
    for document in candidate_documents:
        text = document.read_text()
        assert not re.search(r"\bABI-(?:025|031|032|034|035|036|037|038|039|040|041|042|043|044)\b", text)
        assert not re.search(r"separately? authoriz|human gate|human-gated", text, re.IGNORECASE)

    ledger_events = [json.loads(line) for line in Path("research-ledger.jsonl").read_text().splitlines()]
    for event in ledger_events:
        report_path = event.get("report_path")
        if report_path is not None:
            assert Path(report_path).is_file(), report_path
            assert not re.search(r"campaign-reports/abi-\d{3}-", report_path, re.IGNORECASE)
        reason = event.get("reason", "")
        assert not re.search(r"abi\d{3}|authoriz|onboarding", reason, re.IGNORECASE)

    for task in Path("backlog/tasks").glob("*.md"):
        assert not re.search(r"campaign-reports/abi-\d{3}-", task.read_text(), re.IGNORECASE), task


def test_candidate_run_provenance_remains_consistent() -> None:
    index = Path("EXPERIMENT_INDEX.md").read_text()
    ledger_events = [json.loads(line) for line in Path("research-ledger.jsonl").read_text().splitlines()]
    submitted = {
        event["candidate_id"]: event["run_id"]
        for event in ledger_events
        if event.get("event_type") == "candidate_submitted"
    }
    expected = {
        "abi032_mcast11_focal_tversky_v1": (
            "run_20260812_121722_8d6cd3",
            Path("campaign-reports/bounded-autonomous-candidate-run.md"),
        ),
        "abi037_mcast11_bce_dice_cldice_v1": (
            "run_20260812_151543_5b9508",
            Path("campaign-reports/bce-dice-cldice-autonomy-step.md"),
        ),
        "abi043_fullspectral_deeplabv3plus_resource_pilot_v1": (
            "run_20260813_131515_ff53ab",
            Path("campaign-reports/full-spectral-deeplabv3plus-resource-pilot.md"),
        ),
        "abi044_fullspectral_deeplabv3plus_representative_scout_v1": (
            "run_20260813_145951_a64a37",
            Path("campaign-reports/full-spectral-deeplabv3plus-representative-scout.md"),
        ),
    }
    for candidate_id, (run_id, report) in expected.items():
        assert submitted[candidate_id] == run_id
        assert candidate_id in index and run_id in index
        report_text = report.read_text()
        assert candidate_id in report_text and run_id in report_text


def test_agent_visible_markdown_links_resolve() -> None:
    documents = [Path("EXPERIMENT_INDEX.md"), *Path("campaign-reports").glob("*.md")]
    documents += [*Path("candidates").glob("*/README.md"), *Path("candidates").glob("*/PROPOSAL.md")]
    documents += list(Path("evaluation-requests").glob("*.md"))

    for document in documents:
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", document.read_text()):
            path_target = unquote(target.split("#", 1)[0])
            if not path_target or "://" in path_target or path_target.startswith("mailto:"):
                continue
            assert (document.parent / path_target).exists(), f"{document}: {target}"


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
