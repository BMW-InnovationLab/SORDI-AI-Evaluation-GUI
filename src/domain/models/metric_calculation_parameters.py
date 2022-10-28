from typing import Optional

from pandas import DataFrame
from pydantic import BaseModel

from domain.models.evaluation_job_parameters import EvaluationJobParameters


class MetricsCalculationParameters(BaseModel):
    linkages_df: DataFrame
    job_parameters: EvaluationJobParameters
    per_label: Optional[str]

    class Config:
        arbitrary_types_allowed = True
