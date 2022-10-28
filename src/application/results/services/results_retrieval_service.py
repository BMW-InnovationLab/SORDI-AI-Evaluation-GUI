from domain.contracts.abstract_results_retrieval_service import AbstractResultsRetrievalService
from domain.models.evaluation_job_results import EvaluationJobResults


class ResultsRetrievalService(AbstractResultsRetrievalService):

    def __init__(self, results_repository):
        self.results_repository = results_repository
        # print(id(self.results_repository))

    def get_results(self, uid: str) -> EvaluationJobResults:
        return self.results_repository.get_results(uid)
