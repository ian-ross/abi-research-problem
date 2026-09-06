from __future__ import annotations

import json

import numpy as np
import pytest
from pyproj import CRS

from abi_contrail.datasets import ABIPatchIndexRecord
from abi_contrail.temporal_grids import (
    google_temporal_patch_grid,
    mit_temporal_patch_grid,
    validate_google_center_grid_against_materialized_patch,
)


def test_mit_temporal_patch_grid_uses_fixed_mit_scene_grid_and_record_window() -> None:
    record = ABIPatchIndexRecord(
        dataset_source="mit",
        split="train",
        scene_name="mit-scene",
        scene_index=0,
        goes_time="2020-01-01T00:00:00Z",
        row=3,
        col=7,
        positive=False,
        sample_index=None,
    )

    grid = mit_temporal_patch_grid(record)

    assert grid.height == 256
    assert grid.width == 256
    assert grid.crs.to_proj4().startswith("+proj=ortho")
    assert grid.x(0, 0) == pytest.approx(-2440354.0 + 2000.0 * 7)
    assert grid.y(0, 0) == pytest.approx(1320437.0 - 2000.0 * 3)
    assert grid.x(4, 2) == pytest.approx(-2440354.0 + 2000.0 * 9)
    assert grid.y(4, 2) == pytest.approx(1320437.0 - 2000.0 * 7)


def test_google_temporal_patch_grid_uses_patch_specific_location_metadata() -> None:
    location = {
        "projection_wkt": CRS.from_epsg(4326).to_wkt(),
        "col_min": -105.0,
        "row_min": 40.0,
        "col_size": 0.02,
        "row_size": -0.02,
    }

    grid = google_temporal_patch_grid(json.dumps(location))

    assert grid.height == 256
    assert grid.width == 256
    assert grid.crs.to_epsg() == 4326
    assert grid.x(0, 0) == pytest.approx(-105.0)
    assert grid.y(0, 0) == pytest.approx(40.0)
    assert grid.x(10, 3) == pytest.approx(-104.94)
    assert grid.y(10, 3) == pytest.approx(39.80)


def test_google_center_grid_validation_compares_trusted_lon_lat_channels_to_location_grid() -> None:
    location = {
        "projection_wkt": CRS.from_epsg(4326).to_wkt(),
        "col_min": -100.0,
        "row_min": 30.0,
        "col_size": 0.01,
        "row_size": 0.01,
    }
    raw_center = np.zeros((256, 256, 19), dtype=np.float32)
    rows, cols = np.indices((256, 256))
    raw_center[..., 16] = location["col_min"] + location["col_size"] * cols
    raw_center[..., 17] = location["row_min"] + location["row_size"] * rows

    report = validate_google_center_grid_against_materialized_patch(raw_center, location, sample_step=64)

    assert report["valid"] is True
    assert report["max_abs_lon_error"] < 1e-5
    assert report["max_abs_lat_error"] < 1e-5

    raw_center[128, 128, 16] += 1.0
    with pytest.raises(ValueError, match="Google location grid validation failed"):
        validate_google_center_grid_against_materialized_patch(raw_center, location, sample_step=64, tolerance_degrees=0.001)
