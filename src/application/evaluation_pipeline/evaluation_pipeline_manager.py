from domain.excpetions.inference_apis_exceptions import InvalidInferenceApiUrl
from domain.excpetions.validation_exceptions import InvalidDataset, InvalidModel
from domain.models.evaluation_job_parameters import EvaluationJobParameters
from shared.helpers.uuid_helpers import get_uuid


class EvaluationPipelineManager:

    def __init__(self, dataset_validation_service, models_discovery_service, testing_url_validity_service,
                 evaluation_pipeline_service):
        self.dataset_validation_service = dataset_validation_service
        self.models_discovery_service = models_discovery_service
        self.testing_url_validity_service = testing_url_validity_service
        self.evaluation_pipeline_service = evaluation_pipeline_service

    def check_evaluation_job_parameters(self,
                                        evaluation_job_parameters: EvaluationJobParameters) -> EvaluationJobParameters:
        if not self.dataset_validation_service.check_dataset_valid(evaluation_job_parameters):
            raise InvalidDataset

        valid: bool = self.testing_url_validity_service.test_url_validity(evaluation_job_parameters.url)

        if not valid:
            raise InvalidInferenceApiUrl

        if not self.models_discovery_service.check_model_validity(evaluation_job_parameters):
            raise InvalidModel

        evaluation_job_parameters.uid = get_uuid()
        return evaluation_job_parameters

    def run_evaluation_job(self, evaluation_job_parameters: EvaluationJobParameters) -> None:
        self.evaluation_pipeline_service.run_evaluation_pipeline(evaluation_job_parameters)
