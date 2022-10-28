from abc import abstractmethod, ABC, ABCMeta

from domain.models.inference_object import InferenceObject
from typing import List
from domain.models.evaluation_job_results import EvaluationJobResults


class AbstractResultsStorageService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def save_predictions(self, uid: str, predictions_to_save: List[InferenceObject]) -> None:
        pass

    @abstractmethod
    def save_ground_truths(self, uid: str, predictions_to_save: List[InferenceObject]) -> None:
        pass

    @abstractmethod
    def get_results_based_on_image_paths(self, uid: str,
                                         image_paths: List[str]) -> EvaluationJobResults: raise NotImplementedError

    @abstractmethod
    def delete_results(self, uid: str) -> None:
        pass
