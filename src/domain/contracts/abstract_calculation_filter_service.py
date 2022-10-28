from abc import ABC, ABCMeta, abstractmethod

from pandas import DataFrame


class AbstractCalculationFilterService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def filter_same_labels(self, linkage_df: DataFrame) -> None: raise NotImplementedError

    @abstractmethod
    def check_iou_threshold(self, linkage_df: DataFrame, iou_threshold: float) -> None: raise NotImplementedError

    @abstractmethod
    def filter_overlapping_predictions(self, linkage_df: DataFrame) -> None: raise NotImplementedError
