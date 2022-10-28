from typing import Dict, Type

from domain.contracts.abstract_inference_formatting_service import AbstractInferenceFormattingService
from domain.models.evaluation_job_parameters import EvaluationJobParameters
from domain.models.inference_types import InferenceTypes
from shared.services.image_classification_formatting_service import ImageClassificationFormattingService
from shared.services.object_detection_formatting_service import ObjectDetectionFormattingService


class FormattingServiceFactory:
    def __init__(self):
        self.formatting_services_instances: Dict[str, AbstractInferenceFormattingService] = dict()
        self.formatting_services_mappings: Dict[str, Type[AbstractInferenceFormattingService]] = dict()
        self._initialize_mappings()

    def _initialize_mappings(self) -> None:
        self.formatting_services_mappings = {
            InferenceTypes.image_classification.value: ImageClassificationFormattingService,
            InferenceTypes.object_detection.value: ObjectDetectionFormattingService
        }

    def get_instance(self, evaluation_job_parameters: EvaluationJobParameters) -> AbstractInferenceFormattingService:
        if evaluation_job_parameters.job_type in self.formatting_services_instances.keys():
            return self.formatting_services_instances.get(evaluation_job_parameters.job_type)

        else:
            formatting_service: AbstractInferenceFormattingService = self.formatting_services_mappings.get(
                evaluation_job_parameters.job_type)()
            self.formatting_services_instances[evaluation_job_parameters.job_type] = formatting_service
            return formatting_service
