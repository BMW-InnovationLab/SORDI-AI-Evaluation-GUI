from application.metrics.services.base_iou_service import BaseIoUService
from domain.models.metric_calculation_parameters import MetricsCalculationParameters
from domain.models.metric_result import MetricResult


class IoUService(BaseIoUService):
    """
        Average prediction IoU
    """

    def calculate_metric(self, calculation_parameters: MetricsCalculationParameters) -> MetricResult:
        iou = self.get_iou_values(calculation_parameters)
        if len(iou) > 0:
            mean = iou.mean()
        else:
            mean = 0
        return MetricResult(metric='IoU', value=mean * 100)
