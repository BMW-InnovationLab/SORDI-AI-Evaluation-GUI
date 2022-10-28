from abc import ABC, ABCMeta

from pandas import DataFrame


class AbstractLinkageTypeCalculationService(ABC):
    __metaclass__ = ABCMeta

    def get_true_negative_case(self, linkage_df: DataFrame, ground_truths: DataFrame, predictions_df: DataFrame,
                               linkage_type: str) -> DataFrame: raise NotImplementedError

    def get_false_negative_cases(self, linkage_df: DataFrame,
                                 ground_truths: DataFrame) -> DataFrame: raise NotImplementedError

    def get_false_positive_cases(self, linkage_df: DataFrame,
                                 predictions_df: DataFrame) -> DataFrame: raise NotImplementedError
