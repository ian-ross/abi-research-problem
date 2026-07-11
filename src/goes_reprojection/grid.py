from __future__ import annotations

from dataclasses import dataclass, asdict

import numpy as np
from pyproj import CRS, Transformer


MCAST_PROJ4 = "+proj=ortho +ellps=GRS80 +lat_0=39.8283 +lon_0=-98.5795 +no_defs"


@dataclass(frozen=True)
class AffineGrid:
    """Pixel-center affine grid in projected metres."""

    crs_proj4: str
    height: int
    width: int
    x0: float
    dx_col: float
    dx_row: float
    y0: float
    dy_col: float
    dy_row: float
    rms_x_m: float | None = None
    rms_y_m: float | None = None

    def x(self, rows, cols):
        return self.x0 + self.dx_col * cols + self.dx_row * rows

    def y(self, rows, cols):
        return self.y0 + self.dy_col * cols + self.dy_row * rows

    @property
    def area_extent_edges(self) -> list[float]:
        """Return [llx, lly, urx, ury] pixel-edge extent for north-up grids.

        This assumes dx_row and dy_col are negligible, as they are for the MIT grid.
        """
        x_min_center = self.x(0, 0)
        x_max_center = self.x(0, self.width - 1)
        y_max_center = self.y(0, 0)
        y_min_center = self.y(self.height - 1, 0)
        half_dx = abs(self.dx_col) / 2
        half_dy = abs(self.dy_row) / 2
        return [
            float(x_min_center - half_dx),
            float(y_min_center - half_dy),
            float(x_max_center + half_dx),
            float(y_max_center + half_dy),
        ]

    def to_dict(self):
        d = asdict(self)
        d["area_extent_edges"] = self.area_extent_edges
        return d


def fit_grid_from_lonlat(lon: np.ndarray, lat: np.ndarray, proj4: str = MCAST_PROJ4, step: int = 20) -> AffineGrid:
    """Fit projected x/y pixel-center affine coordinates from zarr lon/lat channels."""
    height, width = lon.shape
    rows = np.arange(0, height, step)
    cols = np.arange(0, width, step)
    row_grid, col_grid = np.meshgrid(rows, cols, indexing="ij")

    crs = CRS.from_proj4(proj4)
    transformer = Transformer.from_crs("EPSG:4326", crs, always_xy=True)
    x, y = transformer.transform(lon[rows[:, None], cols[None, :]], lat[rows[:, None], cols[None, :]])
    mask = np.isfinite(x) & np.isfinite(y)
    design = np.column_stack([
        np.ones(mask.sum()),
        col_grid[mask].astype(float),
        row_grid[mask].astype(float),
    ])
    coef_x = np.linalg.lstsq(design, x[mask], rcond=None)[0]
    coef_y = np.linalg.lstsq(design, y[mask], rcond=None)[0]
    rms_x = float(np.sqrt(np.mean((design @ coef_x - x[mask]) ** 2)))
    rms_y = float(np.sqrt(np.mean((design @ coef_y - y[mask]) ** 2)))
    return AffineGrid(
        crs_proj4=proj4,
        height=height,
        width=width,
        x0=float(coef_x[0]),
        dx_col=float(coef_x[1]),
        dx_row=float(coef_x[2]),
        y0=float(coef_y[0]),
        dy_col=float(coef_y[1]),
        dy_row=float(coef_y[2]),
        rms_x_m=rms_x,
        rms_y_m=rms_y,
    )


def nice_mit_grid() -> AffineGrid:
    """Rounded grid inferred from scene-0 lon/lat channels.

    The fitted values are within float32 lon/lat quantisation noise of these
    integer-metre pixel centers.
    """
    return AffineGrid(
        crs_proj4=MCAST_PROJ4,
        height=2000,
        width=3000,
        x0=-2440354.0,
        dx_col=2000.0,
        dx_row=0.0,
        y0=1320437.0,
        dy_col=0.0,
        dy_row=-2000.0,
    )
