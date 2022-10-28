from abc import abstractmethod, ABC, ABCMeta

from typing import Dict, List

from domain.models.inference_retrieval_request_body import InferenceRetrievalRequestBody


class AbstractInferenceRetrievalService(ABC):

    __metaclass__ = ABCMeta
    
    @abstractmethod
    def get_inference(self, inference_retrieval_request_body: InferenceRetrievalRequestBody) -> List[Dict]:
        pass

    