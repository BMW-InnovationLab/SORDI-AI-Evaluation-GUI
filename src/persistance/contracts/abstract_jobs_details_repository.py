from abc import ABC, ABCMeta, abstractmethod
from typing import List

from domain.models.evaluation_job_details import EvaluationJobDetails


class AbstractJobsDetailsRepository(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def set_job_details(self, evaluation_job_details: EvaluationJobDetails) -> None:
        pass

    @abstractmethod
    def get_all_jobs(self) -> List[EvaluationJobDetails]:
        pass

    @abstractmethod
    def get_job_by_uid(self, uid: str) -> EvaluationJobDetails:
        pass

    @abstractmethod
    def delete_job(self, uid: str) -> None:
        pass
