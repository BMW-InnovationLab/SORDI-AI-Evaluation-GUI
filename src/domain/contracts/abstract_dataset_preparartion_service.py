from abc import ABC, ABCMeta, abstractmethod
from typing import List

from domain.models.evaluation_job_parameters import EvaluationJobParameters
from domain.models.inference_object import InferenceObject


class AbstractDatasetPreparationService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_ground_truths(self, evaluation_job_parameters: EvaluationJobParameters) -> List[
        InferenceObject]: raise NotImplementedError
