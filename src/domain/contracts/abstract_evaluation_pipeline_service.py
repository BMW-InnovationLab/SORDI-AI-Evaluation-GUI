from abc import ABC, ABCMeta, abstractmethod
from domain.models.evaluation_job_parameters import EvaluationJobParameters

class AbstractEvaluationPipelineService(ABC):

    __metaclass__ = ABCMeta


    @abstractmethod
    def run_evaluation_pipeline(self, evaluation_job_parameters: EvaluationJobParameters) -> None:
        pass




    