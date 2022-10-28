from pydantic import BaseModel
from typing import Optional


class InferenceObject(BaseModel):
    image_path: str
    class_id: Optional[str]
    class_name: Optional[str]
    confidence: Optional[float]
    left: Optional[int]
    top: Optional[int]
    right: Optional[int]
    bottom: Optional[int]
