import os

from domain.contracts.abstract_dataset_validator import AbstractDatasetValidator
from domain.models.dataset_parameters import DatasetParameters
from shared.helpers.dataset_helpers import get_dataset_path


class BatchSizeValidator(AbstractDatasetValidator):
    def check_dataset_valid(self, evaluation_job_parameters: DatasetParameters) -> bool:
        dataset_path: str = get_dataset_path(evaluation_job_parameters.dataset_name, evaluation_job_parameters.job_type)

        if not os.path.isdir(os.path.join(dataset_path, 'images')): return False

        nb_items: int = len(os.listdir(os.path.join(dataset_path, 'images')))
        return nb_items >= evaluation_job_parameters.batch_size
