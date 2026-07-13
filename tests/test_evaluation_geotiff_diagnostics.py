from __future__ import annotations

import numpy as np
import pytest
import torch
from PIL import Image

from abi_contrail.artifact_filters import ABIArtifactFilterPipeline, GeographicFeatureFilter, ScanlineArtifactFilter
from abi_contrail.evaluation import _evaluate_probability_tensor


class _DiagnosticDataset:
    def __len__(self) -> int:
        return 3

    def filter_context(self, index: int) -> dict[str, object]:
        lon = np.tile(np.linspace(-100.0, -99.7, 4), (4, 1))
        lat = np.tile(np.linspace(40.3, 40.0, 4)[:, np.newaxis], (1, 4))
        context: dict[str, object] = {"longitude": lon, "latitude": lat}
        if index == 0:
            feature_mask = np.zeros((4, 4), dtype=bool)
            feature_mask[1, 1] = True
            context["geographic_feature_mask"] = feature_mask
        return context

    def sample_metadata(self, index: int) -> dict[str, object]:
        return {"dataset_source": "mit", "scene_name": f"scene-{index}", "row": index, "col": 2 * index}


def test_evaluation_writes_selected_filtered_and_unfiltered_geotiff_diagnostics(tmp_path) -> None:
    probabilities = torch.zeros((3, 1, 4, 4), dtype=torch.float32)
    probabilities[0, 0, 1, 1] = 0.9  # filter-hit case via geographic_feature_mask
    probabilities[1, 0, 2, 2] = 0.8  # no-filter-hit case
    probabilities[2, 0, 0, 0] = 0.7
    targets = torch.zeros_like(probabilities)
    pipeline = ABIArtifactFilterPipeline(
        filters=(GeographicFeatureFilter(pixel_buffer=0), ScanlineArtifactFilter(min_length_pixels=10)),
        pixel_area_km2=2.5,
    )

    _, per_sample, _, manifest = _evaluate_probability_tensor(
        dataset=_DiagnosticDataset(),
        probabilities=probabilities,
        targets=targets,
        threshold=0.5,
        filter_pipeline=pipeline,
        diagnostic_output_dir=tmp_path / "eval" / "diagnostic_samples",
        max_artifact_samples=2,
    )

    samples = manifest["samples"]
    assert [sample["selection_reason"] for sample in samples] == ["filter_hit", "no_filter_hit"]
    assert samples[0]["dataset_index"] == 0
    assert samples[0]["artifact_filters"]["removed_pixel_count"] == 1
    assert samples[0]["artifact_filters"]["removed_area_km2"] == pytest.approx(2.5)
    assert samples[0]["artifact_filters"]["filters_hit"] == ["geographic_feature_filter"]
    assert set(samples[0]["geotiffs"]) == {"unfiltered_prediction", "filtered_prediction"}

    unfiltered_path = tmp_path / "eval" / samples[0]["geotiffs"]["unfiltered_prediction"]
    filtered_path = tmp_path / "eval" / samples[0]["geotiffs"]["filtered_prediction"]
    assert unfiltered_path.is_file()
    assert filtered_path.is_file()
    assert np.asarray(Image.open(unfiltered_path))[1, 1] == 1
    assert np.asarray(Image.open(filtered_path))[1, 1] == 0
    assert per_sample[0]["artifact_filters/diagnostic_geotiffs"] == samples[0]["geotiffs"]

    tags = Image.open(unfiltered_path).tag_v2
    assert 33550 in tags  # ModelPixelScaleTag
    assert 33922 in tags  # ModelTiepointTag
    assert 34735 in tags  # GeoKeyDirectoryTag with EPSG:4326
    assert samples[0]["georeferencing"]["crs"] == "EPSG:4326"


def test_evaluation_diagnostic_selection_uses_available_case_when_only_one_category(tmp_path) -> None:
    probabilities = torch.ones((2, 1, 4, 4), dtype=torch.float32)
    targets = torch.zeros_like(probabilities)
    pipeline = ABIArtifactFilterPipeline(filters=(ScanlineArtifactFilter(min_length_pixels=10),), pixel_area_km2=1.0)

    _, _, _, manifest = _evaluate_probability_tensor(
        dataset=_DiagnosticDataset(),
        probabilities=probabilities,
        targets=targets,
        threshold=0.5,
        filter_pipeline=pipeline,
        diagnostic_output_dir=tmp_path / "eval" / "diagnostic_samples",
        max_artifact_samples=2,
    )

    assert manifest["samples"]
    assert {sample["selection_reason"] for sample in manifest["samples"]} == {"no_filter_hit"}
