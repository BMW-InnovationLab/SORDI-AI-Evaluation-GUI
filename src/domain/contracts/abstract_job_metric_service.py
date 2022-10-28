from abc import ABC, ABCMeta, abstractmethod

from domain.models.metric_calculation_parameters import MetricsCalculationParameters
from domain.models.metric_result import MetricResult


class AbstractJobMetricService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def calculate_metric(self, calculation_parameters: MetricsCalculationParameters) -> MetricResult:
        pass
