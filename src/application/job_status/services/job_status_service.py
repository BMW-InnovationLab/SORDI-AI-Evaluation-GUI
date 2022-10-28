from domain.contracts.abstract_job_status_service import AbstractJobStatusService
from domain.excpetions.validation_exceptions import InvalidJobId
from domain.models.job_status_object import JobStatusObject
from domain.models.job_statuses import JobStatuses
from persistance.contracts.abstract_job_status_repository import AbstractJobStatusRepository


class JobStatusService(AbstractJobStatusService):
    def __init__(self, job_status_repository: AbstractJobStatusRepository):
        self.job_status_repository = job_status_repository

    def set_job_status(self, job_status_object: JobStatusObject) -> None:
        if job_status_object.status == JobStatuses.done.value:
            existing_job_status_object = self.job_status_repository.get_job_by_uid(job_status_object.uid)
            if existing_job_status_object is None:
                raise InvalidJobId

        self.job_status_repository.set_job_status(job_status_object)

    def get_jobs_statuses(self):
        return self.job_status_repository.get_all_jobs()
