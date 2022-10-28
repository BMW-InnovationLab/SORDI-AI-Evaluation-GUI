import os
from typing import List

from domain.models.inference_service_details import InferenceServiceDetails
from persistance.contracts.abstract_inference_services_repository import AbstractInferenceServicesRepository
from persistance.contracts.abstract_path_service import AbstractPathService
from shared.helpers.json_helpers import parse_json, write_json


class InferenceServicesRepository(AbstractInferenceServicesRepository):
    def __init__(self, paths_service: AbstractPathService):
        self.inference_api_services_path: str = paths_service.paths.inference_api_services

    def _check_existence(self):
        if not os.path.exists(self.inference_api_services_path):
            initial_list: List[InferenceServiceDetails] = []
            write_json(self.inference_api_services_path, initial_list)

    def _get_serializable_list(self, inference_services: List[InferenceServiceDetails]) -> List:
        return [service.dict() for service in inference_services]

    def _get_objects_list(self, serialized_list) -> List[InferenceServiceDetails]:
        return [InferenceServiceDetails.parse_obj(service) for service in serialized_list]

    def save_inference_services(self, inference_services: List[InferenceServiceDetails]) -> None:
        write_json(self.inference_api_services_path, self._get_serializable_list(inference_services))

    def get_inference_services(self) -> List[InferenceServiceDetails]:
        self._check_existence()
        return self._get_objects_list(parse_json(self.inference_api_services_path))
