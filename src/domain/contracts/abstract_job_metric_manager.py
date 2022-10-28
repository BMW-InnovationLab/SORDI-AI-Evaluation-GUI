from abc import ABC, ABCMeta, abstractmethod
from typing import List, Optional

from domain.models.metric_result import MetricResult


class AbstractJobMetricManager(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_metrics(self, job_id: str, per_label: Optional[str] = None) -> List[MetricResult]:
        pass
