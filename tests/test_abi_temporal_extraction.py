from __future__ import annotations

from datetime import datetime, timezone

import numpy as np
import pytest
from pyproj import CRS

from abi_contrail.temporal_grids import RegularSourceGrid, TemporalPatchGrid, extract_regular_source_patch


def _target_grid(*, x0: float, y0: float, size: int = 3) -> TemporalPatchGrid:
    return TemporalPatchGrid(
        crs=CRS.from_epsg(4326),
        height=size,
        width=size,
        x0=x0,
        dx_col=1.0,
        dx_row=0.0,
        y0=y0,
        dy_col=0.0,
        dy_row=1.0,
    )


def _source_grid() -> RegularSourceGrid:
    variables = {}
    for channel in range(1, 17):
        values = np.zeros((5, 5), dtype=np.float32)
        rows, cols = np.indices((5, 5))
        values[:, :] = channel * 100 + rows * 10 + cols
        variables[f"CMI_C{channel:02d}"] = values
    return RegularSourceGrid(
        crs=CRS.from_epsg(4326),
        x=np.arange(5, dtype=float),
        y=np.arange(5, dtype=float),
        variables=variables,
    )


def test_regular_source_patch_extraction_returns_19_channel_patch_without_padding() -> None:
    patch = extract_regular_source_patch(
        _source_grid(),
        _target_grid(x0=1.0, y0=1.0),
        solar_zenith_angle_function=lambda _time, lon, lat: lon + lat,
        observation_time="test-time",
    )

    assert patch.shape == (3, 3, 19)
    assert patch[0, 0, 0] == 100 + 10 + 1
    assert patch[2, 2, 15] == 1600 + 30 + 3
    np.testing.assert_array_equal(patch[:, :, 16], np.array([[1, 2, 3], [1, 2, 3], [1, 2, 3]], dtype=np.float32))
    np.testing.assert_array_equal(patch[:, :, 17], np.array([[1, 1, 1], [2, 2, 2], [3, 3, 3]], dtype=np.float32))
    np.testing.assert_array_equal(patch[:, :, 18], patch[:, :, 16] + patch[:, :, 17])


def test_regular_source_patch_normalizes_timezone_aware_observation_time_for_sza() -> None:
    observed_times = []

    def fake_sza(observation_time: object, lon: np.ndarray, lat: np.ndarray) -> np.ndarray:
        observed_times.append(observation_time)
        return lon + lat

    extract_regular_source_patch(
        _source_grid(),
        _target_grid(x0=1.0, y0=1.0),
        solar_zenith_angle_function=fake_sza,
        observation_time=datetime(2020, 1, 1, 3, 4, 5, tzinfo=timezone.utc),
    )

    assert observed_times == [datetime(2020, 1, 1, 3, 4, 5)]


def test_regular_source_patch_extraction_fails_closed_for_partial_coverage() -> None:
    with pytest.raises(ValueError, match="fully cover"):
        extract_regular_source_patch(
            _source_grid(),
            _target_grid(x0=3.0, y0=3.0),
            solar_zenith_angle_function=lambda _time, lon, lat: lon + lat,
            observation_time="test-time",
        )
