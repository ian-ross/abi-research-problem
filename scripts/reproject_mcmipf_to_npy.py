#!/usr/bin/env python
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import numpy as np
import xarray as xr
from pyorbital.astronomy import sun_zenith_angle
from pyproj import CRS, Transformer

# Allow running from the repository checkout without installing the package.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from goes_reprojection.grid import nice_mit_grid


LOOKUPS_ENV = "GOES_REPROJECTION_LOOKUPS_DIR"
FALLBACK_LOOKUPS_ENV = "LOOKUPS_DIR"
ABI_VARS = [f"CMI_C{i:02d}" for i in range(1, 17)]


def lookup_prefix_for_lon0(lon0: float) -> str:
    """Return lookup filename prefix for the ABI projection longitude."""
    if abs(lon0 - (-89.5)) < 0.05:
        return "lon0_m89p5_scene0"
    if abs(lon0 - (-75.0)) < 0.05:
        return "lon0_m75p0_scene70"
    raise ValueError(
        f"Unsupported GOES projection longitude lon_0={lon0}. "
        "Known empirical lookups are for -89.5 and -75.0 degrees."
    )


def lookups_dir_from_env() -> Path:
    value = os.environ.get(LOOKUPS_ENV) or os.environ.get(FALLBACK_LOOKUPS_ENV)
    if not value:
        raise RuntimeError(
            f"Set {LOOKUPS_ENV} to the directory containing lookup *_row.npy and *_col.npy files "
            f"(or set fallback {FALLBACK_LOOKUPS_ENV})."
        )
    path = Path(value)
    if not path.is_dir():
        raise RuntimeError(f"Lookup directory does not exist or is not a directory: {path}")
    return path


def load_lookup(lookups_dir: Path, lon0: float) -> tuple[np.ndarray, np.ndarray, Path]:
    prefix = lookup_prefix_for_lon0(lon0)
    row_path = lookups_dir / f"{prefix}_row.npy"
    col_path = lookups_dir / f"{prefix}_col.npy"
    if not row_path.exists() or not col_path.exists():
        raise FileNotFoundError(f"Missing lookup files: {row_path} / {col_path}")
    row = np.load(row_path)
    col = np.load(col_path)
    if row.shape != (2000, 3000) or col.shape != (2000, 3000):
        raise ValueError(f"Lookup arrays must have shape (2000, 3000); got {row.shape} and {col.shape}")
    if np.any(row < 0) or np.any(col < 0):
        raise ValueError("Lookup contains unresolved negative source indices")
    return row.astype(np.intp, copy=False), col.astype(np.intp, copy=False), row_path.with_name(prefix)


def observation_time(ds: xr.Dataset, mode: str):
    """Observation time for solar zenith angle.

    The MIT metadata records scenes at minute precision. Using the floored start
    minute reproduces the stored SZA channel to within a few hundredths of a
    degree for validation scenes. Use --sza-time start if exact NetCDF image
    start time is preferred for new frames.
    """
    import pandas as pd

    start = pd.to_datetime(ds.attrs["time_coverage_start"])
    if mode == "minute":
        return start.floor("min").to_pydatetime()
    if mode == "start":
        return start.to_pydatetime()
    if mode == "midpoint":
        end = pd.to_datetime(ds.attrs["time_coverage_end"])
        return (start + (end - start) / 2).to_pydatetime()
    raise ValueError(f"unknown SZA time mode: {mode}")


def write_lon_lat_sza(out: np.ndarray, ds: xr.Dataset, block_rows: int, sza_time_mode: str) -> None:
    grid = nice_mit_grid()
    transformer = Transformer.from_crs(CRS.from_proj4(grid.crs_proj4), "EPSG:4326", always_xy=True)
    obs_time = observation_time(ds, sza_time_mode)

    cols = np.arange(grid.width)[None, :]
    for r0 in range(0, grid.height, block_rows):
        r1 = min(grid.height, r0 + block_rows)
        rows = np.arange(r0, r1)[:, None]
        x = grid.x(rows, cols)
        y = grid.y(rows, cols)
        lon, lat = transformer.transform(x, y)
        lon = lon.astype(np.float32)
        lat = lat.astype(np.float32)
        out[r0:r1, :, 16] = lon
        out[r0:r1, :, 17] = lat
        out[r0:r1, :, 18] = sun_zenith_angle(obs_time, lon, lat).astype(np.float32)


def reproject(input_nc: Path, output_npy: Path, block_rows: int, sza_time_mode: str) -> None:
    lookups_dir = lookups_dir_from_env()
    ds = xr.open_dataset(input_nc)
    lon0 = float(ds["goes_imager_projection"].attrs["longitude_of_projection_origin"])
    lookup_row, lookup_col, lookup_prefix = load_lookup(lookups_dir, lon0)

    print(f"Input: {input_nc}")
    print(f"Detected GOES lon_0={lon0}; using lookup {lookup_prefix}")
    print(f"Output: {output_npy}")

    out = np.lib.format.open_memmap(output_npy, mode="w+", dtype=np.float32, shape=(2000, 3000, 19))

    # ABI channels 1-16 -> output indexes 0-15.
    for ch, var in enumerate(ABI_VARS):
        print(f"Writing channel {ch}: {var}")
        src = np.asarray(ds[var].values, dtype=np.float32)
        for r0 in range(0, 2000, block_rows):
            r1 = min(2000, r0 + block_rows)
            out[r0:r1, :, ch] = src[lookup_row[r0:r1, :], lookup_col[r0:r1, :]]
        out.flush()

    print("Writing longitude, latitude, solar zenith angle")
    write_lon_lat_sza(out, ds, block_rows, sza_time_mode)
    out.flush()
    ds.close()
    print("Done")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Reproject one GOES ABI L2 MCMIPF NetCDF file to a (2000, 3000, 19) float32 .npy "
            "array matching the MIT zarr channel order. The lookup directory is read from "
            f"${LOOKUPS_ENV}."
        )
    )
    parser.add_argument("input_nc", type=Path, help="Input OR_ABI-L2-MCMIPF NetCDF file")
    parser.add_argument("output_npy", type=Path, help="Output .npy filename")
    parser.add_argument("--block-rows", type=int, default=128, help="Rows to process at once")
    parser.add_argument(
        "--sza-time",
        choices=["minute", "start", "midpoint"],
        default="minute",
        help="Observation time to use for solar zenith angle; default matches MIT minute-precision metadata best",
    )
    args = parser.parse_args()
    reproject(args.input_nc, args.output_npy, args.block_rows, args.sza_time)


if __name__ == "__main__":
    main()
