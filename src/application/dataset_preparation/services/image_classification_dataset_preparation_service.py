import os
from typing import List

from domain.contracts.abstract_dataset_preparartion_service import AbstractDatasetPreparationService
from domain.models.evaluation_job_parameters import EvaluationJobParameters
from domain.models.inference_object import InferenceObject
from shared.helpers.dataset_helpers import get_dataset_path
from shared.services.image_classification_formatting_service import ImageClassificationFormattingService


class ImageClassificationDatasetPreparationService(AbstractDatasetPreparationService):

    def __init__(self):
        self.formatter = ImageClassificationFormattingService()

    def _get_classes_folders(self, evaluation_job_parameters: EvaluationJobParameters) -> List[str]:
        classes_folders: List[str] = []
        dataset_path: str = get_dataset_path(evaluation_job_parameters.dataset_name, evaluation_job_parameters.job_type)

        for element in os.listdir(dataset_path):
            if os.path.isdir(os.path.join(dataset_path, element)):
                classes_folders.append(os.path.join(dataset_path, element))

        return classes_folders

    def get_ground_truths(self, evaluation_job_parameters: EvaluationJobParameters) -> List[InferenceObject]:
        dataset_path: str = get_dataset_path(evaluation_job_parameters.dataset_name, evaluation_job_parameters.job_type)

        classes_folders: List[str] = self._get_classes_folders(evaluation_job_parameters)

        ground_truths: List[InferenceObject] = []

        for class_folder in classes_folders:

            class_name = os.path.split(class_folder)[1]

            for image in os.listdir(class_folder):
                image_path: str = os.path.join(class_folder, image)

                label: List[Dict] = [{'ObjectClass': class_name}]

                ground_truths.extend(self.formatter.get_inference_objects_list(label, image_path))

        return ground_truths
