from abc import ABC, ABCMeta, abstractmethod
from typing import List

from domain.models.job_status_object import JobStatusObject


class AbstractJobStatusRepository(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def set_job_status(self, job_status_object: JobStatusObject) -> None:
        pass

    @abstractmethod
    def get_all_jobs(self) -> List[JobStatusObject]:
        pass

    @abstractmethod
    def get_job_by_uid(self, uid: str) -> JobStatusObject:
        pass
