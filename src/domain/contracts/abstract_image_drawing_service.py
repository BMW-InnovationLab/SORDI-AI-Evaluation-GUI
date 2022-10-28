from abc import ABC, ABCMeta, abstractmethod
from typing import List

from pandas import DataFrame


class AbstractImageDrawingService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def draw_text_on_image(self, image_path: str, output_path: str, gt_label: str, predicted_label: str) -> None: raise NotImplementedError

    @abstractmethod
    def draw_bounding_box_on_image(self, image_path: str, image_output_path: str, gt_bbox_coordinates: List[DataFrame], pred_bbox_coordinates: List[DataFrame],
                                   include_legend: bool) -> None: raise NotImplementedError
