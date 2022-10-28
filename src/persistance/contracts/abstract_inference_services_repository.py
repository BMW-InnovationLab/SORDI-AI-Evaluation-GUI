from abc import abstractmethod, ABC, ABCMeta
from typing import List

from domain.models.inference_service_details import InferenceServiceDetails


class AbstractInferenceServicesRepository(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_inference_services(self) -> List[InferenceServiceDetails]:
        pass

    @abstractmethod
    def save_inference_services(self, inference_services: List[InferenceServiceDetails]) -> None:
        pass
