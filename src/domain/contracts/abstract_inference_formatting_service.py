from abc import abstractmethod, ABC, ABCMeta
from typing import List, Dict

from domain.models.inference_object import InferenceObject


class AbstractInferenceFormattingService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_inference_objects_list(self, inference_objects: List[Dict], image_path: str) -> List[
        InferenceObject]: raise NotImplementedError
