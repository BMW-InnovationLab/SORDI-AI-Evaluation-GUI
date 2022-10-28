from pandas import DataFrame
from typing import Dict, List
from domain.models.dataframe_base_model import DataFrameBaseModel


class EvaluationJobResults(DataFrameBaseModel):
    ground_truths: DataFrame
    predictions: DataFrame
    base_linkages: DataFrame
    classification_linkages: DataFrame
    linkages_by_iou: DataFrame
    inference_time: float
