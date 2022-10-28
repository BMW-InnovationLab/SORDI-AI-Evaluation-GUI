from typing import Dict

from application.metrics.services.base_metric_linkage_type_service import BaseMetricLinkageType
from domain.models.linkage_type import LinkageType
from domain.models.metric_calculation_parameters import MetricsCalculationParameters
from domain.models.metric_result import MetricResult


class PrecisionService(BaseMetricLinkageType):
    """
        Precision = TP/(TP+FP)
    """

    def calculate_metric(self, calculation_parameters: MetricsCalculationParameters) -> MetricResult:
        prediction_linkage_results: Dict[LinkageType, int] = self.get_linkage_type_result(calculation_parameters)

        total_positive = prediction_linkage_results[LinkageType.true_positive] + prediction_linkage_results[
            LinkageType.false_positive]
        if total_positive > 0:
            precision = prediction_linkage_results[LinkageType.true_positive] / total_positive
        else:
            precision = 0
        return MetricResult(metric='Precision', value=precision * 100)
