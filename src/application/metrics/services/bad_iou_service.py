import numpy as np

from application.metrics.services.base_iou_service import BaseIoUService
from domain.models.metric_calculation_parameters import MetricsCalculationParameters
from domain.models.metric_result import MetricResult


class BadIoUService(BaseIoUService):
    def calculate_metric(self, calculation_parameters: MetricsCalculationParameters) -> MetricResult:
        iou: np.ndarray = self.get_iou_values(calculation_parameters)
        bad_iou: np.ndarray = np.extract(iou < calculation_parameters.job_parameters.iou_average_threshold, iou)
        if len(bad_iou) > 0:
            mean = bad_iou.mean()
        else:
            mean = 0
        return MetricResult(metric='Bad IoU', value=mean * 100)
