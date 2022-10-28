from pandas import DataFrame
from typing import List, Optional
from application.calculation.image_classification.services.image_classification_linkage_service import \
    ImageClassificationLinkageService
from domain.contracts.abstract_calculation_service import AbstractCalculationService
from domain.models.evaluation_job_parameters import EvaluationJobParameters
from domain.models.evaluation_job_results import EvaluationJobResults
from domain.models.linkage_job_result import LinkageJobResult
import pandas as pd


class ImageClassificationCalculationService(AbstractCalculationService):
    def __init__(self):
        self.image_classification_linkage_service = ImageClassificationLinkageService()

    def calculate(self, evaluation_result: EvaluationJobResults,
                  iou_threshold: float,
                  evaluation_job_parameters: EvaluationJobParameters,
                  linkage_job_result: LinkageJobResult) -> DataFrame:
        classification_result = self.image_classification_linkage_service.get_classification_linkage_result(
            ground_truths=evaluation_result.ground_truths, predictions=evaluation_result.predictions)
        # Update classification linkages
        evaluation_result.classification_linkages = classification_result if \
            len(classification_result) == 0 else pd.concat(
            [evaluation_result.classification_linkages, classification_result], ignore_index=True)

        return evaluation_result.classification_linkages

    def generate_linkage_results(self, evaluation_result: EvaluationJobResults,
                                 evaluation_job_parameters: EvaluationJobParameters) -> DataFrame:
        pass
