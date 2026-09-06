from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
import xarray as xr
from pyproj import CRS

from abi_contrail.temporal_netcdf import load_regular_source_grid_from_netcdf, materialize_goes_scene


def _write_regular_scene(path: Path) -> None:
    y = np.arange(4, dtype=np.float32)
    x = np.arange(5, dtype=np.float32)
    data_vars = {
        "spatial_ref": xr.DataArray(0, attrs={"crs_wkt": CRS.from_epsg(4326).to_wkt()}),
    }
    rows, cols = np.indices((4, 5))
    for channel in range(1, 17):
        data_vars[f"CMI_C{channel:02d}"] = (("y", "x"), (channel * 100 + rows * 10 + cols).astype(np.float32))
    xr.Dataset(
        data_vars=data_vars,
        coords={"x": x, "y": y},
        attrs={"time_coverage_start": "2020-01-01T00:00:00Z", "time_coverage_end": "2020-01-01T00:01:00Z"},
    ).to_netcdf(path)


def test_load_regular_source_grid_from_netcdf_reads_crs_coordinates_and_cmi_variables(tmp_path: Path) -> None:
    scene = tmp_path / "scene.nc"
    _write_regular_scene(scene)

    grid = load_regular_source_grid_from_netcdf(scene)

    assert grid.crs.to_epsg() == 4326
    np.testing.assert_array_equal(grid.x, np.arange(5, dtype=np.float32))
    np.testing.assert_array_equal(grid.y, np.arange(4, dtype=np.float32))
    assert sorted(grid.variables) == [f"CMI_C{channel:02d}" for channel in range(1, 17)]
    assert grid.variables["CMI_C16"][3, 4] == 1600 + 30 + 4


def test_materialize_goes_scene_copies_s3_uri_with_injectable_opener(tmp_path: Path) -> None:
    payload = b"netcdf-bytes"

    def opener(uri: str):
        assert uri == "s3://noaa-goes16/ABI-L2-MCMIPC/2020/001/00/example.nc"
        import io

        return io.BytesIO(payload)

    local = materialize_goes_scene(
        "s3://noaa-goes16/ABI-L2-MCMIPC/2020/001/00/example.nc",
        tmp_path / "scene-cache",
        opener=opener,
    )

    assert local.is_file()
    assert local.read_bytes() == payload
    assert local.name.endswith("example.nc")
    assert materialize_goes_scene(str(local), tmp_path / "scene-cache") == local.resolve()


def test_load_regular_source_grid_from_goes_cf_projection_scales_scan_angles(tmp_path: Path) -> None:
    scene = tmp_path / "goes.nc"
    height = 35786023.0
    data_vars = {
        "goes_imager_projection": xr.DataArray(
            0,
            attrs={
                "grid_mapping_name": "geostationary",
                "perspective_point_height": height,
                "semi_major_axis": 6378137.0,
                "semi_minor_axis": 6356752.31414,
                "longitude_of_projection_origin": -75.0,
                "sweep_angle_axis": "x",
            },
        )
    }
    for channel in range(1, 17):
        data_vars[f"CMI_C{channel:02d}"] = (("y", "x"), np.zeros((2, 2), dtype=np.float32), {"grid_mapping": "goes_imager_projection"})
    xr.Dataset(data_vars=data_vars, coords={"x": np.array([0.1, 0.2]), "y": np.array([-0.1, -0.2])}).to_netcdf(scene)

    grid = load_regular_source_grid_from_netcdf(scene)

    assert grid.crs.to_cf()["grid_mapping_name"] == "geostationary"
    np.testing.assert_allclose(grid.x, np.array([0.1, 0.2]) * height)
    np.testing.assert_allclose(grid.y, np.array([-0.1, -0.2]) * height)
