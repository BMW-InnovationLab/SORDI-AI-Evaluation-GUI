from typing import Dict, List

from domain.models.job_status_object import JobStatusObject
from persistance.contracts.abstract_job_status_repository import AbstractJobStatusRepository


class JobStatusRepository(AbstractJobStatusRepository):
    def __init__(self):
        self.jobs_statuses_store: Dict[str, JobStatusObject] = dict()

    def set_job_status(self, job_status_object: JobStatusObject) -> None:
        self.jobs_statuses_store[job_status_object.uid] = job_status_object

    def get_all_jobs(self) -> List[JobStatusObject]:
        return list(self.jobs_statuses_store.values())

    def get_job_by_uid(self, uid: str) -> JobStatusObject:
        return self.jobs_statuses_store.get(uid, None)
