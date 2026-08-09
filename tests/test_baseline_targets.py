from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from abi_contrail.baseline_segmenters import MCAST_BASELINE_1_1, MCAST_BASELINE_2_1
from abi_contrail.artifact_filters import ABIArtifactFilterPipeline
from abi_contrail.baseline_targets import (
    canonical_baseline_metrics,
    generate_canonical_baseline_targets,
    load_canonical_baseline_targets,
    resolve_canonical_baseline_targets_path,
)
from abi_contrail.evaluation import ABIEvaluationAdapter


def _metrics(offset: float) -> dict[str, float]:
    metrics = {
        f"{namespace}/{name}": value + offset
        for namespace, namespace_offset in (("raw", 0.0), ("filtered", -0.01))
        for name, value in (
            ("dice", 0.40 + namespace_offset),
            ("iou", 0.25 + namespace_offset),
            ("precision", 0.45 + namespace_offset),
            ("recall", 0.36 + namespace_offset),
            ("contrail_connectivity", 0.54 + namespace_offset),
        )
    }
    metrics["artifact_filters/removed_pixel_count"] = 3.0
    return metrics


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _fixture_asset(root: Path, baseline_name: str) -> dict[str, object]:
    assets_root = root.parent / "source-model-assets"
    assets_root.mkdir(exist_ok=True)
    if baseline_name == MCAST_BASELINE_1_1:
        path = assets_root / "detection-1.1.pt"
        path.write_bytes(b"mcast-1.1-checkpoint")
        return {
            "path": str(path),
            "kind": "file",
            "size_bytes": path.stat().st_size,
            "sha256": _file_sha256(path),
        }
    path = assets_root / "detection-2.1"
    path.mkdir(exist_ok=True)
    (path / "checkpoint.pt").write_bytes(b"mcast-2.1-checkpoint")
    relative = "checkpoint.pt"
    file_sha = _file_sha256(path / relative)
    size = (path / relative).stat().st_size
    digest = hashlib.sha256()
    digest.update(relative.encode() + b"\0" + file_sha.encode() + b"\n")
    return {
        "path": str(path),
        "kind": "directory",
        "size_bytes": size,
        "sha256": digest.hexdigest(),
        "files": [{"path": relative, "size_bytes": size, "sha256": file_sha}],
    }


def _write_source_run(root: Path, baseline_name: str, version: str, offset: float) -> None:
    evaluation_dir = root / baseline_name
    evaluation_dir.mkdir(parents=True)
    metrics = _metrics(offset)
    artifacts = {
        "aggregate_metrics": "aggregate_metrics.json",
        "per_sample_metrics": "per_sample_metrics.jsonl",
        "threshold_sweep": "threshold_sweep.json",
        "diagnostic_samples": "diagnostic_samples/samples.json",
    }
    manifest = {
        "status": "completed",
        "completed_at": "2026-08-09T00:00:00Z",
        "baseline": {
            "name": baseline_name,
            "version": version,
            "asset": _fixture_asset(root, baseline_name),
        },
        "sample_count": 2,
        "metrics": metrics,
        "artifacts": artifacts,
        "workspace_git": {"commit": "workspace-sha", "dirty": False},
        "harness_git": {"commit": "harness-sha", "dirty": False},
        "data_config": {
            "sources": [
                {"layout": "mit", "split_seed": 20260712, "val_fraction": 0.2},
                {"layout": "google"},
            ]
        },
    }
    (evaluation_dir / "run_manifest.json").write_text(json.dumps(manifest))
    (evaluation_dir / "aggregate_metrics.json").write_text(
        json.dumps(
            {
                "baseline": {"name": baseline_name, "version": version},
                "sample_count": 2,
                "metrics": metrics,
            }
        )
    )
    rows = []
    for index, source in enumerate(("mit", "google")):
        rows.append(
            {
                "sample_id": f"val/{index:06d}",
                "sample/dataset_source": source,
                "artifact_filters/diagnostics": {
                    "filters": [
                        {
                            "filter": "geographic_feature_filter",
                            "active": True,
                            "required": True,
                            "bundle_id": "natural-earth-v5.1.2",
                            "removed_pixel_count": 1 if index == 0 else 2,
                            "ancillary_sources": [
                                {
                                    "id": "natural_earth_10m_coastline",
                                    "version": "5.1.2",
                                    "sha256": "coast-sha",
                                    "size_bytes": 10,
                                },
                                {
                                    "id": "natural_earth_10m_rivers_north_america",
                                    "version": "5.1.2",
                                    "sha256": "river-sha",
                                    "size_bytes": 20,
                                },
                            ],
                        },
                        {
                            "filter": "scanline_artifact_filter",
                            "min_length_pixels": 128,
                            "max_probability_std": 0.03,
                            "removed_pixel_count": 0,
                        },
                    ]
                },
            }
        )
    (evaluation_dir / "baseline_evaluation_metadata.json").write_text(
        json.dumps({"baseline": {"name": baseline_name, "version": version, "asset_path": manifest["baseline"]["asset"]["path"]}})
    )
    (evaluation_dir / "per_sample_metrics.jsonl").write_text(
        "".join(json.dumps(row) + "\n" for row in rows)
    )
    (evaluation_dir / "threshold_sweep.json").write_text("{}\n")
    diagnostic_dir = evaluation_dir / "diagnostic_samples"
    diagnostic_dir.mkdir()
    (diagnostic_dir / "samples.json").write_text("{}\n")


def _source_root(tmp_path: Path) -> Path:
    root = tmp_path / "source"
    _write_source_run(root, MCAST_BASELINE_1_1, "1.1", 0.0)
    _write_source_run(root, MCAST_BASELINE_2_1, "2.1", 0.01)
    return root


def test_generate_and_load_canonical_targets_for_raw_and_filtered_comparisons(tmp_path: Path) -> None:
    source = _source_root(tmp_path)
    registry_path = tmp_path / "canonical" / "mcast-v1.json"

    generated = generate_canonical_baseline_targets(
        source_root=source,
        output_path=registry_path,
    )
    loaded = load_canonical_baseline_targets(registry_path)
    metrics = canonical_baseline_metrics(registry_path)

    assert loaded == generated
    assert "source_evaluation_root" not in loaded
    assert loaded["canonical_artifact_root"] == "."
    assert loaded["comparison_modes"]["unfiltered"]["metric_namespace"] == "raw"
    filtered = loaded["comparison_modes"]["artifact_filtered"]
    assert filtered["metric_namespace"] == "filtered"
    assert [item["name"] for item in filtered["artifact_filters"]] == [
        "geographic_feature_filter",
        "scanline_artifact_filter",
    ]
    assert loaded["sample_set"] == {
        "sample_count": 2,
        "sample_ids_sha256": "2a2e942de7deb5bab18644fa14af5f404dc25da58fd5d9f195580391df4a5278",
        "dataset_source_counts": {"google": 1, "mit": 1},
    }
    assert set(metrics) == {MCAST_BASELINE_1_1, MCAST_BASELINE_2_1}
    assert metrics[MCAST_BASELINE_2_1]["raw/dice"] == pytest.approx(0.41)
    assert metrics[MCAST_BASELINE_2_1]["filtered/dice"] == pytest.approx(0.40)
    assert metrics[MCAST_BASELINE_1_1]["baseline/target_registry_path"] == str(
        registry_path.resolve()
    )
    aggregate_path = Path(metrics[MCAST_BASELINE_1_1]["baseline/aggregate_metrics_path"])
    assert aggregate_path.is_file()
    assert aggregate_path.is_relative_to(registry_path.parent.resolve())
    for baseline in loaded["baselines"].values():
        assert all(not artifact["path"].startswith("..") for artifact in baseline["artifacts"].values())
        assert baseline["asset"]["path"].startswith("model-assets/")
        assert (registry_path.parent / baseline["asset"]["path"]).exists()
    canonical_manifest = json.loads(
        (registry_path.parent / MCAST_BASELINE_1_1 / "run_manifest.json").read_text()
    )
    assert canonical_manifest["baseline"]["asset"]["path"] == "model-assets/detection-1.1.pt"
    assert canonical_manifest["data_config"]["mcast_detection_1_1_path"] == "canonical/model-assets/detection-1.1.pt"
    assert canonical_manifest["data_config"]["mcast_detection_2_1_path"] == "canonical/model-assets/detection-2.1"


def test_acceptance_report_loads_configured_canonical_raw_and_filtered_targets(tmp_path: Path) -> None:
    baselines_root = tmp_path / "baselines"
    source = _source_root(baselines_root)
    registry_path = baselines_root / "canonical" / "mcast-v1.json"
    generate_canonical_baseline_targets(source_root=source, output_path=registry_path)

    class TrustedTrainingAdapter:
        data_config = {
            "data_roots": {
                "training": str(tmp_path / "training"),
                "ancillary": str(tmp_path / "ancillary"),
                "baselines": str(baselines_root),
            },
            "canonical_baseline_targets": "canonical/mcast-v1.json",
        }

    evaluator = ABIEvaluationAdapter(
        training_adapter=TrustedTrainingAdapter(),
        filter_pipeline=ABIArtifactFilterPipeline(filters=()),
    )
    report = evaluator.build_acceptance_gate_report(
        candidate_metrics={
            "raw/dice": 0.42,
            "raw/predicted_positive_pixel_count": 100.0,
            "filtered/dice": 0.41,
            "filtered/recall": 0.38,
            "filtered/contrail_connectivity": 0.56,
            "artifact_filters/removed_pixel_count": 3.0,
        }
    )

    assert report["baseline_target_registry"] == {
        "id": "abi-mcast-working-validation-v1",
        "path": str(registry_path.resolve()),
    }
    assert report["comparison_targets"]["unfiltered"]["metric"] == "raw/dice"
    assert report["comparison_targets"]["unfiltered"]["baseline"] == pytest.approx(0.41)
    assert report["comparison_targets"]["artifact_filtered"]["metric"] == "filtered/dice"
    assert report["comparison_targets"]["artifact_filtered"]["baseline"] == pytest.approx(0.40)
    assert Path(report["best_baseline"]["aggregate_metrics_path"]).is_file()


def test_registry_is_independent_of_source_and_detects_changed_canonical_artifact(tmp_path: Path) -> None:
    source = _source_root(tmp_path)
    registry_path = tmp_path / "canonical" / "mcast-v1.json"
    generate_canonical_baseline_targets(source_root=source, output_path=registry_path)

    (source / MCAST_BASELINE_1_1 / "threshold_sweep.json").write_text('{"changed":true}\n')
    load_canonical_baseline_targets(registry_path)

    canonical_sweep = registry_path.parent / MCAST_BASELINE_1_1 / "threshold_sweep.json"
    canonical_sweep.write_text('{"changed":true}\n')
    with pytest.raises(ValueError, match="checksum mismatch"):
        load_canonical_baseline_targets(registry_path)


def test_registry_detects_changed_canonical_model_asset(tmp_path: Path) -> None:
    source = _source_root(tmp_path)
    registry_path = tmp_path / "canonical" / "mcast-v1.json"
    generate_canonical_baseline_targets(source_root=source, output_path=registry_path)
    (registry_path.parent / "model-assets" / "detection-1.1.pt").write_bytes(b"changed")

    with pytest.raises(ValueError, match="model asset checksum mismatch"):
        load_canonical_baseline_targets(registry_path)


def test_registry_rejects_artifact_paths_outside_canonical_root(tmp_path: Path) -> None:
    source = _source_root(tmp_path)
    registry_path = tmp_path / "canonical" / "mcast-v1.json"
    generate_canonical_baseline_targets(source_root=source, output_path=registry_path)
    registry = json.loads(registry_path.read_text())
    registry["baselines"][MCAST_BASELINE_1_1]["artifacts"]["aggregate_metrics"]["path"] = "../outside.json"
    registry_path.write_text(json.dumps(registry))

    with pytest.raises(ValueError, match="must stay beneath"):
        load_canonical_baseline_targets(registry_path)


def test_canonical_target_path_is_relative_to_named_baselines_root(tmp_path: Path) -> None:
    roots = {
        "training": str(tmp_path / "training"),
        "ancillary": str(tmp_path / "ancillary"),
        "baselines": str(tmp_path / "baselines"),
    }
    resolved = resolve_canonical_baseline_targets_path(
        {
            "data_roots": roots,
            "canonical_baseline_targets": "canonical/mcast-v1.json",
        }
    )

    assert resolved == (tmp_path / "baselines" / "canonical" / "mcast-v1.json").resolve()


def test_canonical_target_path_cannot_escape_named_baselines_root(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="must resolve beneath data_roots.baselines"):
        resolve_canonical_baseline_targets_path(
            {
                "data_roots": {
                    "training": str(tmp_path / "training"),
                    "ancillary": str(tmp_path / "ancillary"),
                    "baselines": str(tmp_path / "baselines"),
                },
                "canonical_baseline_targets": "../elsewhere.json",
            }
        )
