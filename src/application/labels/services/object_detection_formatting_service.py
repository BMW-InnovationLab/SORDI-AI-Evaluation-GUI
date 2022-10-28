from typing import List, Dict

from domain.contracts.abstract_inference_formatting_service import AbstractInferenceFormattingService
from domain.models.inference_object import InferenceObject


class ObjectDetectionFormattingService(AbstractInferenceFormattingService):

    def get_inference_objects_list(self, inference_objects: List[Dict], image_path: str) -> List[InferenceObject]:
        if inference_objects == [] or inference_objects is None:
            return [InferenceObject(image_path=image_path)]
        else:
            return [
                InferenceObject(
                    image_path=image_path,
                    class_id=inference_object['ObjectClassId'],
                    class_name=inference_object['ObjectClassName'],
                    confidence=inference_object.get('confidence', None),
                    left=inference_object['coordinates']['left'] if 'coordinates' in inference_object.keys() else
                    inference_object['Left'],
                    top=inference_object['coordinates']['top'] if 'coordinates' in inference_object.keys() else
                    inference_object['Top'],
                    right=inference_object['coordinates']['right'] if 'coordinates' in inference_object.keys() else
                    inference_object['Right'],
                    bottom=inference_object['coordinates']['bottom'] if 'coordinates' in inference_object.keys() else
                    inference_object['Bottom'])
                for inference_object in inference_objects
            ]
