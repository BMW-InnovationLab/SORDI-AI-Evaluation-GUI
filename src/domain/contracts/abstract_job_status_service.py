from abc import ABC, ABCMeta, abstractmethod
from domain.models.job_status_object import JobStatusObject


class AbstractJobStatusService(ABC):

    __metaclass__ = ABCMeta


    @abstractmethod
    def set_job_status(self, job_status_object: JobStatusObject) -> None:
        pass

    @abstractmethod
    def get_jobs_statuses(self):
        pass