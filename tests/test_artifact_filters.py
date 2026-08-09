from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from abi_contrail.artifact_filters import ABIArtifactFilterPipeline, GeographicFeatureFilter, ScanlineArtifactFilter


def test_geographic_feature_filter_removes_predictions_on_provider_owned_raster_mask() -> None:
    prediction = np.zeros((1, 8, 8), dtype=bool)
    prediction[0, 3, 1:6] = True
    probabilities = prediction.astype(np.float32) * 0.8
    feature_mask = np.zeros((8, 8), dtype=bool)
    feature_mask[3, 2:4] = True

    result = GeographicFeatureFilter(pixel_buffer=0).apply(
        prediction,
        probabilities,
        context={"geographic_feature_mask": feature_mask},
    )

    assert result.diagnostics["removed_pixel_count"] == 2
    assert result.filtered_mask[0, 3, 1]
    assert not result.filtered_mask[0, 3, 2]
    assert not result.filtered_mask[0, 3, 3]
    assert result.filtered_probabilities[0, 3, 2] == 0.0


def test_scanline_artifact_filter_removes_long_constant_abi_y_runs_only() -> None:
    prediction = np.zeros((1, 10, 16), dtype=bool)
    probabilities = np.zeros((1, 10, 16), dtype=np.float32)
    prediction[0, 4, 1:14] = True
    probabilities[0, 4, 1:14] = 0.72
    prediction[0, 6, 1:14] = True
    probabilities[0, 6, 1:14] = np.linspace(0.55, 0.95, 13)

    result = ScanlineArtifactFilter(min_length_pixels=10, max_probability_std=0.01).apply(prediction, probabilities)

    assert result.diagnostics["removed_pixel_count"] == 13
    assert not result.filtered_mask[0, 4, 7]
    assert result.filtered_mask[0, 6, 7]


def test_geographic_feature_filter_parses_ancillary_vectors_once_across_abi_patches(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    coastline = tmp_path / "coastline.geojson"
    coastline.write_text(
        json.dumps(
            {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "properties": {},
                        "geometry": {"type": "LineString", "coordinates": [[0.0, 0.0], [1.0, 1.0]]},
                    }
                ],
            }
        )
    )
    original_read_text = Path.read_text
    reads = 0

    def counting_read_text(path: Path, *args: object, **kwargs: object) -> str:
        nonlocal reads
        if path.resolve() == coastline.resolve():
            reads += 1
        return original_read_text(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", counting_read_text)
    artifact_filter = GeographicFeatureFilter(coastline_geojson=coastline, pixel_buffer=0, active=True)
    prediction = np.ones((1, 2, 2), dtype=bool)
    probabilities = prediction.astype(np.float32)
    context = {
        "longitude": np.asarray([[0.0, 1.0], [0.0, 1.0]]),
        "latitude": np.asarray([[0.0, 0.0], [1.0, 1.0]]),
    }

    first = artifact_filter.apply(prediction, probabilities, context=context)
    second = artifact_filter.apply(prediction, probabilities, context=context)

    assert reads == 1
    assert np.array_equal(second.filtered_mask, first.filtered_mask)
    assert first.diagnostics["feature_pixel_count"] == 2


def test_artifact_filter_pipeline_reports_removed_pixel_count_and_area() -> None:
    prediction = np.zeros((1, 6, 6), dtype=bool)
    prediction[0, 2, 1:5] = True
    probabilities = prediction.astype(np.float32) * 0.9
    feature_mask = np.zeros((6, 6), dtype=bool)
    feature_mask[2, 2] = True
    pipeline = ABIArtifactFilterPipeline(
        filters=(GeographicFeatureFilter(pixel_buffer=0), ScanlineArtifactFilter(min_length_pixels=4, max_probability_std=0.01)),
        pixel_area_km2=4.0,
    )

    result = pipeline.apply(prediction, probabilities, context={"geographic_feature_mask": feature_mask})

    assert result.diagnostics["removed_pixel_count"] == 1
    assert result.diagnostics["removed_area_km2"] == 4.0
    assert len(result.diagnostics["filters"]) == 2
