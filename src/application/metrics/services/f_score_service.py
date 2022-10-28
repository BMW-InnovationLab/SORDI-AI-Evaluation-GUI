from typing import Dict

from application.metrics.services.base_metric_linkage_type_service import BaseMetricLinkageType
from domain.models.linkage_type import LinkageType
from domain.models.metric_calculation_parameters import MetricsCalculationParameters
from domain.models.metric_result import MetricResult


class FScoreService(BaseMetricLinkageType):
    """
        F-Score = 2* (Precision*Recall)/(Precision+Recall) = (tp)/(tp+0.5(fp+fn))
    """

    def calculate_metric(self, calculation_parameters: MetricsCalculationParameters) -> MetricResult:
        prediction_linkage_results: Dict[LinkageType, int] = self.get_linkage_type_result(calculation_parameters)

        den: float = prediction_linkage_results[LinkageType.true_positive] + (0.5 * (
                prediction_linkage_results[LinkageType.false_positive] + prediction_linkage_results[
            LinkageType.false_negative]))

        if den == 0: MetricResult(metric='F-Score', value=0)
        f_score = prediction_linkage_results[LinkageType.true_positive] / den

        return MetricResult(metric='F-Score', value=f_score * 100)
