from typing import Dict

from pandas import DataFrame

from application.web_graphs.formatters.heat_map_formatter import HeatMapFormatter
from application.web_graphs.formatters.histrogram_formatter import HistogramFormatter
from application.web_graphs.formatters.pie_chart_formatter import PieChartFormatter
from domain.excpetions.web_graphs_exceptions import WebGraphsGenralException, InvalidLabelName
from domain.models.web_graph_output_object import WebGraphsOutputObject
from application.web_graphs.models.web_graphs_types import WebGraphsTypes
from domain.contracts.abstract_web_graphs_formatter import AbstractWebGraphsFormatter
from domain.models.web_graphs_parameters import WebGraphsParameters


class WebGraphService:

    def __init__(self):

        self.web_graphs_instances: Dict[str, AbstractWebGraphsFormatter] = dict()
        self.web_graphs_mappings: Dict[str, AbstractWebGraphsFormatter] = dict()
        self._initialize_mappings()

    def _initialize_mappings(self) -> None:
        self.web_graphs_mappings = {
            WebGraphsTypes.heat_map.value: HeatMapFormatter,
            WebGraphsTypes.pie_chart.value: PieChartFormatter,
            WebGraphsTypes.histogram.value: HistogramFormatter
        }

    def _get_web_graphs_instance(self, graph_name: str) -> AbstractWebGraphsFormatter:
        if graph_name in self.web_graphs_instances.keys():
            return self.web_graphs_instances.get(graph_name)
        else:
            web_graphs_instance: AbstractWebGraphsFormatter = self.web_graphs_mappings.get(graph_name)()
            self.web_graphs_instances[graph_name] = web_graphs_instance
            return web_graphs_instance

    def get_web_graphs_data(self, linkages_df: DataFrame,
                            web_graphs_parameters: WebGraphsParameters) -> WebGraphsOutputObject:
        try:
            if web_graphs_parameters.label_name is None:
                return self._get_web_graphs_instance(web_graphs_parameters.graph_name).get_general_output(
                    linkages_df=linkages_df, web_graphs_parameters=web_graphs_parameters)
            else:
                return self._get_web_graphs_instance(web_graphs_parameters.graph_name).get_per_label_output(
                    linkages_df=linkages_df, web_graphs_parameters=web_graphs_parameters)
        except InvalidLabelName:
            raise InvalidLabelName
        except Exception as e:
            raise WebGraphsGenralException(message=e.__str__())
