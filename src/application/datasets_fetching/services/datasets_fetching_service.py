from typing import List

from domain.contracts.abstract_datasets_fetching_service import AbstractDatasetsFetchingService
from domain.models.dataset_information import DatasetInformation
from persistance.contracts.abstract_dataset_repository import AbstractDatasetRepository


class DatasetsFetchingService(AbstractDatasetsFetchingService):
    def __init__(self, dataset_repository: AbstractDatasetRepository):
        self._dataset_repo = dataset_repository

    def get_datasets(self) -> List[DatasetInformation]:
        return self._dataset_repo.list_dataset()
