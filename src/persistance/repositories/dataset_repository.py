import os
from typing import List

from domain.models.dataset_information import DatasetInformation
from domain.models.inference_types import InferenceTypes
from persistance.contracts.abstract_dataset_repository import AbstractDatasetRepository
from persistance.contracts.abstract_path_service import AbstractPathService


class DatasetRepository(AbstractDatasetRepository):
    def __init__(self, paths_service: AbstractPathService):
        self._paths_service: AbstractPathService = paths_service

    def list_dataset(self) -> List[DatasetInformation]:
        return self._get_classification_datasets(self._paths_service.paths.classification_datasets) + \
               self._get_object_detection_datasets(self._paths_service.paths.object_detection_datasets)

    def _get_object_detection_datasets(self, path: str) -> List[DatasetInformation]:
        return [DatasetInformation(name=dataset, type=InferenceTypes.object_detection) for dataset in
                self._list_datasets(path)]

    def _get_classification_datasets(self, path: str) -> List[DatasetInformation]:
        return [DatasetInformation(name=dataset, type=InferenceTypes.image_classification) for dataset in
                self._list_datasets(path)]

    def _list_datasets(self, path: str) -> List[str]:
        return [dataset for dataset in os.listdir(path) if os.path.isdir(os.path.join(path, dataset))]
