from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from abi_contrail.datasets import ABIPatchIndexRecord, mark_temporal_patch_extracted, write_temporal_cache_database, temporal_record_identity_sha256
from abi_contrail.temporal_profile import generate_temporal_eligibility_profile


def _record(source: str, split: str, index: int, *, positive: bool) -> ABIPatchIndexRecord:
    return ABIPatchIndexRecord(
        dataset_source=source,  # type: ignore[arg-type]
        split=split,  # type: ignore[arg-type]
        scene_name=f"{source}-{split}-scene-{index}",
        scene_index=index,
        goes_time=f"2020-01-01T00:{index:02d}:00Z",
        row=0,
        col=0,
        positive=positive,
        sample_index=index if source == "google" else None,
    )


def _eligibility(records: tuple[ABIPatchIndexRecord, ...]) -> dict[str, object]:
    return {
        "full_dataset_scan": True,
        "dataset_scope": {"record_identity_sha256": temporal_record_identity_sha256(records)},
        "records": [
            {
                "dataset_source": record.dataset_source,
                "split": record.split,
                "scene_name": record.scene_name,
                "scene_index": record.scene_index,
                "goes_time": record.goes_time,
                "row": record.row,
                "col": record.col,
                "sample_index": record.sample_index,
                "temporal_source_scenes": {
                    "-2": "scene-minus-two",
                    "-1": "scene-minus-one",
                    "0": "materialized_training_zarr",
                    "1": "scene-plus-one",
                    "2": "scene-plus-two",
                },
            }
            for record in records
        ],
    }


def test_temporal_eligibility_profile_summarizes_windows_without_disclosing_patch_paths(tmp_path: Path) -> None:
    temporal_root = tmp_path / "temporal-cache"
    temporal_root.mkdir()
    records = (
        _record("google", "train", 0, positive=True),
        _record("google", "train", 1, positive=False),
        _record("google", "validation", 2, positive=False),
        _record("mit", "train", 3, positive=True),
    )
    database_path = temporal_root / "abi-temporal-cache.sqlite"
    write_temporal_cache_database(database_path, cache_root=temporal_root, records=records, scenes=(), eligibility=_eligibility(records))
    for offset in (-2, -1, 1, 2):
        path = temporal_root / f"offset_{offset}.npy"
        np.save(path, np.zeros((1,), dtype=np.float32))
        mark_temporal_patch_extracted(database_path, records[0], offset, path.name)
        mark_temporal_patch_extracted(database_path, records[2], offset, path.name)
    for offset in (-1, 1):
        mark_temporal_patch_extracted(database_path, records[1], offset, f"offset_{offset}.npy")

    profile = generate_temporal_eligibility_profile(temporal_cache_root=temporal_root, max_samples=1)

    windows = {tuple(window["temporal_frame_offsets"]): window for window in profile["windows"]}
    assert windows[(0,)]["eligible_count"] == 4
    assert windows[(-1, 0, 1)]["by_source"]["google"]["train"]["eligible_count"] == 2
    assert windows[(-1, 0, 1)]["by_source"]["google"]["train"]["selected_count"] == 1
    assert windows[(-1, 0, 1)]["by_source"]["google"]["train"]["selected_positive_count"] == 1
    assert windows[(-2, -1, 0, 1, 2)]["by_source"]["google"]["train"]["eligible_count"] == 1
    assert windows[(-2, -1, 0, 1, 2)]["by_source"]["mit"]["train"]["eligible_count"] == 0
    assert profile["cache_provenance"]["dataset_scope"]["record_identity_status"] == "matches_records"
    assert profile["temporal_input_boundary"]["longitude_latitude_exposed_to_candidates"] is False

    serialized = json.dumps(profile)
    assert str(temporal_root) not in serialized
    assert "offset_-1.npy" not in serialized
    assert "google-train-scene" not in serialized
