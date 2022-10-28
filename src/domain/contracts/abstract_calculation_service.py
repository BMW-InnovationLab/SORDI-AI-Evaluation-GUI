from abc import ABC, ABCMeta, abstractmethod

from pandas import DataFrame

from domain.models.evaluation_job_parameters import EvaluationJobParameters
from domain.models.evaluation_job_results import EvaluationJobResults
from domain.models.linkage_job_result import LinkageJobResult


class AbstractCalculationService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def calculate(self, evaluation_result: EvaluationJobResults,
                  iou_threshold: float,
                  evaluation_job_parameters: EvaluationJobParameters,
                  linkage_job_result: LinkageJobResult) -> DataFrame: raise NotImplementedError
    @abstractmethod
    def generate_linkage_results(self, evaluation_result: EvaluationJobResults,
                                 evaluation_job_parameters: EvaluationJobParameters) -> DataFrame: raise NotImplementedError
