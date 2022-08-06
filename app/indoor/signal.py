from typing import Final
from dataclasses import dataclass

import numpy as np
from scipy import spatial
import pymap3d

from app.config import EngineeringCenterProfile
from app import utils


@dataclass
class Signal:
    profile: EngineeringCenterProfile
    lat: float
    lon: float
    alt: float
    row: int = None
    col: int = None

    def __post_init__(self):
        if self.lat is None or \
           self.lon is None or \
           self.alt is None:
            raise ValueError(f'lat: {self.lat} lon: {self.lon} alt: {self.alt}')
        self.__position()

    def __position(self):
        e, n, _ = pymap3d.geodetic2enu(self.lat, self.lon, self.alt,
                                       self.profile.lat0, self.profile.lon0, 0)
        x, y = utils.rotate_point(e, n, self.profile.bearing)
        self.col = int(np.ceil(x / self.profile.cell_size))
        self.row = int(np.ceil(y / self.profile.cell_size))

    def adjust_position(self, matrix):
        """ Returns
            row_: adjusted row index
            col_: adjusted col index
        """
        if self.row < 0 or self.col < 0:
            raise IndexError(f'row: {self.row} col: {self.col}')
        _ = matrix[self.row, self.row]
        if (self.col, self.row) in self.profile.aisle:
            return self.col, self.row
        tree = spatial.cKDTree([[self.row, self.col]])
        dists, _ = tree.query(self.profile.aisle, k=1, workers=-1)
        _row, _col = self.profile.aisle[np.argmin(dists)]
        return _row, _col


class Status:
    NO_SIGNAL: Final = 'NO SIGNAL'
    OUT_OF_BOUNDS: Final = 'OUT OF BOUNDS'
