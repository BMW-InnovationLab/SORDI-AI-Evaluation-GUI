import os
import random
from typing import List

from pandas import DataFrame

from domain.models.linkage_type import LinkageType

from domain.contracts.abstract_image_drawing_service import AbstractImageDrawingService
from domain.contracts.abstract_web_images_service import AbstractWebImagesService


class ObjectDetectionWebImagesService(AbstractWebImagesService):
    def __init__(self, image_drawing_service: AbstractImageDrawingService):
        self.image_drawing_service: AbstractImageDrawingService = image_drawing_service

    def get_sample_images(self, linkages_df: DataFrame, gt_df: DataFrame, predictions_df: DataFrame, servable_path: str) -> None:
        image_indexes: List[str] = [random.choice(linkages_df.image_path.unique().tolist()) for i in range(0, 3)]
        sample_df: DataFrame = linkages_df[linkages_df.image_path.isin(image_indexes)]
        linkages_grouped = sample_df.groupby(['image_path'])
        try:
            for index, (name, group_df) in enumerate(linkages_grouped):
                image_output_path: str = os.path.join(servable_path, str(index + 1) + '.png')
                gt_prediction_indexes: List[List[int]] = group_df.loc[
                    (group_df.linkage_type != LinkageType.true_negative.value) & (group_df.gt_label.notnull()), ["gt_index",
                                                                                                                 "prediction_index"]].values.tolist()
                pred_bbox_coordinates: List[DataFrame] = [predictions_df.loc[predictions_df.index == i[1], ['left', 'top', 'right', 'bottom']] for i in
                                                          gt_prediction_indexes]
                gt_bbox_coordinates: List[DataFrame] = [gt_df.loc[gt_df.index == i[0], ['left', 'top', 'right', 'bottom']] for i in gt_prediction_indexes]
                #  remove empty dataframe so they don't cause error when drawing
                pred_bbox_coordinates: List[DataFrame] = [element for element in pred_bbox_coordinates if element.empty is False]

                self.image_drawing_service.draw_bounding_box_on_image(image_path=name, image_output_path=image_output_path,
                                                                      gt_bbox_coordinates=gt_bbox_coordinates,
                                                                      pred_bbox_coordinates=pred_bbox_coordinates, include_legend=False)

        except Exception as e:
            raise e

    def get_per_class_sample_images(self, linkages_df: DataFrame, gt_df: DataFrame, predictions_df: DataFrame, servable_path: str) -> None:
        gt_classes: List[str] = list(set(linkages_df.loc[linkages_df.gt_label.notnull()].gt_label))
        try:
            for class_name in gt_classes:

                images_list: List[str] = [random.choice(linkages_df.loc[linkages_df.gt_label == class_name].image_path.unique().tolist()) for i in range(0, 3)]
                selected_images_df: DataFrame = linkages_df.loc[
                    (linkages_df.image_path.isin(images_list)) & (linkages_df.gt_label == class_name), ['image_path', 'gt_index', 'prediction_index']]

                grouped_df = selected_images_df.groupby(['image_path'])
                for index, (image_path, group_df) in enumerate(grouped_df):
                    gt_bbox_coordinates: List[DataFrame] = [gt_df.loc[gt_df.index == i, ['left', 'top', 'right', 'bottom']] for i in group_df.gt_index.tolist()]
                    pred_bbox_coordinates: List[DataFrame] = [predictions_df.loc[predictions_df.index == i, ['left', 'top', 'right', 'bottom']] for i in
                                                              group_df.prediction_index.tolist()]
                    pred_bbox_coordinates: List[DataFrame] = [element for element in pred_bbox_coordinates if element.empty is False]

                    output_path: str = os.path.join(servable_path, class_name)
                    if not os.path.isdir(output_path):
                        os.makedirs(output_path)
                    output_path = os.path.join(output_path, str(index + 1) + '.png')
                    self.image_drawing_service.draw_bounding_box_on_image(image_path=image_path, image_output_path=output_path,
                                                                          gt_bbox_coordinates=gt_bbox_coordinates,
                                                                          pred_bbox_coordinates=pred_bbox_coordinates, include_legend=False)
        except Exception as e:
            raise e
