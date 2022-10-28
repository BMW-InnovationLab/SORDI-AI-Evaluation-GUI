from typing import List
from pandas import DataFrame


from domain.contracts.abstract_results_storage_service import AbstractResultsStorageService
from domain.models.inference_object import InferenceObject
from domain.models.evaluation_job_results import EvaluationJobResults
from domain.excpetions.validation_exceptions import InvalidJobId


class ResultsStorageService(AbstractResultsStorageService):

    def __init__(self, results_retrieval_service, results_repository):
        self.results_retrival_service = results_retrieval_service
        self.results_repository = results_repository

    def save_predictions(self, uid: str, predictions_to_save: List[InferenceObject]) -> None:
        evaluation_job_results: EvaluationJobResults = self.results_retrival_service.get_results(uid)
        for prediction in predictions_to_save:
            evaluation_job_results.predictions = evaluation_job_results.predictions.append(prediction.dict(),
                                                                                           ignore_index=True)

        self.results_repository.save_predictions(uid, evaluation_job_results)

    def save_ground_truths(self, uid: str, predictions_to_save: List[InferenceObject]) -> None:
        evaluation_job_results: EvaluationJobResults = self.results_retrival_service.get_results(uid)
        for prediction in predictions_to_save:
            evaluation_job_results.ground_truths = evaluation_job_results.ground_truths.append(prediction.dict(),
                                                                                               ignore_index=True)
        self.results_repository.save_ground_truths(uid, evaluation_job_results)

    def save_linkages(self, uid: str, linkages_to_save: DataFrame) -> None:
        self.results_repository.save_linkages(uid, linkages_to_save)

    def get_results_based_on_image_paths(self, uid: str, image_paths: List[str]) -> EvaluationJobResults:
        if not uid in self.results_repository.store.keys():
            self.results_repository.store[uid] = EvaluationJobResults(
                ground_truths=DataFrame(),
                predictions=DataFrame(),
                base_linkages=DataFrame(),
                classification_linkages=DataFrame(),
                linkages_by_iou=DataFrame(),
                inference_time=0
            )
        results: EvaluationJobResults = self.results_repository.get_results(uid)

        results.predictions = results.predictions.loc[results.predictions.image_path.isin(image_paths)]
        results.ground_truths = results.ground_truths.loc[results.ground_truths.image_path.isin(image_paths)]
        return results

    def delete_results(self, uid: str) -> None:

        try:
            self.results_repository.delete_results(uid)

        except InvalidJobId:
            raise InvalidJobId
