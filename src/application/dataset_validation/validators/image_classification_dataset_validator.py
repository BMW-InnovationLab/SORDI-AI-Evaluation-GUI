import os
from typing import List, Tuple

from domain.contracts.abstract_dataset_validator import AbstractDatasetValidator
from domain.models.evaluation_job_parameters import EvaluationJobParameters
from shared.helpers.dataset_helpers import get_dataset_path


class ImageClassificationDatasetValidator(AbstractDatasetValidator):

    def __init__(self):
        self.accepted_image_extenstions: Tuple[str] = ('jpg', 'jpeg', 'png')

    def _check_dataset_structure_validity(self, evaluation_job_parameters: EvaluationJobParameters) -> bool:
        valid: bool = True if os.path.isdir(
            os.path.join(get_dataset_path(evaluation_job_parameters.dataset_name,
                                          evaluation_job_parameters.job_type))) else False
        return valid

    def _get_classes_folders(self, evaluation_job_parameters: EvaluationJobParameters) -> List[str]:
        classes_folders: List[str] = []
        dataset_path: str = get_dataset_path(evaluation_job_parameters.dataset_name, evaluation_job_parameters.job_type)

        for element in os.listdir(dataset_path):
            if os.path.isdir(os.path.join(dataset_path, element)):
                classes_folders.append(os.path.join(dataset_path, element))

        return classes_folders

    def _check_images_extensions(self, class_folder: str) -> bool:
        valid: bool = True

        for image in os.listdir(class_folder):
            if not image.lower().endswith(self.accepted_image_extenstions):
                valid = False
                break

        return valid

    def check_dataset_valid(self, evaluation_job_parameters: EvaluationJobParameters) -> bool:
        valid = self._check_dataset_structure_validity(evaluation_job_parameters)

        if valid:
            classes_folders: List[str] = self._get_classes_folders(evaluation_job_parameters)

            if len(classes_folders) == 0:
                valid = False

            i = 0
            while valid == True and i < len(classes_folders):
                valid = self._check_images_extensions(classes_folders[i])
                i += 1

        return valid
