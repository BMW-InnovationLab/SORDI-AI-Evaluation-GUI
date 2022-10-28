from pydantic import BaseModel
from typing import Optional, Tuple


class LinkageObject(BaseModel):
    id: int
    image_path: str
    gt_index: Optional[int]
    gt_label: Optional[str]
    prediction_index: Optional[int]
    prediction_label: Optional[str]
    iou: Optional[float]
    ecludien_distance: Optional[float]
    confidence: Optional[float]
    gt_centroid: Optional[Tuple[float, float]]
    prediction_centroid: Optional[Tuple[float, float]]
    linkage_type: Optional[str]
