from typing import Dict

from pandas import DataFrame

from persistance.contracts.abstract_results_repository import AbstractResultsRepository
from domain.excpetions.validation_exceptions import InvalidJobId
from domain.models.evaluation_job_results import EvaluationJobResults


class ResultsRepository(AbstractResultsRepository):
    def __init__(self):
        self.store: Dict[str, EvaluationJobResults] = dict()

    def _initialize_job(self, uid: str) -> EvaluationJobResults:
        if not uid in self.store.keys():
            self.store[uid] = EvaluationJobResults(
                ground_truths=DataFrame(),
                predictions=DataFrame(),
                base_linkages=DataFrame(),
                classification_linkages=DataFrame(),
                linkages_by_iou=DataFrame(),
                inference_time=0
            )

        return self.store[uid]

    def save_ground_truths(self, uid: str, evaluation_job_results: EvaluationJobResults) -> None:
        stored_evaluation_job_results: EvaluationJobResults = self._initialize_job(uid)
        stored_evaluation_job_results.ground_truths = evaluation_job_results.ground_truths
        self.store[uid] = stored_evaluation_job_results

    def save_predictions(self, uid: str, evaluation_job_results: EvaluationJobResults) -> None:
        stored_evaluation_job_results: EvaluationJobResults = self._initialize_job(uid)
        stored_evaluation_job_results.predictions = evaluation_job_results.predictions
        self.store[uid] = stored_evaluation_job_results

    def save_linkages(self, uid: str, linkages_to_save: DataFrame) -> None:
        stored_evaluation_job_results: EvaluationJobResults = self._initialize_job(uid)
        stored_evaluation_job_results.linkages_by_iou = linkages_to_save
        self.store[uid] = stored_evaluation_job_results

    def get_results(self, uid: str) -> EvaluationJobResults:
        return self._initialize_job(uid)

    def delete_results(self, uid: str) -> None:

        if not uid in list(self.store.keys()):
            raise InvalidJobId

        else:
            self.store.pop(uid)
