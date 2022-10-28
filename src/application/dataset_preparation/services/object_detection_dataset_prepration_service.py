import os
from typing import List, Dict

from application.labels.services.object_detection_formatting_service import ObjectDetectionFormattingService
from domain.contracts.abstract_dataset_preparartion_service import AbstractDatasetPreparationService
from domain.models.evaluation_job_parameters import EvaluationJobParameters
from domain.models.inference_object import InferenceObject
from persistance.services.path_service import PathService
from shared.helpers.filename_helpers import get_filename_without_extension
from shared.helpers.json_helpers import parse_json


class ObjectDetectionDatasetPreparationService(AbstractDatasetPreparationService):
    def __init__(self):
        self.paths_service = PathService()  # todo change
        self.formatter = ObjectDetectionFormattingService()

    def get_ground_truths(self, evaluation_job_parameters: EvaluationJobParameters) -> List[InferenceObject]:
        dataset_path: str = os.path.join(self.paths_service.paths.base_dataset, evaluation_job_parameters.job_type,
                                         evaluation_job_parameters.dataset_name)
        images_path: str = os.path.join(dataset_path, 'images')
        labels_path: str = os.path.join(dataset_path, 'labels', evaluation_job_parameters.labels_type)

        labels_stem: Dict[str, str] = {get_filename_without_extension(label): label for label in
                                       os.listdir(labels_path)}
        ground_truths: List[InferenceObject] = []
        for image in os.listdir(images_path):
            label = labels_stem.get(get_filename_without_extension(image), None)
            if label is None: continue
            image_path: str = os.path.join(images_path, image)
            label_path: str = os.path.join(labels_path, label)
            if evaluation_job_parameters.labels_type == 'json':
                label_content = parse_json(label_path)
                ground_truths.extend(self.formatter.get_inference_objects_list(label_content, image_path))


        return ground_truths
