import requests
import os
from typing import Dict, List

from domain.contracts.abstract_inference_retrieval_service import AbstractInferenceRetrievalService
from domain.models.inference_retrieval_request_body import InferenceRetrievalRequestBody


class InferenceRetrievalService(AbstractInferenceRetrievalService):

    def get_inference(self, inference_retrieval_request_body: InferenceRetrievalRequestBody) -> List[Dict]:

        url: str = os.path.join(inference_retrieval_request_body.url, 'models')
        url = os.path.join(url, inference_retrieval_request_body.model_name)
        url = os.path.join(url, 'predict')

        files: Dict = {'input_data': open(inference_retrieval_request_body.image_path, "rb")}

        response = requests.post(url, files=files)

        json_response = response.json()

        if response.status_code == 200 and json_response['success'] == True:
            return json_response['data']['bounding-boxes'] if isinstance(json_response['data'], Dict) and "bounding-boxes" in json_response['data'].keys() else [max(json_response['data'], key=lambda x:x['Confidence'])]
        
        else:
            raise Exception
