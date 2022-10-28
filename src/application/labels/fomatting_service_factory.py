from application.labels.services.image_classification_formatting_service import ImageClassificationFormattingService
from application.labels.services.object_detection_formatting_service import ObjectDetectionFormattingService
from domain.contracts.services.abstract_factory import BaseFactory
from domain.contracts.services.abstract_inference_formatting_service import AbstractInferenceFormattingService
from domain.models.inference_types import InferenceTypes


class FormattingServiceFactory(BaseFactory[AbstractInferenceFormattingService]):
    def __init__(self):
        super().__init__()

    def _initialize_mappings(self) -> None:
        self.mappings = {
            InferenceTypes.image_classification.value: ImageClassificationFormattingService,
            InferenceTypes.object_detection.value: ObjectDetectionFormattingService
        }
