"""Trusted center-grid definitions for ABI temporal patch extraction."""

from __future__ import annotations

import json
from collections.abc import Mapping
from datetime import UTC, datetime
from dataclasses import dataclass
from typing import Any

import numpy as np
from pyproj import CRS, Transformer

from abi_contrail.datasets import ABIPatchIndexRecord

MIT_CRS_PROJ4 = "+proj=ortho +ellps=GRS80 +lat_0=39.8283 +lon_0=-98.5795 +no_defs"
MIT_FULL_SCENE_HEIGHT = 2000
MIT_FULL_SCENE_WIDTH = 3000
MIT_X0 = -2440354.0
MIT_DX_COL = 2000.0
MIT_Y0 = 1320437.0
MIT_DY_ROW = -2000.0
ABI_PATCH_SIZE = 256
ABI_VARS = tuple(f"CMI_C{i:02d}" for i in range(1, 17))


@dataclass(frozen=True)
class RegularSourceGrid:
    """Regular source grid for trusted reprojection/extraction tests and wrappers."""

    crs: CRS
    x: np.ndarray
    y: np.ndarray
    variables: Mapping[str, np.ndarray]


@dataclass(frozen=True)
class TemporalPatchGrid:
    """Pixel-center affine grid for one 256x256 temporal extraction target."""

    crs: CRS
    height: int
    width: int
    x0: float
    dx_col: float
    dx_row: float
    y0: float
    dy_col: float
    dy_row: float

    def x(self, rows: Any, cols: Any) -> Any:
        return self.x0 + self.dx_col * cols + self.dx_row * rows

    def y(self, rows: Any, cols: Any) -> Any:
        return self.y0 + self.dy_col * cols + self.dy_row * rows

    @property
    def area_extent_edges(self) -> list[float]:
        rows = np.array([0, 0, self.height - 1, self.height - 1], dtype=float)
        cols = np.array([0, self.width - 1, 0, self.width - 1], dtype=float)
        xs = np.asarray(self.x(rows, cols), dtype=float)
        ys = np.asarray(self.y(rows, cols), dtype=float)
        half_x = max(abs(self.dx_col), abs(self.dx_row)) / 2
        half_y = max(abs(self.dy_col), abs(self.dy_row)) / 2
        return [float(xs.min() - half_x), float(ys.min() - half_y), float(xs.max() + half_x), float(ys.max() + half_y)]


def mit_temporal_patch_grid(record: ABIPatchIndexRecord) -> TemporalPatchGrid:
    """Return the fixed MIT grid window for a center ABI Patch record."""

    if record.dataset_source != "mit":
        raise ValueError("MIT temporal patch grid requires a MIT ABI Patch record")
    if record.row < 0 or record.col < 0 or record.row + ABI_PATCH_SIZE > MIT_FULL_SCENE_HEIGHT or record.col + ABI_PATCH_SIZE > MIT_FULL_SCENE_WIDTH:
        raise ValueError("MIT ABI Patch record window falls outside the fixed MIT full-scene grid")
    return TemporalPatchGrid(
        crs=CRS.from_proj4(MIT_CRS_PROJ4),
        height=ABI_PATCH_SIZE,
        width=ABI_PATCH_SIZE,
        x0=MIT_X0 + MIT_DX_COL * record.col,
        dx_col=MIT_DX_COL,
        dx_row=0.0,
        y0=MIT_Y0 + MIT_DY_ROW * record.row,
        dy_col=0.0,
        dy_row=MIT_DY_ROW,
    )


def google_temporal_patch_grid(location: str | Mapping[str, object]) -> TemporalPatchGrid:
    """Return the patch-specific Google grid from trusted ``location`` metadata."""

    metadata = _location_mapping(location)
    try:
        crs = CRS.from_wkt(str(metadata["projection_wkt"]))
        col_min = float(metadata["col_min"])
        row_min = float(metadata["row_min"])
        col_size = float(metadata["col_size"])
        row_size = float(metadata["row_size"])
    except KeyError as exc:
        raise ValueError(f"Google location metadata is missing required field {exc.args[0]!r}") from exc
    if col_size == 0.0 or row_size == 0.0:
        raise ValueError("Google location col_size and row_size must be non-zero")
    return TemporalPatchGrid(
        crs=crs,
        height=ABI_PATCH_SIZE,
        width=ABI_PATCH_SIZE,
        x0=col_min,
        dx_col=col_size,
        dx_row=0.0,
        y0=row_min,
        dy_col=0.0,
        dy_row=row_size,
    )


def validate_google_center_grid_against_materialized_patch(
    raw_center_inputs: np.ndarray,
    location: str | Mapping[str, object],
    *,
    sample_step: int = 32,
    tolerance_degrees: float = 0.02,
) -> dict[str, object]:
    """Validate Google ``location`` grid metadata against trusted lon/lat channels.

    This is a provider-owned precondition before non-zero temporal extraction for
    Google patches. Longitude/latitude are read only from materialized source
    channels 16/17 and are never candidate inputs.
    """

    source = np.asarray(raw_center_inputs)
    if source.ndim != 3 or source.shape[0] < ABI_PATCH_SIZE or source.shape[1] < ABI_PATCH_SIZE or source.shape[2] <= 17:
        raise ValueError("Google center validation requires raw [H,W,19] materialized ABI inputs")
    if sample_step < 1:
        raise ValueError("sample_step must be positive")
    grid = google_temporal_patch_grid(location)
    rows = np.arange(0, ABI_PATCH_SIZE, sample_step)
    cols = np.arange(0, ABI_PATCH_SIZE, sample_step)
    row_grid, col_grid = np.meshgrid(rows, cols, indexing="ij")
    transformer = Transformer.from_crs(grid.crs, "EPSG:4326", always_xy=True)
    expected_lon, expected_lat = transformer.transform(grid.x(row_grid, col_grid), grid.y(row_grid, col_grid))
    actual_lon = source[row_grid, col_grid, 16].astype(float)
    actual_lat = source[row_grid, col_grid, 17].astype(float)
    lon_error = np.abs(actual_lon - expected_lon)
    lat_error = np.abs(actual_lat - expected_lat)
    finite = np.isfinite(actual_lon) & np.isfinite(actual_lat) & np.isfinite(expected_lon) & np.isfinite(expected_lat)
    max_lon = float(np.max(lon_error[finite])) if np.any(finite) else float("inf")
    max_lat = float(np.max(lat_error[finite])) if np.any(finite) else float("inf")
    valid = bool(np.any(finite) and max(max_lon, max_lat) <= tolerance_degrees)
    report = {
        "valid": valid,
        "sample_count": int(np.size(row_grid)),
        "finite_sample_count": int(np.sum(finite)),
        "max_abs_lon_error": max_lon,
        "max_abs_lat_error": max_lat,
        "tolerance_degrees": float(tolerance_degrees),
    }
    if not valid:
        raise ValueError(f"Google location grid validation failed: {report}")
    return report


def extract_regular_source_patch(
    source: RegularSourceGrid,
    target_grid: TemporalPatchGrid,
    *,
    observation_time: object,
    solar_zenith_angle_function: object | None = None,
) -> np.ndarray:
    """Extract a trusted nearest-neighbor 19-channel ABI patch on ``target_grid``.

    The source grid must fully cover every target pixel center. The function
    raises instead of padding, masking, or clipping partial coverage.
    """

    x_coords = np.asarray(source.x, dtype=float)
    y_coords = np.asarray(source.y, dtype=float)
    if x_coords.ndim != 1 or y_coords.ndim != 1 or len(x_coords) < 2 or len(y_coords) < 2:
        raise ValueError("source x/y coordinates must be one-dimensional arrays with at least two values")
    rows, cols = np.indices((target_grid.height, target_grid.width))
    source_transformer = Transformer.from_crs(target_grid.crs, source.crs, always_xy=True)
    target_x, target_y = source_transformer.transform(target_grid.x(rows, cols), target_grid.y(rows, cols))
    source_rows, source_cols = _nearest_regular_source_indices(target_x, target_y, x_coords=x_coords, y_coords=y_coords)
    if (
        not np.all(np.isfinite(target_x))
        or not np.all(np.isfinite(target_y))
        or np.any(source_rows < 0)
        or np.any(source_rows >= len(y_coords))
        or np.any(source_cols < 0)
        or np.any(source_cols >= len(x_coords))
    ):
        raise ValueError("GOES-16 CONUS source scene does not fully cover requested temporal ABI Patch footprint")
    out = np.empty((target_grid.height, target_grid.width, 19), dtype=np.float32)
    for channel_index, var_name in enumerate(ABI_VARS):
        try:
            values = np.asarray(source.variables[var_name], dtype=np.float32)
        except KeyError as exc:
            raise ValueError(f"source scene is missing ABI variable {var_name}") from exc
        if values.shape != (len(y_coords), len(x_coords)):
            raise ValueError(f"source variable {var_name} shape {values.shape} does not match source grid")
        out[:, :, channel_index] = values[source_rows, source_cols]
    lonlat_transformer = Transformer.from_crs(target_grid.crs, "EPSG:4326", always_xy=True)
    lon, lat = lonlat_transformer.transform(target_grid.x(rows, cols), target_grid.y(rows, cols))
    out[:, :, 16] = np.asarray(lon, dtype=np.float32)
    out[:, :, 17] = np.asarray(lat, dtype=np.float32)
    sza_function = solar_zenith_angle_function or _default_solar_zenith_angle_function
    out[:, :, 18] = np.asarray(sza_function(_normalise_observation_time_for_sza(observation_time), lon, lat), dtype=np.float32)
    return out


def _nearest_regular_source_indices(
    target_x: np.ndarray,
    target_y: np.ndarray,
    *,
    x_coords: np.ndarray,
    y_coords: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    dx = float(x_coords[1] - x_coords[0])
    dy = float(y_coords[1] - y_coords[0])
    if dx == 0.0 or dy == 0.0:
        raise ValueError("source x/y coordinates must have non-zero spacing")
    cols = np.rint((target_x - x_coords[0]) / dx).astype(int)
    rows = np.rint((target_y - y_coords[0]) / dy).astype(int)
    return rows, cols


def _default_solar_zenith_angle_function(observation_time: object, lon: np.ndarray, lat: np.ndarray) -> np.ndarray:
    from pyorbital.astronomy import sun_zenith_angle

    return sun_zenith_angle(observation_time, lon, lat)


def _normalise_observation_time_for_sza(observation_time: object) -> object:
    """Return timezone-naive UTC datetimes for pyorbital SZA calculation.

    ``pyorbital`` converts datetimes through ``np.datetime64``, which cannot
    represent timezone metadata and emits a warning for timezone-aware values.
    Temporal provisioning supplies UTC scene times, so stripping the timezone
    after conversion to UTC preserves the instant while avoiding warning spam.
    """

    if isinstance(observation_time, datetime) and observation_time.tzinfo is not None:
        return observation_time.astimezone(UTC).replace(tzinfo=None)
    return observation_time


def _location_mapping(location: str | Mapping[str, object]) -> Mapping[str, object]:
    if isinstance(location, Mapping):
        return location
    if not isinstance(location, str) or not location.strip():
        raise ValueError("Google location metadata must be a mapping or JSON object string")
    loaded = json.loads(location)
    if not isinstance(loaded, Mapping):
        raise ValueError("Google location metadata JSON must decode to an object")
    return loaded


__all__ = [
    "ABI_PATCH_SIZE",
    "ABI_VARS",
    "MIT_CRS_PROJ4",
    "RegularSourceGrid",
    "TemporalPatchGrid",
    "extract_regular_source_patch",
    "google_temporal_patch_grid",
    "mit_temporal_patch_grid",
    "validate_google_center_grid_against_materialized_patch",
]
