

from abc import abstractmethod, ABC, ABCMeta
from pandas import DataFrame

from domain.models.web_graph_output_object import WebGraphsOutputObject
from domain.models.web_graphs_parameters import WebGraphsParameters


class AbstractWebGraphService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_web_graphs_data(self, linkages_df: DataFrame, web_graphs_parameters: WebGraphsParameters) -> WebGraphsOutputObject:raise NotImplementedError
