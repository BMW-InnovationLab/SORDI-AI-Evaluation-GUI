from typing import Dict

from application.calculation.image_classification.services.image_classification_calculation_service import \
    ImageClassificationCalculationService
from application.calculation.object_detection.services.object_detection_calculation_service import \
    ObjectDetectionCalculationService
from domain.contracts.abstract_calculation_service import AbstractCalculationService
from domain.models.evaluation_job_parameters import EvaluationJobParameters
from domain.models.evaluation_job_results import EvaluationJobResults
from domain.models.inference_types import InferenceTypes
from domain.models.linkage_job_result import LinkageJobResult
from pandas import DataFrame


class CalculationService(AbstractCalculationService):
    def __init__(self):

        self.calculation_instances: Dict[str, AbstractCalculationService] = dict()
        self.calculation_mappings: Dict[str, AbstractCalculationService] = dict()
        self._initialize_mappings()

    def _initialize_mappings(self) -> None:
        self.calculation_mappings = {
            InferenceTypes.image_classification.value: ImageClassificationCalculationService,
            InferenceTypes.object_detection.value: ObjectDetectionCalculationService
        }

    def _get_calculation_instance(self,
                                  evaluation_job_parameters: EvaluationJobParameters) -> AbstractCalculationService:
        if evaluation_job_parameters.job_type in self.calculation_instances.keys():
            return self.calculation_instances.get(evaluation_job_parameters.job_type)

        else:
            calculation_instance: AbstractCalculationService = self.calculation_mappings.get(
                evaluation_job_parameters.job_type)()
            self.calculation_instances[evaluation_job_parameters.job_type] = calculation_instance
            return calculation_instance

    def calculate(self, evaluation_result: EvaluationJobResults,
                  iou_threshold: float,
                  evaluation_job_parameters: EvaluationJobParameters,
                  linkage_job_result: LinkageJobResult) -> DataFrame:
        calculation_instance: AbstractCalculationService = self._get_calculation_instance(evaluation_job_parameters)
        results = calculation_instance.calculate(evaluation_result=evaluation_result,
                                                 iou_threshold=iou_threshold,
                                                 evaluation_job_parameters=evaluation_job_parameters,
                                                 linkage_job_result=linkage_job_result)
        return results

    def generate_linkage_results(self, evaluation_result: EvaluationJobResults,
                                 evaluation_job_parameters: EvaluationJobParameters) -> DataFrame:
        print(
            f"Generating {evaluation_job_parameters.job_type} base linkages for job with uid {evaluation_job_parameters.uid}")
        calculation_instance: AbstractCalculationService = self.calculation_mappings.get(
            evaluation_job_parameters.job_type)()
        results = calculation_instance.generate_linkage_results(evaluation_result=evaluation_result,
                                                                evaluation_job_parameters=evaluation_job_parameters)
        print(
            f"Done generating {evaluation_job_parameters.job_type} base linkages for job with uid {evaluation_job_parameters.uid}")
        return results
