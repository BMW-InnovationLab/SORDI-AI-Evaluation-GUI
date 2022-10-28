from abc import ABC, ABCMeta, abstractmethod

from pandas import DataFrame
from domain.models.evaluation_job_parameters import EvaluationJobParameters


class AbstractLinkageCalculationService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_linkage_result(self, ground_truths_df: DataFrame, predictions_df: DataFrame,
                           evaluation_job_parameters: EvaluationJobParameters) -> DataFrame: raise NotImplementedError
