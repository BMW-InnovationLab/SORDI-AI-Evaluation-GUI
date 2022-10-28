from abc import ABC, ABCMeta, abstractmethod

from pandas import DataFrame

from domain.models.evaluation_job_parameters import EvaluationJobParameters


class AbstractOutputGraphsService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def plot(self, linkages_df: DataFrame, evaluation_job_parameters: EvaluationJobParameters,
             output_dir: str) -> None: raise NotImplementedError
