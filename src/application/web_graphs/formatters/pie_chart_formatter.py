from typing import List, Any

from pandas import DataFrame

from domain.excpetions.web_graphs_exceptions import InvalidLabelName
from domain.models.web_graph_output_object import WebGraphsOutputObject
from domain.contracts.abstract_web_graphs_formatter import AbstractWebGraphsFormatter
from domain.models.linkage_type import LinkageType
from domain.models.web_graphs_parameters import WebGraphsParameters


class PieChartFormatter(AbstractWebGraphsFormatter):

    def get_general_output(self, linkages_df: DataFrame,
                           web_graphs_parameters: WebGraphsParameters) -> WebGraphsOutputObject:
        try:
            title: str = "General Pie chart for all classes distribution"
            labels: List[str] = [linkage_type.value for linkage_type in LinkageType]
            data: List[int] = [(linkages_df.linkage_type.values == label).sum().tolist() for label in labels]

            return WebGraphsOutputObject(title=title, labels=labels, series=data)
        except Exception as e:
            raise e

    def get_per_label_output(self, linkages_df: DataFrame,
                             web_graphs_parameters: WebGraphsParameters) -> WebGraphsOutputObject:
        try:
            title: str = "Per Label Pie chart for class: " + web_graphs_parameters.label_name
            labels: List[str] = [linkage_type.value for linkage_type in LinkageType]
            if web_graphs_parameters.label_name not in linkages_df.gt_label.unique().tolist():
                raise InvalidLabelName

            data: List[int] = [int((linkages_df.loc[(linkages_df["gt_label"] == web_graphs_parameters.label_name) | (
                        (linkages_df.gt_label.isnull()) & (linkages_df["prediction_label"] == web_graphs_parameters.label_name))].linkage_type.values == label).sum())
                               for label in labels]

            return WebGraphsOutputObject(title=title, labels=labels, series=data)

        except InvalidLabelName:
            raise InvalidLabelName
        except Exception as e:
            raise e
