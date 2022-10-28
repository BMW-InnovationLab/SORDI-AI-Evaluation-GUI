from abc import abstractmethod, ABC, ABCMeta
from pandas import DataFrame

from domain.models.web_graph_output_object import WebGraphsOutputObject
from domain.models.web_graphs_parameters import WebGraphsParameters


class AbstractWebGraphsFormatter(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_general_output(self, linkages_df: DataFrame,web_graphs_parameters: WebGraphsParameters ) -> WebGraphsOutputObject: raise NotImplementedError

    @abstractmethod
    def get_per_label_output(self, linkages_df: DataFrame, web_graphs_parameters: WebGraphsParameters) -> WebGraphsOutputObject: raise NotImplementedError
