from abc import ABC, ABCMeta, abstractmethod

from domain.models.evaluation_job_parameters import EvaluationJobParameters 


class AbstractDatasetValidationService(ABC):

    __metaclass__ = ABCMeta

    @abstractmethod
    def check_dataset_valid(self, evaluation_job_parameters: EvaluationJobParameters) -> bool:
        pass