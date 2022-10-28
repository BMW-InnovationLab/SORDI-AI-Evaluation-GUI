from typing import List, Optional

from pandas import DataFrame

from application.calculation.object_detection.services.calculation_filter_service import CalculationFilterService
from application.calculation.object_detection.services.linkage_calculation_service import LinkageCalculationService
from application.calculation.object_detection.services.linkage_type_calculation_service import LinkageTypeCalculationService

from domain.contracts.abstract_calculation_service import AbstractCalculationService
from domain.models.evaluation_job_parameters import EvaluationJobParameters
from domain.models.evaluation_job_results import EvaluationJobResults
from domain.models.linkage_job_result import LinkageJobResult
from domain.models.linkage_type import LinkageType
import pandas as pd
from domain.excpetions.validation_exceptions import EmptyLinkages

class ObjectDetectionCalculationService(AbstractCalculationService):

    def __init__(self):
        self.linkage_calculation_service = LinkageCalculationService()
        self.linkage_type_calculation_service = LinkageTypeCalculationService()
        self.calculation_filter_service = CalculationFilterService()
        self.linkage_result = LinkageJobResult()

    def _get_linkage_case(self, linkage_result: LinkageJobResult,
                          evaluation_result: EvaluationJobResults) -> LinkageJobResult:
        # get only ground truth of  already predicted image only
        current_ground_truths_df: DataFrame = evaluation_result.ground_truths.loc[
            evaluation_result.ground_truths.image_path.isin(
                evaluation_result.predictions.image_path.values.tolist())].copy()

        linkage_result.linkage_df = self.linkage_type_calculation_service.get_false_positive_cases(
            linkage_df=linkage_result.linkage_df,
            predictions_df=evaluation_result.predictions)
        linkage_result.linkage_df = self.linkage_type_calculation_service.get_false_negative_cases(
            linkage_df=linkage_result.linkage_df,
            ground_truths=current_ground_truths_df)
        linkage_result.linkage_df = self.linkage_type_calculation_service.get_true_negative_case(
            linkage_df=linkage_result.linkage_df,
            ground_truths=evaluation_result.ground_truths,
            predictions_df=evaluation_result.predictions,
            linkage_type=LinkageType.true_negative.value)
        return linkage_result

    def _apply_filters(self, linkage_result: LinkageJobResult,
                       iou_threshold: float) -> LinkageJobResult:
        self.calculation_filter_service.filter_same_labels(linkage_result.linkage_df)
        self.calculation_filter_service.check_iou_threshold(linkage_result.linkage_df, iou_threshold)
        self.calculation_filter_service.filter_overlapping_predictions(linkage_result.linkage_df)
        return linkage_result

    def generate_linkage_results(self, evaluation_result: EvaluationJobResults,
                                 evaluation_job_parameters: EvaluationJobParameters) -> DataFrame:
        return self.linkage_calculation_service.get_linkage_result(
            evaluation_job_parameters=evaluation_job_parameters,
            ground_truths_df=evaluation_result.ground_truths,
            predictions_df=evaluation_result.predictions)

    def calculate(self, evaluation_result: EvaluationJobResults,
                  iou_threshold: Optional[float],
                  evaluation_job_parameters: EvaluationJobParameters,
                  linkage_job_result: LinkageJobResult) -> DataFrame:

        self.linkage_result = linkage_job_result

        if evaluation_result.base_linkages.empty is True:
            raise EmptyLinkages()


        temp_linkage_result = self._apply_filters(linkage_result=self.linkage_result.copy(),
                                                  iou_threshold=iou_threshold)
        temp_linkage_result = self._get_linkage_case(linkage_result=temp_linkage_result,
                                                     evaluation_result=evaluation_result)

        # Update linkages by iou
        evaluation_result.linkages_by_iou = temp_linkage_result.linkage_df if \
        iou_threshold not in evaluation_result.linkages_by_iou else pd.concat(
            [evaluation_result.linkages_by_iou, temp_linkage_result.linkage_df], ignore_index=True)

        return evaluation_result.linkages_by_iou