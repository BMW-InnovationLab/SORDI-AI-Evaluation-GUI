from typing import List, Dict

from domain.contracts.abstract_inference_formatting_service import AbstractInferenceFormattingService
from domain.models.inference_object import InferenceObject


class ImageClassificationFormattingService(AbstractInferenceFormattingService):
    def get_inference_objects_list(self, inference_objects: List[Dict], image_path: str) -> List[InferenceObject]:

        if not inference_objects:
            return [InferenceObject(image_path=image_path)]

        else:
            return [
                InferenceObject(
                    image_path=image_path,
                    class_name=inference_object['ObjectClass'],
                    confidence=inference_object['Confidence'] if 'Confidence' in inference_object.keys() else None)
                for inference_object in inference_objects
            ]
