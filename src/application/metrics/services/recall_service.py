from typing import Dict

from application.metrics.services.base_metric_linkage_type_service import BaseMetricLinkageType
from domain.models.linkage_type import LinkageType
from domain.models.metric_calculation_parameters import MetricsCalculationParameters
from domain.models.metric_result import MetricResult


class RecallService(BaseMetricLinkageType):
    """
        Recall = TP/(TP+FN)
    """

    def calculate_metric(self, calculation_parameters: MetricsCalculationParameters) -> MetricResult:
        prediction_linkage_results: Dict[LinkageType, int] = self.get_linkage_type_result(calculation_parameters)

        total_positive = prediction_linkage_results[LinkageType.true_positive] + prediction_linkage_results[
            LinkageType.false_negative]
        if total_positive > 0:
            recall = prediction_linkage_results[LinkageType.true_positive] / total_positive
        else:
            recall = 0
        return MetricResult(metric='Recall', value=recall * 100)
