from typing import Dict

from application.metrics.services.base_metric_linkage_type_service import BaseMetricLinkageType
from domain.models.linkage_type import LinkageType
from domain.models.metric_calculation_parameters import MetricsCalculationParameters
from domain.models.metric_result import MetricResult


class AccuracyService(BaseMetricLinkageType):
    """
        Accuracy = (Correct predictions)/(Total number of examples) = (TP+TN)/(Total number of examples)
    """

    def calculate_metric(self, calculation_parameters: MetricsCalculationParameters) -> MetricResult:
        prediction_linkage_results: Dict[LinkageType, int] = self.get_linkage_type_result(calculation_parameters)

        prediction_count = sum(prediction_linkage_results.values())

        accuracy = ((prediction_linkage_results[LinkageType.true_positive] + prediction_linkage_results[
            LinkageType.true_negative]) / prediction_count) if prediction_count > 0 else 0
        return MetricResult(metric='Accuracy', value=accuracy * 100)
