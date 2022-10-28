from typing import List, Dict

from domain.contracts.abstract_dataset_preparartion_service import AbstractDatasetPreparationService
from domain.models.inference_types import InferenceTypes
from domain.models.inference_object import InferenceObject
from domain.models.evaluation_job_parameters import EvaluationJobParameters
from application.dataset_preparation.services.image_classification_dataset_preparation_service import ImageClassificationDatasetPreparationService
from application.dataset_preparation.services.object_detection_dataset_prepration_service import ObjectDetectionDatasetPreparationService

class DatasetPreparationService(AbstractDatasetPreparationService):

    def __init__(self):
        self.dataset_preparation_instances : Dict[str, AbstractDatasetPreparationService] = dict()
        self.dataset_preparation_mappings : Dict[str, AbstractDatasetPreparationService] = dict()
        self._initialize_mappings()


    def _initialize_mappings(self) -> None:
        self.dataset_preparation_mappings = {
            InferenceTypes.image_classification.value : ImageClassificationDatasetPreparationService,
            InferenceTypes.object_detection.value : ObjectDetectionDatasetPreparationService
        }


    def _get_dataset_preparation_service_instance(self, evaluation_job_parameters:EvaluationJobParameters) -> AbstractDatasetPreparationService:
        if evaluation_job_parameters.job_type in self.dataset_preparation_instances.keys():
            return self.dataset_preparation_instances.get(evaluation_job_parameters.job_type)

        else:
            dataset_preparation_service : AbstractDatasetPreparationService = self.dataset_preparation_mappings.get(evaluation_job_parameters.job_type)()
            self.dataset_preparation_instances[evaluation_job_parameters.job_type] = dataset_preparation_service
            return dataset_preparation_service

    
    def get_ground_truths(self, evaluation_job_parameters: EvaluationJobParameters) -> List[InferenceObject]:
        dataset_preparation_service: AbstractDatasetPreparationService = self._get_dataset_preparation_service_instance(evaluation_job_parameters)
        return dataset_preparation_service.get_ground_truths(evaluation_job_parameters)