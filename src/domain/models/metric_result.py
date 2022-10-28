from typing import Optional

from pydantic import BaseModel


class MetricResult(BaseModel):
    metric: str
    value: float
