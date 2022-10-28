import os
from typing import List
from shutil import copy2
from pandas import DataFrame
from domain.contracts.abstract_output_image_service import AbstractOutputImageService
from domain.models.linkage_type import LinkageType

from domain.contracts.abstract_image_drawing_service import AbstractImageDrawingService


class ImageClassificationOutputImageService(AbstractOutputImageService):
    def __init__(self,image_drawing_service:AbstractImageDrawingService):
        self.image_drawing_service: AbstractImageDrawingService = image_drawing_service


    def get_output_images(self, linkages_df: DataFrame, gt_df: DataFrame, predictions_df: DataFrame,
                          output_path: str) -> None:
        all_label: List[str] = linkages_df.gt_label.unique()
        wrongly_classified_images: List[str] = linkages_df.loc[linkages_df.linkage_type == LinkageType.false_positive.value, "image_path",].values.tolist()
        not_classified_images: List[str] = linkages_df.loc[linkages_df.linkage_type == LinkageType.false_negative.value, "image_path"].values.tolist()

        if not os.path.isdir(os.path.join(output_path, 'Wrong_Classified_Images')) and len(wrongly_classified_images) > 0:
            os.makedirs(os.path.join(output_path, 'Wrong_Classified_Images'))
        if not os.path.isdir(os.path.join(output_path, 'Not_Classified_Images')) and len(not_classified_images) > 0:
            os.makedirs(os.path.join(output_path, 'Not_Classified_Images'))

        [copy2(image_path, os.path.join(output_path, 'Wrong_Classified_Images')) for image_path in wrongly_classified_images]
        [copy2(image_path, os.path.join(output_path, 'Not_Classified_Images')) for image_path in not_classified_images]

        for label in all_label:
            images_paths: List[str]= linkages_df.loc[(linkages_df.gt_label == label) & (linkages_df.linkage_type == LinkageType.true_positive.value), "image_path"].values.tolist()
            [copy2(image_path, os.path.join(output_path, label)) for image_path in images_paths]


