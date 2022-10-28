from pydantic import BaseModel

class InferenceRetrievalRequestBody(BaseModel):
    url: str
    model_name:str
    image_path:str
