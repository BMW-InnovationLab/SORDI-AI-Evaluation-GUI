from abc import ABC

import numpy as np
import pandas as pd

from domain.contracts.abstract_job_metric_service import AbstractJobMetricService
from domain.models.metric_calculation_parameters import MetricsCalculationParameters


class BaseIoUService(AbstractJobMetricService, ABC):
    def get_iou_values(self, calculation_parameters: MetricsCalculationParameters) -> np.ndarray:
        if calculation_parameters.per_label is None:
            iou: np.array = calculation_parameters.linkages_df.iou.values[
                pd.notnull(calculation_parameters.linkages_df.iou.values)]
        else:
            label = calculation_parameters.per_label
            iou: np.array = np.round(calculation_parameters.linkages_df.loc[calculation_parameters
                                     .linkages_df["gt_label"] == label].iou.values[np.logical_not
            (pd.isnull(calculation_parameters.linkages_df.
                       loc[calculation_parameters.linkages_df["gt_label"] == label].iou.values))].tolist(), 2)
        return iou
