from pydantic import BaseModel, validator
from typing import List

class InferenceServiceDetails(BaseModel):
    uuid : str
    name: str
    url: str
    inference_type: str
    models: List[str] = []




