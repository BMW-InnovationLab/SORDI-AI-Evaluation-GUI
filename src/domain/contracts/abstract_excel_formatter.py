from abc import abstractmethod, ABC, ABCMeta

from typing import List, Dict

from pandas import DataFrame

from domain.models.evaluation_job_parameters import EvaluationJobParameters
from domain.models.inference_object import InferenceObject


class AbstractExcelFormatter(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def create_report(self, linkages_df: DataFrame, prediction_df: DataFrame, gt_df: DataFrame,
                      evaluation_job_parameter: EvaluationJobParameters,
                      output_path: str) -> None: raise NotImplementedError
