import os
from typing import Dict

from domain.models.evaluation_job_results import EvaluationJobResults

from domain.models.evaluation_job_parameters import EvaluationJobParameters

from application.web_images_extraction.models.web_images_type import WebImagesType
from domain.contracts.abstract_web_images_service import AbstractWebImagesService

from application.web_images_extraction.services.image_classification_web_images_service import ImageClassificationWebImagesService
from application.web_images_extraction.services.object_detection_web_images_service import ObjectDetectionWebImagesService
from domain.contracts.abstract_image_drawing_service import AbstractImageDrawingService


class WebImagesExtractionService:

    def __init__(self, image_drawing_service: AbstractImageDrawingService):
        self.image_drawing_service = image_drawing_service
        self.web_images_instances: Dict[str, AbstractWebImagesService] = dict()
        self.web_images_mappings: Dict[str, AbstractWebImagesService] = dict()
        self._initialize_mappings()

    def _initialize_mappings(self) -> None:
        self.web_images_mappings = {
            WebImagesType.image_classification.value: ImageClassificationWebImagesService,
            WebImagesType.object_detection.value: ObjectDetectionWebImagesService
        }

    def _get_web_images_instance(self, job_type: str) -> AbstractWebImagesService:
        if job_type in self.web_images_instances.keys():
            return self.web_images_instances.get(job_type)
        else:
            web_images_instance: AbstractWebImagesService = self.web_images_mappings.get(job_type)(image_drawing_service=self.image_drawing_service)
            self.web_images_instances[job_type] = web_images_instance
            return web_images_instance

    def extract_web_images(self, evaluation_job_results: EvaluationJobResults,
                           evaluation_job_parameters: EvaluationJobParameters):
        servable_path = os.path.join("../servable_images/", evaluation_job_parameters.uid)
        if not os.path.isdir(servable_path):
            os.makedirs(servable_path)
        output_image_instance: AbstractWebImagesService = self._get_web_images_instance(evaluation_job_parameters.job_type)

        output_image_instance.get_sample_images(
            linkages_df=evaluation_job_results.linkages_by_iou, gt_df=evaluation_job_results.ground_truths,
            predictions_df=evaluation_job_results.predictions,
            servable_path=servable_path)
        output_image_instance.get_per_class_sample_images(
            linkages_df=evaluation_job_results.linkages_by_iou, gt_df=evaluation_job_results.ground_truths,
            predictions_df=evaluation_job_results.predictions,
            servable_path=servable_path)
