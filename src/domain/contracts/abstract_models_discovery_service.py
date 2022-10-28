from abc import abstractmethod, ABC, ABCMeta

from typing import List

from domain.models.evaluation_job_parameters import EvaluationJobParameters

class AbstractModelsDiscoveryService(ABC):

    __metaclass__ = ABCMeta

    @abstractmethod
    def discover_models(self, url:str) -> List[str]:
        pass
            

    @abstractmethod
    def check_model_validity(self, evaluation_job_parameters:EvaluationJobParameters) -> bool:
        pass