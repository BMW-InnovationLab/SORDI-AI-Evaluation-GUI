from domain.contracts.abstract_dataset_validator import AbstractDatasetValidator
from domain.models.inference_types import InferenceTypes
from domain.contracts.abstract_dataset_validator import AbstractDatasetValidator
from domain.models.evaluation_job_parameters import EvaluationJobParameters
from application.dataset_validation.validators.image_classification_dataset_validator import ImageClassificationDatasetValidator
from application.dataset_validation.validators.object_detection_dataset_validator import ObjectDetectionDatasetValidator
from domain.contracts.abstract_dataset_validaton_service import AbstractDatasetValidationService

class DatasetValidationService(AbstractDatasetValidationService):

    def __init__(self):
        self.dataset_validator_instances : Dict[str, AbstractDatasetValidator] = dict()
        self.dataset_validator_mappings : Dict[str, AbstractDatasetValidator] = dict()
        self._initialize_mappings()


    def _initialize_mappings(self) -> None:
        self.dataset_validator_mappings = {
            InferenceTypes.image_classification.value : ImageClassificationDatasetValidator,
            InferenceTypes.object_detection.value : ObjectDetectionDatasetValidator
        }


    def _get_validator_instance(self, evaluation_job_parameters:EvaluationJobParameters) -> AbstractDatasetValidator:
        if evaluation_job_parameters.job_type in self.dataset_validator_instances.keys():
            return self.dataset_validator_instances.get(evaluation_job_parameters.job_type)

        else:
            dataset_validator : AbstractDatasetValidator = self.dataset_validator_mappings.get(evaluation_job_parameters.job_type)()
            self.dataset_validator_instances[evaluation_job_parameters.job_type] = dataset_validator
            return dataset_validator

    
    def check_dataset_valid(self, evaluation_job_parameters: EvaluationJobParameters) -> bool:
        dataset_validator: AbstractDatasetValidator = self._get_validator_instance(evaluation_job_parameters)
        return dataset_validator.check_dataset_valid(evaluation_job_parameters)
