"""Provider-owned deterministic Artifact Filters for ABI contrail predictions.

Artifact Filters are trusted ABI research-problem behavior. They are applied by
provider/harness evaluation code to candidate and baseline predictions, not by
candidate model code.
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

NATURAL_EARTH_URL = "https://github.com/nvkelso/natural-earth-vector/blob/master/geojson/"
NATURAL_EARTH_COASTLINE_URL = NATURAL_EARTH_URL + "ne_10m_coastline.geojson"
NATURAL_EARTH_RIVERS_NORTH_AMERICA_URL = NATURAL_EARTH_URL + "ne_10m_rivers_north_america.geojson"


@dataclass(frozen=True)
class ArtifactFilterResult:
    """Prediction after Artifact Filters plus removed-pixel diagnostics."""

    filtered_mask: np.ndarray
    filtered_probabilities: np.ndarray
    removed_mask: np.ndarray
    diagnostics: dict[str, object]


class ArtifactFilter:
    """Deterministic provider-owned filter interface."""

    name = "artifact_filter"

    def apply(self, mask: np.ndarray, probabilities: np.ndarray, *, context: Mapping[str, object] | None = None) -> ArtifactFilterResult:
        raise NotImplementedError


@dataclass(frozen=True)
class GeographicFeatureFilter(ArtifactFilter):
    """Remove predictions overlapping trusted coastline/large-river features.

    The v0 approved vector sources are Natural Earth 1:10m coastlines and North
    America rivers. For lightweight fixture tests and preprocessed production
    deployments, callers may provide a pre-rasterized boolean
    ``geographic_feature_mask`` in the filter context. If GeoJSON paths and
    provider-owned longitude/latitude grids are available, the filter rasterizes
    LineString/MultiLineString features to the prediction grid using nearest grid
    points and a configurable pixel buffer.
    """

    coastline_geojson: Path | None = None
    rivers_geojson: Path | None = None
    pixel_buffer: int = 1
    name: str = "geographic_feature_filter"
    ancillary_sources: tuple[dict[str, str], ...] = field(
        default_factory=lambda: (
            {"name": "natural_earth_10m_coastline", "url": NATURAL_EARTH_COASTLINE_URL},
            {"name": "natural_earth_10m_rivers_north_america", "url": NATURAL_EARTH_RIVERS_NORTH_AMERICA_URL},
        )
    )

    def apply(self, mask: np.ndarray, probabilities: np.ndarray, *, context: Mapping[str, object] | None = None) -> ArtifactFilterResult:
        pred = _as_bool_2d(mask)
        probs = _as_float_2d(probabilities)
        ctx = context or {}
        feature_mask = self._feature_mask_for_prediction(pred.shape, ctx)
        removed = np.logical_and(pred, feature_mask)
        filtered = np.logical_and(pred, ~removed)
        filtered_probabilities = probs.copy()
        filtered_probabilities[removed] = 0.0
        return _result_from_arrays(
            filtered,
            filtered_probabilities,
            removed,
            {
                "filter": self.name,
                "removed_pixel_count": int(removed.sum()),
                "feature_pixel_count": int(feature_mask.sum()),
                "available": bool(feature_mask.any()),
                "ancillary_sources": list(self.ancillary_sources),
            },
        )

    def _feature_mask_for_prediction(self, shape: tuple[int, int], context: Mapping[str, object]) -> np.ndarray:
        raster = context.get("geographic_feature_mask")
        if raster is not None:
            feature_mask = _as_bool_2d(raster)
            if feature_mask.shape != shape:
                raise ValueError(f"geographic_feature_mask shape {feature_mask.shape} does not match prediction shape {shape}")
            return feature_mask

        lon = context.get("longitude")
        lat = context.get("latitude")
        if lon is None or lat is None:
            return np.zeros(shape, dtype=bool)
        lon_grid = np.asarray(lon, dtype=np.float64)
        lat_grid = np.asarray(lat, dtype=np.float64)
        if lon_grid.shape != shape or lat_grid.shape != shape:
            raise ValueError("longitude/latitude grids must match prediction shape")

        paths = tuple(path for path in (self.coastline_geojson, self.rivers_geojson) if path is not None)
        if not paths:
            return np.zeros(shape, dtype=bool)
        mask = np.zeros(shape, dtype=bool)
        bbox = (float(np.nanmin(lon_grid)), float(np.nanmin(lat_grid)), float(np.nanmax(lon_grid)), float(np.nanmax(lat_grid)))
        for path in paths:
            for line in _iter_geojson_lines(path, bbox=bbox):
                _burn_line_nearest(mask, line, lon_grid=lon_grid, lat_grid=lat_grid)
        return _dilate_bool(mask, self.pixel_buffer)


@dataclass(frozen=True)
class ScanlineArtifactFilter(ArtifactFilter):
    """Remove long, approximately constant ABI-y positive structures."""

    min_length_pixels: int = 128
    max_probability_std: float = 0.03
    name: str = "scanline_artifact_filter"

    def apply(self, mask: np.ndarray, probabilities: np.ndarray, *, context: Mapping[str, object] | None = None) -> ArtifactFilterResult:
        del context
        pred = _as_bool_2d(mask)
        probs = _as_float_2d(probabilities)
        removed = np.zeros_like(pred, dtype=bool)
        for row in range(pred.shape[0]):
            for start, end in _true_runs(pred[row]):
                if end - start < self.min_length_pixels:
                    continue
                run_probs = probs[row, start:end]
                if float(np.std(run_probs)) <= self.max_probability_std:
                    removed[row, start:end] = True
        filtered = np.logical_and(pred, ~removed)
        filtered_probabilities = probs.copy()
        filtered_probabilities[removed] = 0.0
        return _result_from_arrays(
            filtered,
            filtered_probabilities,
            removed,
            {
                "filter": self.name,
                "removed_pixel_count": int(removed.sum()),
                "min_length_pixels": int(self.min_length_pixels),
                "max_probability_std": float(self.max_probability_std),
            },
        )


@dataclass(frozen=True)
class ABIArtifactFilterPipeline:
    """Ordered provider-owned Artifact Filter composition."""

    filters: tuple[ArtifactFilter, ...] = field(default_factory=lambda: (GeographicFeatureFilter(), ScanlineArtifactFilter()))
    pixel_area_km2: float = 4.0

    def apply(self, mask: Any, probabilities: Any, *, context: Mapping[str, object] | None = None) -> ArtifactFilterResult:
        current_mask = _as_bool_2d(mask)
        current_probabilities = _as_float_2d(probabilities)
        total_removed = np.zeros_like(current_mask, dtype=bool)
        filter_diagnostics: list[dict[str, object]] = []
        for artifact_filter in self.filters:
            result = artifact_filter.apply(current_mask, current_probabilities, context=context)
            removed = _as_bool_2d(result.removed_mask)
            total_removed |= removed
            current_mask = _as_bool_2d(result.filtered_mask)
            current_probabilities = _as_float_2d(result.filtered_probabilities)
            filter_diagnostics.append(result.diagnostics)
        removed_count = int(total_removed.sum())
        diagnostics = {
            "removed_pixel_count": removed_count,
            "removed_area_km2": float(removed_count * self.pixel_area_km2),
            "pixel_area_km2": float(self.pixel_area_km2),
            "filters": filter_diagnostics,
        }
        return _result_from_arrays(current_mask, current_probabilities, total_removed, diagnostics)


def build_default_artifact_filter_pipeline(data_config: Mapping[str, object] | None = None) -> ABIArtifactFilterPipeline:
    """Build the v0 provider-owned filter pipeline from trusted data config."""

    config = data_config or {}
    coastline = _optional_path(config.get("coastline_geojson"))
    rivers = _optional_path(config.get("rivers_geojson"))
    pixel_buffer = int(config.get("geographic_filter_pixel_buffer", 1))
    scanline_min = int(config.get("scanline_min_length_pixels", 128))
    scanline_std = float(config.get("scanline_max_probability_std", 0.03))
    pixel_area = float(config.get("pixel_area_km2", 4.0))
    return ABIArtifactFilterPipeline(
        filters=(
            GeographicFeatureFilter(coastline_geojson=coastline, rivers_geojson=rivers, pixel_buffer=pixel_buffer),
            ScanlineArtifactFilter(min_length_pixels=scanline_min, max_probability_std=scanline_std),
        ),
        pixel_area_km2=pixel_area,
    )


def _optional_path(value: object) -> Path | None:
    if value is None or value == "":
        return None
    return Path(str(value)).expanduser().resolve()


def _result_from_arrays(filtered: np.ndarray, probabilities: np.ndarray, removed: np.ndarray, diagnostics: dict[str, object]) -> ArtifactFilterResult:
    return ArtifactFilterResult(
        filtered_mask=filtered[np.newaxis, :, :],
        filtered_probabilities=probabilities[np.newaxis, :, :],
        removed_mask=removed[np.newaxis, :, :],
        diagnostics=diagnostics,
    )


def _as_bool_2d(value: Any) -> np.ndarray:
    array = np.asarray(value)
    if array.ndim == 3 and array.shape[0] == 1:
        array = array[0]
    if array.ndim != 2:
        raise ValueError(f"expected [H,W] or [1,H,W] mask, got shape {array.shape}")
    return array.astype(bool, copy=False)


def _as_float_2d(value: Any) -> np.ndarray:
    array = np.asarray(value, dtype=np.float32)
    if array.ndim == 3 and array.shape[0] == 1:
        array = array[0]
    if array.ndim != 2:
        raise ValueError(f"expected [H,W] or [1,H,W] probabilities, got shape {array.shape}")
    return array


def _true_runs(row: np.ndarray) -> Iterable[tuple[int, int]]:
    start: int | None = None
    for idx, value in enumerate(row):
        if bool(value) and start is None:
            start = idx
        elif not bool(value) and start is not None:
            yield start, idx
            start = None
    if start is not None:
        yield start, len(row)


def _dilate_bool(mask: np.ndarray, pixels: int) -> np.ndarray:
    radius = max(0, int(pixels))
    if radius == 0 or not mask.any():
        return mask
    padded = np.pad(mask, radius, mode="constant", constant_values=False)
    out = np.zeros_like(mask, dtype=bool)
    for dy in range(2 * radius + 1):
        for dx in range(2 * radius + 1):
            out |= padded[dy : dy + mask.shape[0], dx : dx + mask.shape[1]]
    return out


def _iter_geojson_lines(path: Path, *, bbox: tuple[float, float, float, float]) -> Iterable[list[tuple[float, float]]]:
    payload = json.loads(path.read_text())
    features = payload.get("features", []) if isinstance(payload, dict) else []
    for feature in features:
        if not isinstance(feature, dict):
            continue
        geometry = feature.get("geometry")
        if not isinstance(geometry, dict):
            continue
        geom_type = geometry.get("type")
        coordinates = geometry.get("coordinates")
        for line in _geometry_lines(geom_type, coordinates):
            if _line_intersects_bbox(line, bbox):
                yield line


def _geometry_lines(geom_type: object, coordinates: object) -> Iterable[list[tuple[float, float]]]:
    if geom_type == "LineString" and isinstance(coordinates, Sequence):
        line = _coordinate_line(coordinates)
        if line:
            yield line
    elif geom_type == "MultiLineString" and isinstance(coordinates, Sequence):
        for part in coordinates:
            if isinstance(part, Sequence):
                line = _coordinate_line(part)
                if line:
                    yield line


def _coordinate_line(points: Sequence[object]) -> list[tuple[float, float]]:
    line: list[tuple[float, float]] = []
    for point in points:
        if isinstance(point, Sequence) and len(point) >= 2:
            line.append((float(point[0]), float(point[1])))
    return line


def _line_intersects_bbox(line: Sequence[tuple[float, float]], bbox: tuple[float, float, float, float]) -> bool:
    min_lon, min_lat, max_lon, max_lat = bbox
    return any(min_lon <= lon <= max_lon and min_lat <= lat <= max_lat for lon, lat in line)


def _burn_line_nearest(mask: np.ndarray, line: Sequence[tuple[float, float]], *, lon_grid: np.ndarray, lat_grid: np.ndarray) -> None:
    for lon, lat in line:
        distance = (lon_grid - lon) ** 2 + (lat_grid - lat) ** 2
        flat_index = int(np.nanargmin(distance))
        row, col = np.unravel_index(flat_index, mask.shape)
        mask[row, col] = True


__all__ = [
    "ABIArtifactFilterPipeline",
    "ArtifactFilter",
    "ArtifactFilterResult",
    "GeographicFeatureFilter",
    "NATURAL_EARTH_COASTLINE_URL",
    "NATURAL_EARTH_RIVERS_NORTH_AMERICA_URL",
    "ScanlineArtifactFilter",
    "build_default_artifact_filter_pipeline",
]
