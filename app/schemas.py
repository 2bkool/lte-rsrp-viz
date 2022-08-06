from typing import List, Optional

from pydantic import BaseModel


class SignalResponse(BaseModel):
    """
    Attributes:
        row_: adjusted row index
        col_: adjusted col index
    """
    lat: Optional[float] = None
    lon: Optional[float] = None
    row: Optional[int] = None
    col: Optional[int] = None
    row_: Optional[int] = None
    col_: Optional[int] = None
    matrix: Optional[List] = None
    status: Optional[str] = ''
    floor_peak: Optional[int] = None
    row_peak: Optional[int] = None
    col_peak: Optional[int] = None
