from abc import ABC, ABCMeta, abstractmethod
from domain.models.job_status_object import JobStatusObject
from domain.models.evaluation_job_details import EvaluationJobDetails
from domain.models.evaluation_job_parameters import EvaluationJobParameters
from typing import List

class AbstractJobsDetailsService(ABC):

    __metaclass__ = ABCMeta


    @abstractmethod
    def set_job_status(self, evaluation_job_details: EvaluationJobDetails) -> None:
        pass


    @abstractmethod
    def get_jobs_statuses(self) -> List[JobStatusObject]:
        pass


    @abstractmethod
    def get_job_parameters(self, uid:str) -> EvaluationJobParameters:
        pass


    @abstractmethod
    def delete_job_details(self, uid:str) -> None:
        pass