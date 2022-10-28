from typing import List

from pydantic import BaseModel


class HistogramSeries(BaseModel):
    name: str
    bins: List[float]
    data: List[int]
