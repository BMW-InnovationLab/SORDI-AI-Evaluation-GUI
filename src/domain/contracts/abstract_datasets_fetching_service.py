from abc import ABC, ABCMeta, abstractmethod
from typing import List

from domain.models.dataset_information import DatasetInformation


class AbstractDatasetsFetchingService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_datasets(self) -> List[DatasetInformation]:
        pass
