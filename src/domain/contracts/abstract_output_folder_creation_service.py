from abc import ABC, ABCMeta, abstractmethod
from domain.models.evaluation_job_parameters import EvaluationJobParameters

class AbstractOutputFolderCreationService(ABC):

    __metaclass__ = ABCMeta

    @abstractmethod
    def create_output_folder(self, evaluation_job_parameters:EvaluationJobParameters) -> str:
        pass