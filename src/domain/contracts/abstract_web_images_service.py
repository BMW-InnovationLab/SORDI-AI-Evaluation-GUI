from abc import ABC, ABCMeta, abstractmethod

from pandas import DataFrame


class AbstractWebImagesService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_sample_images(self, linkages_df: DataFrame, gt_df: DataFrame, predictions_df: DataFrame, servable_path: str) -> None: raise NotImplementedError

    @abstractmethod
    def get_per_class_sample_images(self, linkages_df: DataFrame, gt_df: DataFrame, predictions_df: DataFrame, servable_path: str) -> None: raise \
        NotImplementedError
