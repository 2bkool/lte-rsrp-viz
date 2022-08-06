from dataclasses import dataclass

import numpy as np
from scipy import spatial

from app import logging_
from app.config import EngineeringCenterProfile
from . import redis


np.set_printoptions(linewidth=200)
logger = logging_.get_logger(__name__)


@dataclass
class RSRPMap:
    """ Reference Signals Received Power Matrix  """
    profile: EngineeringCenterProfile
    rescue_code: str
    floor_no: str
    __key: str = None
    matrix: np.ndarray = None

    def __post_init__(self):
        # ec: engineering center(공업센터)
        self.__key = f'indoor:rsrp:ec:{self.rescue_code}:{self.floor_no}'
        self.matrix = self.__load()

    def __load(self):
        matrix = redis.get(self.__key)
        if matrix is None:
            matrix = self.__create()
        return matrix

    def __create(self, default=-120):
        matrix = np.empty((self.profile.n_row, self.profile.n_col))
        matrix[:] = default
        matrix[1: -1, 1: -1] = np.nan
        redis.set(self.__key, matrix)
        logger.debug(f'RSRP {matrix.shape} Matrix created!')
        return matrix

    def update(self, row, col, power):
        if power is None:
            return False
        if np.isnan(self.matrix[row, col]):
            pass
        if power <= self.matrix[row, col]:
            return False

        self.matrix[row, col] = float(power)
        redis.set(self.__key, self.matrix)
        return True

    def interpolate(self, p=2.5):
        """ IDW Interpolation """
        n, m = self.matrix.shape
        src = np.argwhere(~np.isnan(self.matrix))
        temp = np.empty((n, m))
        temp[:] = np.nan
        trg = np.argwhere(temp)
        vals = self.matrix[~np.isnan(self.matrix)]
        tree = spatial.cKDTree(src)
        dists, ix = tree.query(trg, k=len(src), workers=-1)
        weights = 1.0 / dists ** p
        weights[np.isposinf(weights)] = 1e12
        wshape = weights.shape
        weights.shape = wshape + ((vals.ndim - 1) * (1,))
        trgvals = vals[ix]
        interpol = np.sum(weights * trgvals, axis=1) / np.sum(weights, axis=1)
        return interpol.reshape(n, m)
