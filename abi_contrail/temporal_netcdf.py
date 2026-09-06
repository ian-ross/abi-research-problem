"""Trusted NetCDF/S3 I/O for ABI temporal provisioning."""

from __future__ import annotations

import hashlib
import shutil
from collections.abc import Callable
from pathlib import Path
from typing import BinaryIO

import numpy as np
import xarray as xr
from pyproj import CRS

from abi_contrail.temporal_grids import ABI_VARS, RegularSourceGrid


def materialize_goes_scene(
    path_or_uri: str | Path,
    cache_root: str | Path,
    *,
    opener: Callable[[str], BinaryIO] | None = None,
) -> Path:
    """Return a local NetCDF path, downloading/caching S3 scenes when needed."""

    value = str(path_or_uri)
    if not value.startswith("s3://"):
        path = Path(value).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(f"GOES ABI scene does not exist: {path}")
        return path
    root = Path(cache_root).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]
    destination = root / f"{digest}-{Path(value).name}"
    if destination.is_file():
        return destination
    if opener is None:
        import fsspec

        def opener(uri: str) -> BinaryIO:
            return fsspec.open(uri, mode="rb", anon=True).open()  # type: ignore[return-value]

    tmp = destination.with_name(f".{destination.name}.tmp")
    try:
        with opener(value) as source, tmp.open("wb") as target:
            shutil.copyfileobj(source, target)
        tmp.replace(destination)
    finally:
        tmp.unlink(missing_ok=True)
    return destination


def load_regular_source_grid_from_netcdf(path: str | Path) -> RegularSourceGrid:
    """Load a GOES ABI scene as a regular source grid for trusted extraction."""

    with xr.open_dataset(path) as ds:
        if "x" not in ds.coords or "y" not in ds.coords:
            raise ValueError("GOES ABI NetCDF scene must contain x and y coordinates")
        crs, scale_scan_angles = _source_crs(ds)
        x = np.asarray(ds.coords["x"].values, dtype=float)
        y = np.asarray(ds.coords["y"].values, dtype=float)
        if scale_scan_angles:
            projection = ds["goes_imager_projection"]
            height = float(projection.attrs["perspective_point_height"])
            x = x * height
            y = y * height
        variables: dict[str, np.ndarray] = {}
        for var_name in ABI_VARS:
            if var_name not in ds:
                raise ValueError(f"GOES ABI NetCDF scene is missing variable {var_name}")
            values = np.asarray(ds[var_name].values, dtype=np.float32)
            if values.ndim != 2:
                raise ValueError(f"GOES ABI variable {var_name} must be two-dimensional")
            if values.shape != (len(y), len(x)):
                raise ValueError(
                    f"GOES ABI variable {var_name} shape {values.shape} does not match y/x lengths {(len(y), len(x))}"
                )
            variables[var_name] = values
    return RegularSourceGrid(crs=crs, x=x, y=y, variables=variables)


def _source_crs(ds: xr.Dataset) -> tuple[CRS, bool]:
    for name in ("spatial_ref", "crs"):
        if name in ds:
            attrs = ds[name].attrs
            for attr_name in ("crs_wkt", "spatial_ref"):
                value = attrs.get(attr_name)
                if value:
                    return CRS.from_wkt(str(value)), False
            epsg = attrs.get("epsg")
            if epsg is not None:
                return CRS.from_epsg(int(epsg)), False
    if "goes_imager_projection" not in ds:
        raise ValueError("GOES ABI NetCDF scene is missing CRS metadata")
    attrs = dict(ds["goes_imager_projection"].attrs)
    try:
        cf = {
            "grid_mapping_name": attrs["grid_mapping_name"],
            "perspective_point_height": float(attrs["perspective_point_height"]),
            "semi_major_axis": float(attrs["semi_major_axis"]),
            "semi_minor_axis": float(attrs["semi_minor_axis"]),
            "longitude_of_projection_origin": float(attrs["longitude_of_projection_origin"]),
            "sweep_angle_axis": str(attrs.get("sweep_angle_axis", "x")),
        }
    except KeyError as exc:
        raise ValueError(f"GOES ABI projection metadata is missing {exc.args[0]!r}") from exc
    return CRS.from_cf(cf), True


__all__ = ["load_regular_source_grid_from_netcdf", "materialize_goes_scene"]
