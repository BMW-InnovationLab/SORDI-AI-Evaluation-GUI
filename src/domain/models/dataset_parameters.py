from typing import List, Optional

from pydantic import BaseModel, validator

from domain.excpetions.validation_exceptions import InvalidInferenceApiType


class DatasetParameters(BaseModel):
    dataset_name: str
    job_type: str
    batch_size: Optional[int] = 1
    labels_type: str = 'json'

    @validator('batch_size')
    def check_batch_size(cls, batch_size: int):
        if batch_size <= 0:
            raise ValueError('Batch size must be strictly positive')
        return batch_size

    @validator('job_type')
    def check_job_type_valid(cls, job_type: str):
        accepted_types: List[str] = [
            'object_detection',
            'image_classification'
        ]

        if job_type not in accepted_types:
            raise ValueError(InvalidInferenceApiType().message)
        return job_type
