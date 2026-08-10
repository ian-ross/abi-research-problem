from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest
import zarr

import abi_contrail.campaign_context as campaign_context
from abi_contrail.baseline_segmenters import MCAST_BASELINE_NAMES
from abi_contrail.campaign_context import (
    generate_agent_campaign_context,
    load_agent_campaign_context,
    validate_agent_campaign_context,
)


def _data_config(tmp_path: Path) -> dict[str, object]:
    inputs_path = tmp_path / "inputs.zarr"
    labels_path = tmp_path / "labels.zarr"
    inputs = zarr.open_group(str(inputs_path), mode="w")
    labels = zarr.open_group(str(labels_path), mode="w")
    values = np.zeros((2, 256, 256, 19), dtype=np.float32)
    for channel in range(16):
        values[..., channel] = channel + 1
    inputs.create_array("inputs", data=values)
    mask = np.zeros((2, 256, 256), dtype=np.uint8)
    mask[1, :8, :8] = 1
    labels.create_array("labels", data=mask)
    return {
        "dataset_root": str(tmp_path),
        "layout": "google",
        "inputs_zarr": str(inputs_path),
        "labels_zarr": str(labels_path),
        "metadata_rows": [
            {"scene_name": "train-000", "sample_index": 0, "positive": False},
            {"scene_name": "validation-000", "sample_index": 1, "positive": True},
        ],
    }


def _metrics(offset: float) -> dict[str, float]:
    result: dict[str, float] = {}
    for namespace, adjustment in (("raw", 0.0), ("filtered", -0.01)):
        for name, value in (
            ("dice", 0.4),
            ("precision", 0.45),
            ("recall", 0.36),
            ("contrail_connectivity", 0.54),
        ):
            result[f"{namespace}/{name}"] = value + adjustment + offset
    for source in ("mit", "google"):
        for namespace in ("raw", "filtered"):
            for name in ("dice", "precision", "recall", "contrail_connectivity"):
                result[f"source/{source}/{namespace}/{name}"] = result[f"{namespace}/{name}"]
    result["artifact_filters/removed_area_km2"] = 12.0
    return result


def _registry(tmp_path: Path) -> tuple[Path, dict[str, object]]:
    registry_path = tmp_path / "canonical" / "registry.json"
    registry_path.parent.mkdir()
    baselines = {}
    for index, name in enumerate(MCAST_BASELINE_NAMES):
        root = registry_path.parent / name
        root.mkdir()
        aggregate = {
            "threshold": 0.42 if index == 0 else 0.314,
            "metrics": _metrics(index * 0.01),
        }
        sweep = {
            "thresholds": [0.1, 0.2, 0.3],
            "best_threshold_by_raw_dice": {"threshold": 0.2, "dice": 0.41},
            "best_threshold_by_filtered_dice": {"threshold": 0.1, "dice": 0.40},
            "precision_recall_equal_threshold_raw": {"threshold": 0.2},
            "precision_recall_equal_threshold": {"threshold": 0.1},
            "primary_metric_note": "diagnostic only",
        }
        aggregate_path = root / "aggregate_metrics.json"
        sweep_path = root / "threshold_sweep.json"
        aggregate_path.write_text(json.dumps(aggregate))
        sweep_path.write_text(json.dumps(sweep))
        baselines[name] = {
            "name": name,
            "version": "1.1" if index == 0 else "2.1",
            "sample_count": 2,
            "completed_at": "2026-08-09T00:00:00Z",
            "metrics": aggregate["metrics"],
            "filter_removed_pixel_counts": {
                "geographic_feature_filter": 3,
                "scanline_artifact_filter": 0,
            },
            "artifacts": {
                "aggregate_metrics": {
                    "path": f"{name}/aggregate_metrics.json",
                    "sha256": "aggregate-sha",
                    "size_bytes": aggregate_path.stat().st_size,
                },
                "threshold_sweep": {
                    "path": f"{name}/threshold_sweep.json",
                    "sha256": "threshold-sha",
                    "size_bytes": sweep_path.stat().st_size,
                },
            },
        }
    registry = {
        "schema": "abi_canonical_baseline_targets/v1",
        "registry_id": "abi-mcast-working-validation-v1",
        "generated_at": "2026-08-09T00:00:00Z",
        "sample_set": {
            "sample_count": 2,
            "dataset_source_counts": {"mit": 1, "google": 1},
            "sample_ids_sha256": "sample-sha",
        },
        "comparison_modes": {
            "unfiltered": {"metric_namespace": "raw", "artifact_filters": []},
            "artifact_filtered": {
                "metric_namespace": "filtered",
                "artifact_filters": [
                    {"name": "geographic_feature_filter", "active": True},
                    {"name": "scanline_artifact_filter", "active": True},
                ],
            },
        },
        "provenance": {
            "workspace_git": {"commit": "workspace-sha", "dirty": False, "root": "/host"},
            "harness_git": {"commit": "harness-sha", "dirty": False, "root": "/host"},
        },
        "baselines": baselines,
    }
    registry_path.write_text(json.dumps(registry))
    return registry_path, registry


def _canary(tmp_path: Path) -> tuple[Path, Path]:
    run_dir = tmp_path / "run_abi025"
    evaluation_dir = run_dir / "evaluation_abi025"
    evaluation_dir.mkdir(parents=True)
    run_metadata = {
        "run_id": "run_abi025",
        "status": "completed",
        "created_at": "2026-08-10T00:00:00Z",
        "updated_at": "2026-08-10T00:01:00Z",
        "candidate_source": {"path": "/host/candidates/abi025_manual_canary_v1"},
        "dataset": {"input_mode": "abi_16ch"},
        "sample_counts": {"train": 16, "validation": 16},
        "training_policy": {"early_stopping": {"enabled": False}},
    }
    evaluation_metadata = {
        "evaluation_id": "eval_abi025",
        "status": "completed",
        "completed_at": "2026-08-10T00:02:00Z",
        "mode": "whole_validation_failure_analysis",
        "source_run": {"run_id": "run_abi025"},
    }
    metrics = _metrics(0.0)
    aggregate = {
        "evaluation_id": "eval_abi025",
        "sample_count": 2,
        "threshold": 0.5,
        "metrics": metrics,
    }
    threshold = {
        "thresholds": [0.1, 0.5],
        "best_threshold_by_raw_dice": {"threshold": 0.1, "dice": 0.4},
        "best_threshold_by_filtered_dice": {"threshold": 0.1, "dice": 0.39},
    }
    acceptance = {
        "candidate_run_id": "run_abi025",
        "baseline_target_registry": {"id": "abi-mcast-working-validation-v1", "path": "/host/registry.json"},
        "overall_status": "gate_flags_present",
        "promotion_decision": "human_review_required",
        "human_review_required": True,
        "human_review_note": "review input only",
        "best_baseline": {
            "name": "mcast_detection_2_1",
            "selection_metric": "filtered/dice",
            "selection_value": 0.4,
            "target_registry_id": "abi-mcast-working-validation-v1",
            "aggregate_metrics_path": "/host/aggregate.json",
        },
        "aggregate_comparison": {
            "baseline": 0.4,
            "baseline_name": "mcast_detection_2_1",
            "candidate": 0.1,
            "candidate_beats_baseline": False,
            "delta": -0.3,
            "metric": "filtered/dice",
            "target_registry_id": "abi-mcast-working-validation-v1",
        },
        "contrail_connectivity_comparison": {"baseline": 0.2, "candidate": 0.3, "delta": 0.1},
        "recall_regression": {"flagged": True},
        "dataset_source_failures": [],
        "artifact_filter_dependence": {"flagged": False},
        "flags": [{"id": "below_baseline", "severity": "fail", "message": "below"}],
    }
    for name, payload in (
        ("run_metadata.json", run_metadata),
        ("evaluation_metadata.json", evaluation_metadata),
        ("aggregate_metrics.json", aggregate),
        ("threshold_sweep.json", threshold),
        ("acceptance_report.json", acceptance),
    ):
        destination = run_dir / name if name == "run_metadata.json" else evaluation_dir / name
        destination.write_text(json.dumps(payload))
    return run_dir, evaluation_dir


def test_campaign_context_extracts_only_curated_aggregate_context(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    registry_path, registry = _registry(tmp_path)
    run_dir, evaluation_dir = _canary(tmp_path)
    monkeypatch.setattr(
        campaign_context,
        "load_canonical_baseline_targets",
        lambda path, verify_artifacts: registry,
    )

    artifact = generate_agent_campaign_context(
        _data_config(tmp_path),
        registry_path=registry_path,
        run_dir=run_dir,
        evaluation_dir=evaluation_dir,
        workspace_config_sha256="workspace-config-sha",
        generation_timestamp="2026-08-10T00:03:00Z",
    )

    assert artifact["dataset_profile"]["combined_counts"]["split_counts"] == {
        "train": 1,
        "validation": 1,
        "total": 2,
    }
    channel_stats = artifact["dataset_profile"]["abi_channels"]
    assert channel_stats["source_channel_indices_included"] == list(range(16))
    assert channel_stats["source_channel_indices_excluded"] == [16, 17]
    assert channel_stats["semantics"][0]["unit"] == "reflectance_factor"
    assert channel_stats["semantics"][6]["unit"] == "kelvin"
    mcast = artifact["canonical_mcast"]["baselines"]["mcast_detection_1_1"]
    assert mcast["aggregate_metrics"]["raw"]["precision"] == pytest.approx(0.45)
    assert mcast["threshold_behavior"]["best_by_raw_dice"]["threshold"] == 0.2
    assert mcast["artifact_filter_effect"]["removed_pixel_counts"]["geographic_feature_filter"] == 3
    canary = artifact["abi_025_manual_canary"]
    assert canary["run"]["id"] == "run_abi025"
    assert canary["acceptance_context"]["canonical_registry_id"] == "abi-mcast-working-validation-v1"
    assert "/host" not in json.dumps(artifact)
    validate_agent_campaign_context(artifact)


def test_campaign_context_rejects_canary_linkage_mismatch(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    registry_path, registry = _registry(tmp_path)
    run_dir, evaluation_dir = _canary(tmp_path)
    metadata_path = evaluation_dir / "evaluation_metadata.json"
    metadata = json.loads(metadata_path.read_text())
    metadata["source_run"]["run_id"] = "wrong-run"
    metadata_path.write_text(json.dumps(metadata))
    monkeypatch.setattr(
        campaign_context,
        "load_canonical_baseline_targets",
        lambda path, verify_artifacts: registry,
    )

    with pytest.raises(ValueError, match="identity mismatch"):
        generate_agent_campaign_context(
            _data_config(tmp_path),
            registry_path=registry_path,
            run_dir=run_dir,
            evaluation_dir=evaluation_dir,
        )


def test_loaded_campaign_context_rejects_forbidden_path_leakage(tmp_path: Path) -> None:
    artifact = {
        "artifact_type": "agent_campaign_context",
        "schema": "abi_agent_campaign_context/v1",
        "provenance": {},
        "safety_contract": {},
        "dataset_profile": {"leak": "/host/training"},
        "canonical_mcast": {},
        "abi_025_manual_canary": {},
    }
    path = tmp_path / "context.json"
    path.write_text(json.dumps(artifact))

    with pytest.raises(ValueError, match="host-only"):
        load_agent_campaign_context(path)

    artifact["dataset_profile"] = {"longitude_statistics": {"min": -100.0}}
    with pytest.raises(ValueError, match="forbidden"):
        validate_agent_campaign_context(artifact)
