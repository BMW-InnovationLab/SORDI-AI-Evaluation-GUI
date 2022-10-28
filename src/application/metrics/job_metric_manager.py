from typing import List, Optional, Type

from pandas import DataFrame

from application.metrics.services.accuracy_service import AccuracyService
from application.metrics.services.bad_iou_service import BadIoUService
from application.metrics.services.confidence_service import ConfidenceService
from application.metrics.services.f_score_service import FScoreService
from application.metrics.services.iou_service import IoUService
from application.metrics.services.average_precision_service import AveragePrecisionService
from application.metrics.services.precision_service import PrecisionService
from application.metrics.services.recall_service import RecallService
from domain.contracts.abstract_job_metric_manager import AbstractJobMetricManager
from domain.contracts.abstract_job_metric_service import AbstractJobMetricService
from domain.contracts.abstract_jobs_details_service import AbstractJobsDetailsService
from domain.contracts.abstract_labels_retrieval_service import AbstractLabelsRetrievalService
from domain.contracts.abstract_results_retrieval_service import AbstractResultsRetrievalService
from domain.excpetions.metrics_exceptions import NoResultsException
from domain.excpetions.web_graphs_exceptions import InvalidLabelName
from domain.models.evaluation_job_parameters import EvaluationJobParameters
from domain.models.metric_calculation_parameters import MetricsCalculationParameters
from domain.models.metric_result import MetricResult


class JobMetricManager(AbstractJobMetricManager):
    def __init__(self, job_details_service: AbstractJobsDetailsService,
                 label_service: AbstractLabelsRetrievalService,
                 results_retrieval_service: AbstractResultsRetrievalService):
        self._job_details_service = job_details_service
        self._label_service = label_service
        self._results_retrieval_service = results_retrieval_service
        self._classification_metrics: List[Type[AbstractJobMetricService]] = [AccuracyService,
                                                                              PrecisionService,
                                                                              RecallService,
                                                                              FScoreService,
                                                                              ConfidenceService]
        self._object_detection_metrics: List[Type[AbstractJobMetricService]] = [IoUService, BadIoUService,AveragePrecisionService]
        self._object_detection_metrics.extend(self._classification_metrics)

    def get_metrics(self, job_id: str, per_label: Optional[str] = None) -> List[MetricResult]:
        if per_label is not None and per_label not in self._label_service.get_labels(job_id):
            raise InvalidLabelName

        job_parameters: EvaluationJobParameters = self._job_details_service.get_job_parameters(job_id)
        linkages_df: DataFrame = self._results_retrieval_service.get_results(job_id).linkages_by_iou

        if linkages_df.empty:
            raise NoResultsException

        metrics_parameters = MetricsCalculationParameters(linkages_df=linkages_df, job_parameters=job_parameters,
                                                          per_label=per_label)
        metrics = self._classification_metrics if job_parameters.job_type == 'image_classification' \
            else self._object_detection_metrics
        return [metric().calculate_metric(metrics_parameters) for metric in metrics]
