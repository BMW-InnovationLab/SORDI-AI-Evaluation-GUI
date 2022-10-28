from pydantic import BaseModel


class JobStatusObject(BaseModel):
    uid: str
    job_name: str
    status: str
    model_name: str
    author_name: str
    dataset_name: str
    progress: int
