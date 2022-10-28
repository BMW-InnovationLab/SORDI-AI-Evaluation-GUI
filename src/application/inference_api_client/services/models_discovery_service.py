import requests
import os

from domain.contracts.abstract_models_discovery_service import AbstractModelsDiscoveryService
from typing import List

from domain.excpetions.inference_apis_exceptions import ModelsDiscoveryError
from domain.models.evaluation_job_parameters import EvaluationJobParameters

from shared.helpers.json_helpers import jsonify_string



class ModelsDiscoveryService(AbstractModelsDiscoveryService):

    def discover_models(self, url: str) -> List[str]:
        
        url = os.path.join(url, 'load')
        response = requests.get(url)
        

        if response.status_code == 200:
            models = response.json()
            return list(models.keys())

        else:
            raise ModelsDiscoveryError(response.status_code, response.reason)
    


    def check_model_validity(self, evaluation_job_parameters:EvaluationJobParameters) -> bool:
        url = os.path.join(evaluation_job_parameters.url, 'models')
        url = os.path.join(url, evaluation_job_parameters.model_name)
        url = os.path.join(url, 'load')
        
        response = requests.get(url)

        if response.status_code == 200:
            json_response = response.json()
            return json_response["success"]

        else:
            raise Exception
