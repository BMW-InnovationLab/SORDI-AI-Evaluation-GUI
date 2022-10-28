from typing import Dict

from application.metrics.services.base_metric_linkage_type_service import BaseMetricLinkageType
from domain.models.linkage_type import LinkageType
from domain.models.metric_calculation_parameters import MetricsCalculationParameters
from domain.models.metric_result import MetricResult
from pandas import DataFrame
from domain.models.inference_types import InferenceTypes
import numpy as np
from typing import List, Tuple


class AveragePrecisionService(BaseMetricLinkageType):
    """
        Average Precision = Area Under Curve of precision-recall graph
        https://github.com/yfpeng/object_detection_metrics/blob/3801acc32d052d1fbf1565f96a9f8d390701f911/src/podm/metrics.py
    """

    def calculate_metric(self, calculation_parameters: MetricsCalculationParameters) -> MetricResult:
        # Get all linkages
        linkages: DataFrame = calculation_parameters.linkages_df

        # Get all labels required for computation
        labels = calculation_parameters.per_label if calculation_parameters.per_label is not None else linkages.loc[
            linkages['gt_label'].notnull(), 'gt_label'].unique().tolist()

        # Compute average precision for each label
        average_precisions = []
        for label in labels:
            average_precisions.append(
                self._compute_average_precision(linkages.copy(), label))

        # Compute (mean) average precision
        average_precision = sum(average_precisions) / len(average_precisions)

        return MetricResult(metric='Average Precision', value=average_precision * 100)

    def _compute_average_precision(self, linkages: DataFrame, label: str) -> float:
        linkages = linkages.loc[(linkages["gt_label"] == label)
                                | ((linkages.gt_label.isnull()) &
                                   (linkages[
                                        "prediction_label"] == label))]

        true_positive_count = np.zeros(linkages.shape[0])
        false_positive_count = np.zeros(linkages.shape[0])
        linkages_sorted = linkages.sort_values(by=["confidence"], ascending=False)

        index = 0
        for row in linkages_sorted.itertuples():
            if row.linkage_type == LinkageType.true_positive.value:
                true_positive_count[index] = 1
            if row.linkage_type == LinkageType.false_positive.value:
                false_positive_count[index] = 1
            index += 1

        cumulative_false_positive_count = np.cumsum(false_positive_count)
        cumulative_true_positive_count = np.cumsum(true_positive_count)
        number_of_gt = linkages_sorted.loc[linkages_sorted.gt_index.notna()].gt_index.count()

        recalls = np.divide(cumulative_true_positive_count, number_of_gt,
                            out=np.full_like(cumulative_true_positive_count, np.nan), where=number_of_gt != 0)
        precisions = np.divide(cumulative_true_positive_count,
                               (cumulative_false_positive_count + cumulative_true_positive_count))

        average_precision, mrec, mpre, _ = self.calculate_all_points_average_precision(recalls, precisions)

        return average_precision

    def calculate_all_points_average_precision(self, recall: List[float], precision: List[float]) \
            -> Tuple[float, List[float], List[float], List[int]]:
        """
        All-point interpolated average precision
        Returns:
            average precision
            interpolated recall
            interpolated precision
            interpolated points
        """
        mrec = [0.0] + [e for e in recall] + [1.0]
        mpre = [0.0] + [e for e in precision] + [0]
        for i in range(len(mpre) - 1, 0, -1):
            mpre[i - 1] = max(mpre[i - 1], mpre[i])
        ii = []
        for i in range(len(mrec) - 1):
            if mrec[i + 1] != mrec[i]:
                ii.append(i + 1)
        ap = 0
        for i in ii:
            ap = ap + np.sum((mrec[i] - mrec[i - 1]) * mpre[i])
        return ap, mrec[0:len(mpre) - 1], mpre[0:len(mpre) - 1], ii
