from pandas import DataFrame

from domain.contracts.abstract_job_metric_service import AbstractJobMetricService
from domain.models.metric_calculation_parameters import MetricsCalculationParameters
from domain.models.metric_result import MetricResult


class ConfidenceService(AbstractJobMetricService):
    """
        Average prediction confidence
    """
    def calculate_metric(self, calculation_parameters: MetricsCalculationParameters) -> MetricResult:
        df: DataFrame = calculation_parameters.linkages_df.loc[calculation_parameters.linkages_df["gt_label"] ==
                                                               calculation_parameters.per_label] \
            if calculation_parameters.per_label is not None else calculation_parameters.linkages_df
        confidence = df['confidence'].mean()
        return MetricResult(metric='Confidence', value=confidence)
