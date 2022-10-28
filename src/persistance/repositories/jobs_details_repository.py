from typing import Dict, List

from domain.excpetions.validation_exceptions import InvalidJobId
from domain.models.evaluation_job_details import EvaluationJobDetails
from persistance.contracts.abstract_jobs_details_repository import AbstractJobsDetailsRepository


class JobsDetailsRepository(AbstractJobsDetailsRepository):
    def __init__(self):
        self.jobs_details_store: Dict[str, EvaluationJobDetails] = dict()

    def set_job_details(self, evaluation_job_details: EvaluationJobDetails) -> None:
        self.jobs_details_store[evaluation_job_details.parameters.uid] = evaluation_job_details

    def get_all_jobs(self) -> List[EvaluationJobDetails]:
        return list(self.jobs_details_store.values())

    def get_job_by_uid(self, uid: str) -> EvaluationJobDetails:
        return self.jobs_details_store.get(uid, None)

    def delete_job(self, uid: str) -> None:
        if uid not in list(self.jobs_details_store.keys()):
            raise InvalidJobId
        else:
            self.jobs_details_store.pop(uid)
