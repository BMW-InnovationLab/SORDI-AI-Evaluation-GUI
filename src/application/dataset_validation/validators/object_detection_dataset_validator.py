import os
from typing import Dict, Tuple

from domain.contracts.abstract_dataset_validator import AbstractDatasetValidator
from domain.models.evaluation_job_parameters import EvaluationJobParameters
from shared.helpers.dataset_helpers import get_dataset_path


class ObjectDetectionDatasetValidator(AbstractDatasetValidator):

    def __init__(self):

        self.label_to_extenstion_map: Dict[str, str] = {
            'json': 'json'
        }

        self.accepted_image_extenstions: Tuple[str] = ('jpg', 'jpeg', 'png')

    def _check_dataset_structure_validity(self, evaluation_job_parameters: EvaluationJobParameters) -> bool:
        dataset_path: str = get_dataset_path(evaluation_job_parameters.dataset_name, evaluation_job_parameters.job_type)

        valid = True if os.path.isdir(os.path.join(dataset_path, 'images')) else False

        if valid == True:
            valid = True if os.path.isdir(os.path.join(dataset_path, 'labels')) else False

        if valid == True:
            valid = True if os.path.isdir(
                os.path.join(os.path.join(dataset_path, 'labels'), evaluation_job_parameters.labels_type)) else False

        return valid

    def _check_images_extensions(self, evaluation_job_parameters: EvaluationJobParameters) -> bool:
        valid: bool = True

        dataset_path: str = get_dataset_path(evaluation_job_parameters.dataset_name, evaluation_job_parameters.job_type)

        for image in os.listdir(os.path.join(dataset_path, 'images')):
            if not image.lower().endswith(self.accepted_image_extenstions):
                valid = False
                break

        return valid

    def _check_labels_extensions(self, evaluation_job_parameters: EvaluationJobParameters) -> bool:
        valid: bool = True

        dataset_path: str = get_dataset_path(evaluation_job_parameters.dataset_name, evaluation_job_parameters.job_type)

        for label in os.listdir(
                os.path.join(os.path.join(dataset_path, 'labels'), evaluation_job_parameters.labels_type)):
            if not label.lower().endswith(self.label_to_extenstion_map[evaluation_job_parameters.labels_type]):
                valid = False
                break

        return valid

    def check_dataset_valid(self, evaluation_job_parameters: EvaluationJobParameters) -> bool:
        valid = self._check_dataset_structure_validity(evaluation_job_parameters)

        if valid:
            valid = self._check_images_extensions(evaluation_job_parameters)

        if valid:
            valid = self._check_labels_extensions(evaluation_job_parameters)

        return valid
