from abc import ABC, ABCMeta, abstractmethod

from pandas import DataFrame


class AbstractClassificationLinkageService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_classification_linkage_result(self, ground_truths: DataFrame,
                                          predictions: DataFrame) -> DataFrame: raise NotImplementedError
