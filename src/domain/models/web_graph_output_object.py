from typing import List, Any, Optional

from pydantic.main import BaseModel


class WebGraphsOutputObject(BaseModel):
    title: str
    labels: List[str]
    series: Optional[Any]
