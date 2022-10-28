import os
from typing import Dict

from pandas import DataFrame

from application.output_images.models.output_images_type import OutputImagesTypes
from application.output_images.services.image_classification_output_image_service import \
    ImageClassificationOutputImageService
from application.output_images.services.object_detection_output_image_service import ObjectDetectionOutputImageService
from domain.contracts.abstract_output_image_service import AbstractOutputImageService
from domain.models.evaluation_job_parameters import EvaluationJobParameters
from domain.models.evaluation_job_results import EvaluationJobResults

from domain.contracts.abstract_image_drawing_service import AbstractImageDrawingService


class OutputImageService():

    def __init__(self, image_drawing_service: AbstractImageDrawingService):
        self.image_drawing_service: AbstractImageDrawingService = image_drawing_service

        self.output_images_instances: Dict[str, AbstractOutputImageService] = dict()
        self.output_images_mappings: Dict[str, AbstractOutputImageService] = dict()
        self._initialize_mappings()

    def _initialize_mappings(self) -> None:
        self.output_images_mappings = {
            OutputImagesTypes.image_classification.value: ImageClassificationOutputImageService,
            OutputImagesTypes.object_detection.value: ObjectDetectionOutputImageService
        }

    def _get_output_images_instance(self, job_type: str) -> AbstractOutputImageService:
        if job_type in self.output_images_instances.keys():
            return self.output_images_instances.get(job_type)
        else:
            output_image_instance: AbstractOutputImageService = self.output_images_mappings.get(job_type)(image_drawing_service=self.image_drawing_service)
            self.output_images_instances[job_type] = output_image_instance
            return output_image_instance

    def get_output_images(self, evaluation_job_results: EvaluationJobResults, output_path: str,
                          evaluation_job_parameters: EvaluationJobParameters) -> None:

        output_path: str = os.path.join(output_path, "02-Specific Per Label Evaluation")

        self._get_output_images_instance(evaluation_job_parameters.job_type).get_output_images(
            linkages_df=evaluation_job_results.linkages_by_iou, gt_df=evaluation_job_results.ground_truths,
            predictions_df=evaluation_job_results.predictions,
            output_path=output_path)
