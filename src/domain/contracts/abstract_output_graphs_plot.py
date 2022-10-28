from abc import ABC, ABCMeta, abstractmethod

from pandas import DataFrame

from domain.models.evaluation_job_parameters import EvaluationJobParameters


class AbstractOutputGraphsPlot(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def draw_general_plot(self, linkages_df: DataFrame, evaluation_job_parameters: EvaluationJobParameters,
                          output_dir: str) -> None: raise NotImplementedError

    @abstractmethod
    def draw_per_class_plot(self, linkages_df: DataFrame, evaluation_job_parameters: EvaluationJobParameters,
                            output_dir: str) -> None: raise NotImplementedError
