from abc import abstractmethod, ABC, ABCMeta

from domain.models.inference_service_details import InferenceServiceDetails
from domain.models.inference_service_request_body import InferenceServiceRequestBody

class AbstractInferenceServiceDetailsCreatorService(ABC):


    __metaclass__ = ABCMeta

    @abstractmethod
    def create_inference_service_details_object(self, inference_service_request_body: InferenceServiceRequestBody) -> InferenceServiceDetails:
        pass