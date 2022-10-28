from abc import abstractmethod
from typing import List, Dict
from sklearn.metrics import confusion_matrix

from pandas import DataFrame
import numpy as np

from domain.excpetions.web_graphs_exceptions import WebGraphsGenralException
from domain.models.web_graph_output_object import WebGraphsOutputObject
from domain.contracts.abstract_web_graphs_formatter import AbstractWebGraphsFormatter
from domain.models.linkage_type import LinkageType
from domain.models.web_graphs_parameters import WebGraphsParameters


class HeatMapFormatter(AbstractWebGraphsFormatter):

    def get_general_output(self, linkages_df: DataFrame,
                           web_graphs_parameters: WebGraphsParameters) -> WebGraphsOutputObject:
        try:
            title: str = "Heat Map Confusion Matrix for all classes: "
            prediction_labels: List[str] = linkages_df.prediction_label.astype(str).tolist()
            gt_labels: List[str] = linkages_df.gt_label.astype(str).tolist()
            all_label: List[str] = list(set(prediction_labels + gt_labels))

            # add nan to the end in the case of object_detection
            if "nan" in all_label:
                all_label.append(all_label.pop(all_label.index("nan")))


            confusion_matrix_output: List[int] = confusion_matrix(gt_labels, prediction_labels,
                                                                  labels=all_label).tolist()
            confusion_matrix_value_dict: List[Dict] = [
                {"name": str(value), "data": list([confusion_matrix_output[index]])} for index, value in enumerate(all_label)]

            return WebGraphsOutputObject(title=title, labels=all_label, series=confusion_matrix_value_dict)
        except Exception as e:
            raise e

    def get_per_label_output(self, linkages_df: DataFrame,
                             web_graphs_parameters: WebGraphsParameters) -> WebGraphsOutputObject:
        pass
