from typing import List

from domain.models.inference_service_details import InferenceServiceDetails
from domain.models.inference_service_request_body import InferenceServiceRequestBody
from shared.helpers.uuid_helpers import get_uuid


class InferenceServiceDetailsCreatorService:
    def __init__(self, models_discovery_service):
        self.models_discovery_service = models_discovery_service

    def create_inference_service_details_object(self,
                                                inference_service_request_body: InferenceServiceRequestBody) \
            -> InferenceServiceDetails:
        uuid: str = get_uuid() if inference_service_request_body.uuid is None else inference_service_request_body.uuid
        models: List[str] = self.models_discovery_service.discover_models(
            inference_service_request_body.url) if inference_service_request_body.discover_models\
            else inference_service_request_body.models
        return InferenceServiceDetails(
            uuid=uuid,
            name=inference_service_request_body.name,
            url=inference_service_request_body.url,
            inference_type=inference_service_request_body.inference_type,
            models=models
        )
