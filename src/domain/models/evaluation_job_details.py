from typing import Optional

from pydantic import BaseModel

from domain.models.evaluation_job_parameters import EvaluationJobParameters


class EvaluationJobDetails(BaseModel):
    status: str
    parameters: EvaluationJobParameters
    progress: int = 0 # todo make not optional
