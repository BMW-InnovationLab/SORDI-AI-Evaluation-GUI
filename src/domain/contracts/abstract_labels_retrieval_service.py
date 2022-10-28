from abc import ABC, ABCMeta, abstractmethod

from typing import List

class AbstractLabelsRetrievalService(ABC):

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_labels(self, uid:str) -> List[str]:
        pass
