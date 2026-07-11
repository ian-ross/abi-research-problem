from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import xarray as xr
import zarr
from pyproj import CRS, Transformer

from .grid import AffineGrid


ABI_VARS = [f"CMI_C{i:02d}" for i in range(1, 17)]


@dataclass(frozen=True)
class SourceGeometry:
    geos_crs: CRS
    x_m: np.ndarray
    y_m: np.ndarray


def open_inputs(path: str | Path):
    return zarr.open_array(str(path), mode="r")


def open_abi(path: str | Path) -> xr.Dataset:
    return xr.open_dataset(path)


def source_geometry(ds: xr.Dataset) -> SourceGeometry:
    attrs = ds["goes_imager_projection"].attrs
    h = float(attrs["perspective_point_height"])
    return SourceGeometry(
        geos_crs=CRS.from_cf(attrs),
        x_m=ds["x"].values.astype(float) * h,
        y_m=ds["y"].values.astype(float) * h,
    )


def target_to_fractional_source_indices(grid: AffineGrid, geom: SourceGeometry, rows: np.ndarray, cols: np.ndarray):
    target_crs = CRS.from_proj4(grid.crs_proj4)
    transformer = Transformer.from_crs(target_crs, geom.geos_crs, always_xy=True)
    target_x = grid.x(rows, cols)
    target_y = grid.y(rows, cols)
    source_x, source_y = transformer.transform(target_x, target_y)
    frac_cols = (source_x - geom.x_m[0]) / (geom.x_m[1] - geom.x_m[0])
    frac_rows = (source_y - geom.y_m[0]) / (geom.y_m[1] - geom.y_m[0])
    return frac_rows, frac_cols


def predicted_nearest_indices(grid: AffineGrid, geom: SourceGeometry, rows: np.ndarray, cols: np.ndarray):
    frac_rows, frac_cols = target_to_fractional_source_indices(grid, geom, rows, cols)
    return np.rint(frac_rows).astype(int), np.rint(frac_cols).astype(int), frac_rows, frac_cols


def _target_vector(inputs, scene: int, row: int, col: int, channels: list[int]) -> np.ndarray:
    return np.asarray(inputs[scene, row, col, channels], dtype=np.float32)


def _source_vector(ds: xr.Dataset, row: int, col: int, abi_vars: list[str]) -> np.ndarray:
    return np.asarray([ds[v].isel(y=row, x=col).values.item() for v in abi_vars], dtype=np.float32)


def vectors_equal(a: np.ndarray, b: np.ndarray) -> bool:
    return bool(np.all((a == b) | (np.isnan(a) & np.isnan(b))))


def find_matching_source_pixel(
    ds: xr.Dataset,
    inputs,
    scene: int,
    target_row: int,
    target_col: int,
    predicted_source_row: int,
    predicted_source_col: int,
    radius: int = 5,
    channels: list[int] | None = None,
    abi_vars: list[str] | None = None,
) -> list[tuple[int, int]]:
    """Find source pixels whose selected ABI vector exactly equals one target pixel."""
    if channels is None:
        channels = list(range(16))
    if abi_vars is None:
        abi_vars = [ABI_VARS[i] for i in channels]

    target = _target_vector(inputs, scene, target_row, target_col, channels)
    matches: list[tuple[int, int]] = []
    ny = ds.sizes["y"]
    nx = ds.sizes["x"]
    for sr in range(max(0, predicted_source_row - radius), min(ny, predicted_source_row + radius + 1)):
        for sc in range(max(0, predicted_source_col - radius), min(nx, predicted_source_col + radius + 1)):
            source = _source_vector(ds, sr, sc, abi_vars)
            if vectors_equal(source, target):
                matches.append((sr, sc))
    return matches


def random_pixels(height: int, width: int, n: int, seed: int = 0) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    return rng.integers(0, height, n), rng.integers(0, width, n)


def inspect_source_matches(
    abi_path: str | Path,
    inputs_path: str | Path,
    grid: AffineGrid,
    scene: int = 0,
    sample_size: int = 200,
    seed: int = 0,
    radius: int = 5,
    channels: list[int] | None = None,
) -> dict:
    """Compare target ABI vectors against nearby source pixels.

    Returns a JSON-serialisable diagnostic report.
    """
    inputs = open_inputs(inputs_path)
    ds = open_abi(abi_path)
    geom = source_geometry(ds)
    rows, cols = random_pixels(grid.height, grid.width, sample_size, seed)
    pred_rows, pred_cols, frac_rows, frac_cols = predicted_nearest_indices(grid, geom, rows, cols)

    offset_counts: Counter[tuple[int, int]] = Counter()
    floor_offset_counts: Counter[tuple[int, int]] = Counter()
    nearest_exact = 0
    unique = 0
    missing = 0
    multiple = 0
    examples = []

    for row, col, pr, pc, fr, fc in zip(rows, cols, pred_rows, pred_cols, frac_rows, frac_cols):
        row = int(row); col = int(col); pr = int(pr); pc = int(pc)
        if pr < 0 or pr >= ds.sizes["y"] or pc < 0 or pc >= ds.sizes["x"]:
            missing += 1
            continue
        matches = find_matching_source_pixel(ds, inputs, scene, row, col, pr, pc, radius=radius, channels=channels)
        if len(matches) == 0:
            missing += 1
        elif len(matches) > 1:
            multiple += 1
        else:
            unique += 1
            sr, sc = matches[0]
            offset_counts[(sr - pr, sc - pc)] += 1
            floor_offset_counts[(int(sr - np.floor(fr)), int(sc - np.floor(fc)))] += 1
            if (sr, sc) == (pr, pc):
                nearest_exact += 1
            if len(examples) < 20 and (sr, sc) != (pr, pc):
                examples.append({
                    "target_row": row,
                    "target_col": col,
                    "predicted_source_row": pr,
                    "predicted_source_col": pc,
                    "matched_source_row": int(sr),
                    "matched_source_col": int(sc),
                    "offset_from_predicted": [int(sr - pr), int(sc - pc)],
                    "frac_source_row": float(fr),
                    "frac_source_col": float(fc),
                    "frac_row_part": float(fr % 1),
                    "frac_col_part": float(fc % 1),
                })

    total = unique + missing + multiple
    return {
        "scene": scene,
        "sample_size": sample_size,
        "channels": channels if channels is not None else list(range(16)),
        "search_radius": radius,
        "unique_matches": unique,
        "missing_matches": missing,
        "multiple_matches": multiple,
        "nearest_exact_unique": nearest_exact,
        "unique_match_fraction": unique / total if total else None,
        "nearest_exact_fraction_of_unique": nearest_exact / unique if unique else None,
        "offset_from_predicted_counts": {str(k): v for k, v in offset_counts.most_common()},
        "offset_from_floor_counts": {str(k): v for k, v in floor_offset_counts.most_common()},
        "mismatch_examples": examples,
    }


def compare_predicted_values(
    abi_path: str | Path,
    inputs_path: str | Path,
    grid: AffineGrid,
    scene: int = 0,
    sample_size: int = 1000,
    seed: int = 0,
    channels: Iterable[int] = range(16),
) -> dict:
    """Evaluate simple projected nearest-neighbor values on random target pixels."""
    inputs = open_inputs(inputs_path)
    ds = open_abi(abi_path)
    geom = source_geometry(ds)
    rows, cols = random_pixels(grid.height, grid.width, sample_size, seed)
    pred_rows, pred_cols, _, _ = predicted_nearest_indices(grid, geom, rows, cols)

    per_channel = {}
    in_bounds = (pred_rows >= 0) & (pred_rows < ds.sizes["y"]) & (pred_cols >= 0) & (pred_cols < ds.sizes["x"])
    for ch in channels:
        var = ABI_VARS[ch]
        target_vals = []
        pred_vals = []
        for row, col, sr, sc, ok in zip(rows, cols, pred_rows, pred_cols, in_bounds):
            if not ok:
                continue
            target_vals.append(inputs[scene, int(row), int(col), int(ch)])
            pred_vals.append(ds[var].isel(y=int(sr), x=int(sc)).values.item())
        target = np.asarray(target_vals, dtype=np.float32)
        pred = np.asarray(pred_vals, dtype=np.float32)
        finite = np.isfinite(target) & np.isfinite(pred)
        diff = target[finite] - pred[finite]
        per_channel[ch] = {
            "var": var,
            "n": int(finite.sum()),
            "exact_fraction": float(np.mean(target[finite] == pred[finite])) if finite.any() else None,
            "rms_diff": float(np.sqrt(np.mean(diff ** 2))) if finite.any() else None,
            "max_abs_diff": float(np.max(np.abs(diff))) if finite.any() else None,
        }
    return {
        "scene": scene,
        "sample_size": sample_size,
        "in_bounds_fraction": float(np.mean(in_bounds)),
        "per_channel": per_channel,
    }
