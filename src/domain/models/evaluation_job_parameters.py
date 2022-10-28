from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, validator

from domain.excpetions.validation_exceptions import InvalidInferenceApiType, InvalidLabelsFormat
from domain.models.inference_types import InferenceTypes


class EvaluationJobParameters(BaseModel):
    uid: Optional[str]
    dataset_name: str
    job_name: str
    url: str
    model_name: str
    author_name: str
    labels_type: Optional[str]
    confidence_threshold: Optional[float]
    iou_threshold: Optional[float]
    iou_good_threshold: Optional[float]
    iou_average_threshold: Optional[float]
    job_type: str
    batch_size: int
    lite_evaluation: bool = False
    creation_date: Optional[datetime]


    @validator('batch_size')
    def check_batch_size(cls, batch_size: int):
        if batch_size <= 0:
            raise ValueError('Batch size must be strictly positive')
        return batch_size

    @validator('iou_threshold','iou_average_threshold', 'iou_good_threshold','confidence_threshold', pre=True)
    def check_values(cls, value: float):
        if value is not None:
            if value < 0 or value > 1:
                raise ValueError("Value must be between 0 and 1")
            else:
                return value
        else:
            return value

    @validator('iou_average_threshold', pre=True)
    def check_average_smaller_than_good(cls, value: float, values):

        if 'iou_good_threshold' in values and values['iou_good_threshold'] is not None and value >= values[
            'iou_good_threshold']:
            raise ValueError("IoU Average Threshold must be lower than IoU good threshold")

        else:
            return value

    @validator('job_type')
    def check_job_type_valid(cls, job_type: str, values, **kwargs):

        accepted_types: List[str] = [
            'object_detection',
            'image_classification'
        ]

        if job_type not in accepted_types:
            raise ValueError(InvalidInferenceApiType().message)

        if ({'iou_good_threshold', 'iou_average_threshold', 'confidence_threshold', 'iou_threshold'}.issubset(
                values)) and job_type == InferenceTypes.object_detection.value \
                and (values['iou_good_threshold'] is None or values['iou_average_threshold'] is None or values[
            'confidence_threshold'] is None or values['iou_threshold'] is None):
            raise ValueError("IoU fields and confidence threshold are mandatory for object detection")

        else:
            return job_type

    @validator('labels_type')
    def check_labels_type_valid(cls, labels_type: str):

        accepted_types: List[str] = [
            'json',
            'pascal'
        ]

        if labels_type not in accepted_types:
            raise ValueError(InvalidLabelsFormat().message)
        else:
            return labels_type
