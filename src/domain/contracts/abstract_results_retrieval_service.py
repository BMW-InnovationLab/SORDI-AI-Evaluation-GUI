from abc import ABC, ABCMeta, abstractmethod
from domain.models.evaluation_job_results import EvaluationJobResults 

class AbstractResultsRetrievalService(ABC):

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_results(self, uid:str) -> EvaluationJobResults:
        pass