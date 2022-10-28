from pathlib import Path
from typing import List
import random
from domain.contracts.abstract_output_image_service import AbstractOutputImageService
from domain.models.linkage_type import LinkageType
from PIL import Image, ImageDraw, ImageFont
import os

from pandas import DataFrame

from domain.contracts.abstract_image_drawing_service import AbstractImageDrawingService


class ObjectDetectionOutputImageService(AbstractOutputImageService):
    def __init__(self, image_drawing_service: AbstractImageDrawingService):
        self.font = ImageFont.truetype('../data/DejaVuSans.ttf', 15)
        self.image_drawing_service: AbstractImageDrawingService = image_drawing_service



    def _draw_wrong_case_image(self, linkages_df, predictions_df: DataFrame, output_path: str) -> None:
        linkages_grouped = linkages_df.groupby(['image_path'])
        if not os.path.exists(os.path.join(output_path, 'predictions only')):
            os.makedirs(os.path.join(output_path, 'predictions only'))

        for image_name, group_df in linkages_grouped:
            image_output_path: str = os.path.join(output_path, 'predictions only', 'bb_' + str(os.path.splitext(Path(image_name).name)[0] + '.png'))

            prediction_only_indexes: List[List[int]] = group_df.loc[
                (group_df.linkage_type == LinkageType.false_positive.value) & (group_df.gt_label.isnull()), "prediction_index"].values.tolist()
            if len(prediction_only_indexes) == 0:
                continue
            predictions_bbox_coordinates: List[DataFrame] = [predictions_df.loc[predictions_df.index == i, ['left', 'top', 'right', 'bottom', 'class_name']] for
                                                             i in prediction_only_indexes]

            image = Image.open(image_name)
            draw = ImageDraw.Draw(image)
            for pred_bbox in predictions_bbox_coordinates:
                draw.rectangle([pred_bbox.left, pred_bbox.top, pred_bbox.right, pred_bbox.bottom], outline="red", width=3)
                pred_label: str = "Predicted: " + str(pred_bbox.class_name.values[0])
                draw.text((int(pred_bbox.left), int(pred_bbox.top) - 20), str(pred_label), 'red', font=self.font)
            if len(predictions_bbox_coordinates) > 0:
                image.save(image_output_path, 'PNG')

    def _draw_true_case_image(self, linkages_df: DataFrame, gt_df: DataFrame, predictions_df: DataFrame, output_path: str) -> None:

        linkages_grouped = linkages_df.groupby(['image_path', 'gt_label'])
        try:
            for name, group_df in linkages_grouped:
                image_output_path: str = os.path.join(output_path, str(name[1]), 'bounding_boxes',
                                                      'bb_' + str(os.path.splitext(Path(name[0]).name)[0] + '.png'))

                gt_prediction_indexes: List[List[int]] = group_df.loc[
                    (group_df.linkage_type != LinkageType.true_negative.value) & (group_df.gt_label.notnull()), ["gt_index",
                                                                                                                 "prediction_index"]].values.tolist()
                pred_bbox_coordinates: List[DataFrame] = [predictions_df.loc[predictions_df.index == i[1], ['left', 'top', 'right', 'bottom']] for i in
                                                          gt_prediction_indexes]
                gt_bbox_coordinates: List[DataFrame] = [gt_df.loc[gt_df.index == i[0], ['left', 'top', 'right', 'bottom']] for i in gt_prediction_indexes]
                #  remove empty dataframe so they don't cause error when drawing
                pred_bbox_coordinates: List[DataFrame] = [element for element in pred_bbox_coordinates if element.empty is False]

                self.image_drawing_service.draw_bounding_box_on_image(image_path=name[0], image_output_path=image_output_path,
                                                                      gt_bbox_coordinates=gt_bbox_coordinates,
                                                                      pred_bbox_coordinates=pred_bbox_coordinates, include_legend=True)

        except Exception as e:
            raise e

    def get_output_images(self, linkages_df: DataFrame, gt_df: DataFrame, predictions_df: DataFrame, output_path: str) -> None:
        self._draw_true_case_image(linkages_df=linkages_df, gt_df=gt_df, predictions_df=predictions_df, output_path=output_path)
        self._draw_wrong_case_image(linkages_df=linkages_df, predictions_df=predictions_df, output_path=output_path)

