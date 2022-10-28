import os

from pydantic import BaseModel

from domain.models.inference_types import InferenceTypes


class DatasetInformation(BaseModel):
    name: str
    type: InferenceTypes

