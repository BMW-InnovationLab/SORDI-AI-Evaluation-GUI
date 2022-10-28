import random
from typing import List

from pandas import DataFrame
import os
from domain.models.linkage_type import LinkageType

from domain.contracts.abstract_image_drawing_service import AbstractImageDrawingService
from domain.contracts.abstract_web_images_service import AbstractWebImagesService


class ImageClassificationWebImagesService(AbstractWebImagesService):
    def __init__(self, image_drawing_service: AbstractImageDrawingService):
        self.image_drawing_service: AbstractImageDrawingService = image_drawing_service

    def get_per_class_sample_images(self, linkages_df: DataFrame, gt_df: DataFrame, predictions_df: DataFrame, servable_path: str) -> None:
        classes_list = list(set(linkages_df.gt_label))

        for class_name in classes_list:
            linkages_indexes: List[int] = linkages_df.loc[
                (linkages_df.linkage_type.isin([LinkageType.true_positive.value, LinkageType.false_positive.value])) & (
                            linkages_df.gt_label == class_name)].index.tolist()
            image_indexes: List[int] = [random.choice(linkages_indexes) for i in range(0, 3)]
            random_df: DataFrame = linkages_df.loc[linkages_df.index.isin(image_indexes), ["image_path", "gt_label", "prediction_label"]]
            for index, (row_index, row_info) in enumerate(random_df.iterrows()):
                output_path: str = os.path.join(servable_path, class_name)
                if not os.path.isdir(output_path):
                    os.makedirs(output_path)
                image_output_path: str = os.path.join(output_path, str(index + 1) + '.png')
                self.image_drawing_service.draw_text_on_image(image_path=row_info.image_path, output_path=image_output_path, gt_label=row_info.gt_label,
                                                              predicted_label=row_info.prediction_label)

    def get_sample_images(self, linkages_df: DataFrame, gt_df: DataFrame, predictions_df: DataFrame, servable_path: str) -> None:
        linkages_indexes: List[int] = linkages_df.loc[linkages_df.linkage_type.isin([LinkageType.true_positive.value,
                                                                                     LinkageType.false_positive.value])].index.tolist()
        image_indexes: List[int] = [random.choice(linkages_indexes) for i in range(0, 3)]
        random_df: DataFrame = linkages_df.loc[linkages_df.index.isin(image_indexes), ["image_path", "gt_label", "prediction_label"]]

        for index, (row_index, row_info) in enumerate(random_df.iterrows()):
            image_output_path: str = os.path.join(servable_path, str(index + 1) + '.png')
            self.image_drawing_service.draw_text_on_image(image_path=row_info.image_path, output_path=image_output_path, gt_label=row_info.gt_label,
                                                          predicted_label=row_info.prediction_label)
