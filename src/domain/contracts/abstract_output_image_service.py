from abc import ABC, ABCMeta, abstractmethod

from pandas import DataFrame

from domain.models.evaluation_job_parameters import EvaluationJobParameters


class AbstractOutputImageService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_output_images(self, linkages_df: DataFrame, gt_df: DataFrame, predictions_df: DataFrame,
                          output_path: str) -> None: raise NotImplementedError
