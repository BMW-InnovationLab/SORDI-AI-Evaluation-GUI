from typing import List

from domain.excpetions.inference_apis_exceptions import InvalidInferenceApiUrl
from domain.models.inference_service_details import InferenceServiceDetails
from domain.models.inference_service_request_body import InferenceServiceRequestBody
from persistance.contracts.abstract_inference_services_repository import AbstractInferenceServicesRepository


class InferenceServicesManager:
    def __init__(self, testing_url_validity_service,
                 inference_service_details_creator_service,
                 inference_services_repository: AbstractInferenceServicesRepository):
        self.testing_url_validity_service = testing_url_validity_service
        self.inference_service_details_creator_service = inference_service_details_creator_service
        self.inference_services_repository = inference_services_repository

    def _get_inference_services(self) -> List[InferenceServiceDetails]:
        return self.inference_services_repository.get_inference_services()

    def _get_service_by_id(self, uuid: str) -> InferenceServiceDetails:
        services: List[InferenceServiceDetails] = self._get_inference_services()
        for service in services:
            if service.uuid == uuid:
                return service

    def get_all_services(self) -> List[InferenceServiceDetails]:
        return self._get_inference_services()

    def add_service(self, inference_service_request_body: InferenceServiceRequestBody) -> None:

        existing_services: List[InferenceServiceDetails] = self._get_inference_services()

        if self.testing_url_validity_service.test_url_validity(inference_service_request_body.url):
            existing_services.append(
                self.inference_service_details_creator_service.create_inference_service_details_object(
                    inference_service_request_body))
            self.inference_services_repository.save_inference_services(existing_services)

        else:
            raise InvalidInferenceApiUrl

    def edit_service(self, inference_service_request_body: InferenceServiceRequestBody) -> InferenceServiceDetails:

        existing_services: List[InferenceServiceDetails] = self._get_inference_services()

        if self.testing_url_validity_service.test_url_validity(inference_service_request_body.url):
            for service in existing_services:
                if service.uuid == inference_service_request_body.uuid:
                    index: int = existing_services.index(service)
                    existing_services[
                        index] = self.inference_service_details_creator_service.create_inference_service_details_object(
                        inference_service_request_body)

            self.inference_services_repository.save_inference_services(existing_services)
            return self._get_service_by_id(inference_service_request_body.uuid)

        else:
            raise InvalidInferenceApiUrl

    def remove_service(self, uuid: str) -> None:
        existing_services: List[InferenceServiceDetails] = self._get_inference_services()

        for service in existing_services:
            if service.uuid == uuid:
                index: int = existing_services.index(service)
                existing_services.pop(index)

        self.inference_services_repository.save_inference_services(existing_services)
