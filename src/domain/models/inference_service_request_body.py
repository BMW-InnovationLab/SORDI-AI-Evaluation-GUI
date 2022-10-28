from pydantic import BaseModel, validator, ValidationError
from typing import List, Optional

from domain.excpetions.validation_exceptions import InvalidInferenceApiType

class InferenceServiceRequestBody(BaseModel):
    uuid: Optional[str]
    name: str
    url: str
    inference_type: str
    models: List[str] = []
    discover_models: bool


    @validator('inference_type')
    def check_inference_type_valid(cls, inference_type:str):

        accepted_types: List[str] = [
            'object_detection',
            'image_classification'
        ]

        if inference_type not in accepted_types:
            raise ValueError(InvalidInferenceApiType().message)


        else:
            return inference_type