from typing import List

from domain.contracts.abstract_jobs_details_service import AbstractJobsDetailsService
from domain.excpetions.validation_exceptions import InvalidJobId
from domain.models.evaluation_job_details import EvaluationJobDetails
from domain.models.evaluation_job_parameters import EvaluationJobParameters
from domain.models.job_status_object import JobStatusObject
from domain.models.job_statuses import JobStatuses


class JobsDetailsService(AbstractJobsDetailsService):

    def __init__(self, jobs_details_repository):
        self.jobs_details_repository = jobs_details_repository

    def set_job_status(self, evaluation_job_details: EvaluationJobDetails) -> None:
        if evaluation_job_details.status == JobStatuses.done.value:
            existing_job_status_object = self.jobs_details_repository.get_job_by_uid(
                evaluation_job_details.parameters.uid)

            if existing_job_status_object is None:
                raise InvalidJobId

        self.jobs_details_repository.set_job_details(evaluation_job_details)

    def get_jobs_statuses(self) -> List[JobStatusObject]:

        evaluation_jobs: List[EvaluationJobDetails] = self.jobs_details_repository.get_all_jobs()

        return [self._job_as_status_dto(job) for job in evaluation_jobs]

    def get_job_status(self, uuid: str) -> JobStatusObject:
        job: EvaluationJobDetails = self.jobs_details_repository.get_job_by_uid(uuid)
        if job is None: raise InvalidJobId
        return self._job_as_status_dto(job)

    def _job_as_status_dto(self, job: EvaluationJobDetails) -> JobStatusObject:
        return JobStatusObject(
            uid=job.parameters.uid,
            job_name=job.parameters.job_name,
            status=job.status,
            progress=job.progress,
            model_name=job.parameters.model_name,
            author_name=job.parameters.author_name,
            dataset_name=job.parameters.dataset_name)

    def get_job_parameters(self, uid: str) -> EvaluationJobParameters:
        if self.jobs_details_repository.get_job_by_uid(uid) is not None:
            return self.jobs_details_repository.get_job_by_uid(uid).parameters
        else:
            raise InvalidJobId

    def delete_job_details(self, uid: str) -> None:
        try:
            return self.jobs_details_repository.delete_job(uid)
        except InvalidJobId as e:
            raise InvalidJobId
