from typing import List

import numpy as np
from pandas import DataFrame
import pandas as pd

from application.web_graphs.models.histogram_series import HistogramSeries
from domain.excpetions.web_graphs_exceptions import InvalidLabelName
from domain.models.evaluation_job_parameters import EvaluationJobParameters
from domain.models.web_graph_output_object import WebGraphsOutputObject
from domain.contracts.abstract_web_graphs_formatter import AbstractWebGraphsFormatter
from domain.models.web_graphs_parameters import WebGraphsParameters


class HistogramFormatter(AbstractWebGraphsFormatter):

    def _get_histogram_distribution(self, title: str, all_iou_value: np.array,
                                    web_graphs_parameters: WebGraphsParameters) -> WebGraphsOutputObject:

        all_bins: List[List[float]] = \
            [[round(i, 2) for i in np.arange(0, web_graphs_parameters.iou_average_threshold + 0.01, 0.05).tolist()],
             [round(i, 2) for i in np.arange(web_graphs_parameters.iou_average_threshold, web_graphs_parameters.iou_good_threshold + 0.01,0.05).tolist()],
             [round(i, 2) for i in np.arange(web_graphs_parameters.iou_good_threshold, 1.01, 0.05).tolist()]]

        all_hist: List[int] = [np.histogram(all_iou_value, bins=bins)[0].tolist() for bins in all_bins]

        return WebGraphsOutputObject(title=title, labels=["iou", "Number of detections"], series=[
            HistogramSeries(name="bad_iou", bins=all_bins[0], data=all_hist[0]).dict(),
            HistogramSeries(name="average_iou", bins=all_bins[1], data=all_hist[1]).dict(),
            HistogramSeries(name="good_iou", bins=all_bins[2], data=all_hist[2]).dict(),
        ])

    def get_general_output(self, linkages_df: DataFrame,
                           web_graphs_parameters: WebGraphsParameters) -> WebGraphsOutputObject:
        try:
            title: str = "Histogram of IoU distribution"

            all_iou_value: np.array = linkages_df.iou.values[pd.notnull(linkages_df.iou.values)]

            return self._get_histogram_distribution(title=title, all_iou_value=all_iou_value,
                                                    web_graphs_parameters=web_graphs_parameters)
        except Exception as e:
            raise e

    def get_per_label_output(self, linkages_df: DataFrame,
                             web_graphs_parameters: WebGraphsParameters) -> WebGraphsOutputObject:
        try:
            title: str = "Histogram of IoU distribution for class: " + web_graphs_parameters.label_name

            if web_graphs_parameters.label_name not in linkages_df.gt_label.unique().tolist():
                raise InvalidLabelName

            all_iou_value: np.array = np.round(
                linkages_df.loc[linkages_df["gt_label"] == web_graphs_parameters.label_name].iou.values[np.logical_not(
                    pd.isnull(linkages_df.loc[
                                  linkages_df["gt_label"] == web_graphs_parameters.label_name].iou.values))].tolist(),2)

            return self._get_histogram_distribution(title=title, all_iou_value=all_iou_value,
                                                    web_graphs_parameters=web_graphs_parameters)
        except InvalidLabelName:
            raise InvalidLabelName
        except Exception as e:
            raise e
