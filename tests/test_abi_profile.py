from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import zarr

from abi_contrail.profile import generate_dataset_profile, main, missing_data_profile


def _write_mit_full_scene(tmp_path: Path) -> tuple[Path, Path]:
    inputs_path = tmp_path / "mit_inputs.zarr"
    labels_path = tmp_path / "mit_labels.zarr"
    inputs = zarr.open_array(str(inputs_path), mode="w", shape=(2, 256, 256, 19), dtype="f4")
    labels = zarr.open_array(str(labels_path), mode="w", shape=(2, 256, 256), dtype="u1")
    inputs[:] = 0
    labels[:] = 0
    labels[0, :8, :8] = 1
    return inputs_path, labels_path


def _write_google_patches(tmp_path: Path) -> tuple[Path, Path]:
    inputs_path = tmp_path / "google_inputs.zarr"
    labels_path = tmp_path / "google_labels.zarr"
    inputs_group = zarr.open_group(str(inputs_path), mode="w")
    labels_group = zarr.open_group(str(labels_path), mode="w")
    inputs_group.create_array("inputs", data=np.zeros((2, 256, 256, 19), dtype=np.float32))
    labels = np.zeros((2, 256, 256), dtype=np.uint8)
    labels[1, :4, :4] = 2
    labels_group.create_array("labels", data=labels)
    return inputs_path, labels_path


def test_generate_dataset_profile_summarizes_mit_and_google_counts(tmp_path: Path) -> None:
    mit_inputs, mit_labels = _write_mit_full_scene(tmp_path)
    google_inputs, google_labels = _write_google_patches(tmp_path)

    profile = generate_dataset_profile(
        {
            "dataset_root": str(tmp_path),
            "sources": [
                {
                    "layout": "mit",
                    "inputs_zarr": str(mit_inputs),
                    "labels_zarr": str(mit_labels),
                    "scene_names": ["mit-a", "mit-b"],
                    "val_fraction": 0.5,
                    "split_seed": 1,
                },
                {
                    "layout": "google",
                    "inputs_zarr": str(google_inputs),
                    "labels_zarr": str(google_labels),
                    "metadata_rows": [
                        {"scene_name": "train-000/patch.zarr", "sample_index": 0, "positive": False},
                        {"scene_name": "validation-000/patch.zarr", "sample_index": 1, "positive": True},
                    ],
                },
            ],
        }
    )

    assert profile["task"]["name"] == "binary GOES ABI Contrail Segmentation"
    assert {source["dataset_source"] for source in profile["source_profiles"]} == {"mit", "google"}
    assert profile["combined_counts"]["split_counts"]["total"] == 4
    assert profile["combined_counts"]["positive_patch_count"] == 2
    assert profile["schema_version"] == "dataset-profile.v1"
    assert profile["abi_channels"]["source_channel_indices_included"] == list(range(16))
    assert profile["abi_channels"]["source_channel_indices_excluded"] == [16, 17]
    assert len(profile["abi_channels"]["semantics"]) == 16
    assert profile["abi_channels"]["semantics"][0]["unit"] == "reflectance_factor"
    assert profile["abi_channels"]["semantics"][6]["unit"] == "kelvin"
    for source in profile["source_profiles"]:
        assert set(source["mask_area_distribution"]["by_split"]) == {"train", "validation"}
        assert "safe_channel_statistics" not in source
        assert "inputs_zarr" not in source
        assert "labels_zarr" not in source
    for statistics in profile["abi_channels"]["safe_range_statistics_by_source"].values():
        assert len(statistics["channels"]) == 16
    assert str(tmp_path) not in json.dumps(profile)
    assert profile["split_policy"]["google_split_policy"] == "respect_google_scene_name_train_validation_provenance"
    assert profile["split_policy"]["mit_split_policy"] == "deterministic_whole_scene_train_validation_split_before_windowing"
    assert any("Longitude and latitude" in caveat for caveat in profile["projection_caveats"])


def test_generate_dataset_profile_loads_source_metadata_from_parquet(tmp_path: Path) -> None:
    google_inputs, google_labels = _write_google_patches(tmp_path)
    pd.DataFrame(
        [
            {"scene": "train-000", "contrail_pixels": 0, "goes_time": "2020-01-01 00:00"},
            {"scene": "validation-000", "contrail_pixels": 16, "goes_time": "2020-01-01 00:10"},
        ]
    ).to_parquet(tmp_path / "metadata.parquet")

    profile = generate_dataset_profile(
        {
            "dataset_root": str(tmp_path),
            "layout": "google",
            "inputs_zarr": str(google_inputs),
            "labels_zarr": str(google_labels),
            "metadata_parquet": "metadata.parquet",
        }
    )

    assert profile["combined_counts"]["split_counts"] == {"train": 1, "validation": 1, "total": 2}
    assert profile["combined_counts"]["positive_patch_count"] == 1


def test_profile_missing_data_placeholder_is_explicit() -> None:
    profile = missing_data_profile({"dataset_root": "data"}, "not mounted")

    assert profile["status"] == "missing_optional_data"
    assert profile["reason"] == "not mounted"
    assert "mit" in profile["expected_sources"]
    assert "google" in profile["expected_sources"]


def test_profile_cli_allow_missing_writes_placeholder(tmp_path: Path) -> None:
    output = tmp_path / "profile.json"

    exit_code = main(["--allow-missing", "--output", str(output)])

    assert exit_code == 0
    payload = json.loads(output.read_text())
    assert payload["status"] == "missing_optional_data"
