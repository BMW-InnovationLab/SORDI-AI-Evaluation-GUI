from abc import ABC, ABCMeta, abstractmethod
from typing import Union

from domain.models.dataset_parameters import DatasetParameters
from domain.models.evaluation_job_parameters import EvaluationJobParameters


class AbstractDatasetValidator(ABC):

    __metaclass__ = ABCMeta

    @abstractmethod
    def check_dataset_valid(self, evaluation_job_parameters: Union[EvaluationJobParameters, DatasetParameters]) -> bool:
        pass