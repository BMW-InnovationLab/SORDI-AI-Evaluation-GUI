from typing import List

from pydantic.main import BaseModel


class WebGraphInputObject(BaseModel):
    title: str
    labels: List[str]
    series: List[int]
