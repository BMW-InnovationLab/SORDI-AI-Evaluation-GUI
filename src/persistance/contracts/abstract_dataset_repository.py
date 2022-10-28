from abc import abstractmethod, ABC, ABCMeta
from typing import List

from domain.models.dataset_information import DatasetInformation


class AbstractDatasetRepository(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def list_dataset(self) -> List[DatasetInformation]:
        pass
