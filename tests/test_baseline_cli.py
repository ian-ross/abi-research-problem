from __future__ import annotations

import json
from pathlib import Path

from abi_contrail.baseline_cli import _close_progress_logger, _progress_logger, run_configured_baseline_evaluations
from abi_contrail.baseline_segmenters import MCAST_BASELINE_1_1


class FakeEvaluationAdapter:
    def run_baseline_validation_evaluation(self, **kwargs):
        kwargs["progress_callback"]("fake evaluator progress")
        assert kwargs["log_every"] == 7
        assert kwargs["postprocessing_batch_size"] == 3
        evaluation_dir = kwargs["evaluation_dir"]
        evaluation_dir.mkdir(parents=True, exist_ok=True)
        (evaluation_dir / "aggregate_metrics.json").write_text('{"metrics":{"filtered/dice":0.5}}\n')
        (evaluation_dir / "per_sample_metrics.jsonl").write_text('{"sample_id":"val/000000"}\n')
        return (
            {"filtered/dice": 0.5},
            [{"sample_id": "val/000000"}],
            {},
            {"postprocessing": {"backend": "torch_cpu", "batch_size": 3}},
        )


def test_progress_logger_writes_timestamped_log_file(tmp_path: Path) -> None:
    path = tmp_path / "baseline_evaluation.log"
    logger = _progress_logger(path)
    try:
        logger.info("visible progress")
    finally:
        _close_progress_logger(logger)

    text = path.read_text()
    assert "INFO visible progress" in text
    assert text.endswith("\n")


def test_configured_baseline_evaluation_records_workspace_data_and_asset_provenance(tmp_path: Path) -> None:
    asset = tmp_path / "detection-1.1.pt"
    asset.write_bytes(b"checkpoint")
    data_root = tmp_path / "data"
    data_root.mkdir()
    (tmp_path / "ml-autoresearch.toml").write_text(
        f'''[research_problem]
id = "goes_abi_contrail_segmentation"
package_root = "."
provider_target = "abi_contrail.research_problem:build_spec"
expected_contract_version = "v0"

[research_problem.data_config]
dataset_root = "{data_root}"
mcast_detection_1_1_path = "{asset}"
'''
    )

    progress_messages: list[str] = []
    results = run_configured_baseline_evaluations(
        workspace_root=tmp_path,
        baseline_names=(MCAST_BASELINE_1_1,),
        output_root=tmp_path / "outputs",
        device="cpu",
        evaluator=FakeEvaluationAdapter(),
        progress=progress_messages.append,
        log_every=7,
        postprocessing_batch_size=3,
    )

    assert len(results) == 1
    assert any("starting baseline" in message for message in progress_messages)
    assert "fake evaluator progress" in progress_messages
    assert any("completed baseline" in message for message in progress_messages)
    manifest = json.loads((tmp_path / "outputs" / MCAST_BASELINE_1_1 / "run_manifest.json").read_text())
    assert manifest["status"] == "completed"
    assert manifest["research_problem"]["id"] == "goes_abi_contrail_segmentation"
    assert manifest["data_config"]["dataset_root"] == str(data_root)
    assert manifest["baseline"]["asset"]["path"] == str(asset.resolve())
    assert manifest["baseline"]["asset"]["sha256"]
    assert manifest["sample_count"] == 1
    assert manifest["artifacts"]["aggregate_metrics"] == "aggregate_metrics.json"
    assert manifest["postprocessing"] == {"backend": "torch_cpu", "batch_size": 3}
    assert manifest["artifact_filters"]["pipeline_order"] == [
        "geographic_feature_filter",
        "scanline_artifact_filter",
    ]
    assert manifest["artifact_filters"]["geographic_feature_filter"] == {
        "active": False,
        "bundle_id": None,
        "manifest_path": None,
        "reason": "not_configured",
        "required": False,
        "sources": [],
    }
    assert manifest["artifact_filters"]["scanline_artifact_filter"] == {
        "active": True,
        "min_length_pixels": 128,
        "max_probability_std": 0.03,
    }
