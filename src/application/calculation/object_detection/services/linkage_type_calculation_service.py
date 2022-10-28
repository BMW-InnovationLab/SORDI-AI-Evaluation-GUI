import math
from typing import Set, List
import pandas as pd
from pandas import DataFrame

from domain.contracts.abstract_linkage_type_calculation_service import AbstractLinkageTypeCalculationService
from domain.models.linkage_object import LinkageObject
from domain.models.linkage_type import LinkageType


class LinkageTypeCalculationService(AbstractLinkageTypeCalculationService):

    def get_true_negative_case(self, linkage_df: DataFrame, ground_truths: DataFrame, predictions_df: DataFrame,
                               linkage_type: str) -> DataFrame:
        empty_gt_images: Set[str] = set(ground_truths[ground_truths['class_name'].isnull()]["image_path"].to_list())
        empty_prediction_images: Set[str] = set(
            predictions_df[predictions_df["class_name"].isnull()]["image_path"].to_list())
        empty_images_intersection: List[str] = list(empty_gt_images.intersection(empty_prediction_images))

        missing_linkages: List[LinkageObject] = []
        for image_name in empty_images_intersection:
            gt_image_occurrence: int = len(
                ground_truths.loc[ground_truths["image_path"] == image_name]["class_id"].isnull())
            prediction_image_occurrence: int = len(
                predictions_df.loc[predictions_df["image_path"] == image_name]["class_id"].isnull())

            if gt_image_occurrence == prediction_image_occurrence == 1:
                index: int = int(linkage_df["id"].max() + 1)
                linkage_row: LinkageObject = LinkageObject(id=index, image_path=image_name, linkage_type=linkage_type)
                missing_linkages.append(linkage_row)

        temp_df = DataFrame([linkage.__dict__ for linkage in missing_linkages])
        linkage_df = pd.concat([linkage_df, temp_df], ignore_index=True)
        del temp_df
        return linkage_df

    def get_false_negative_cases(self, linkage_df: DataFrame, ground_truths: DataFrame) -> DataFrame:
        all_ground_truths_index: Set[int] = set(ground_truths[ground_truths['class_name'].notnull()].index.to_list())
        all_linkage_ground_truths_index: Set[int] = set(linkage_df["gt_index"])

        missing_ground_truths_index: List[int] = list(all_ground_truths_index - all_linkage_ground_truths_index)
        missing_linkages: List[LinkageObject] = []
        for ground_truth_index in missing_ground_truths_index:
            index: int = int(linkage_df["id"].max() + 1)
            image_path: str = ground_truths.loc[ground_truths.index == ground_truth_index]["image_path"].to_list()[0]
            label: str = ground_truths.loc[ground_truths.index == ground_truth_index]["class_name"].to_list()[0]
            linkage_row: LinkageObject = LinkageObject(id=index,
                                                       image_path=image_path,
                                                       gt_index=ground_truth_index,
                                                       gt_label=label,
                                                       linkage_type=LinkageType.false_negative.value)
            missing_linkages.append(linkage_row)

        temp_df = DataFrame([linkage.__dict__ for linkage in missing_linkages])
        linkage_df = pd.concat([linkage_df, temp_df], ignore_index=True)
        del temp_df

        # Get ground truths index where a GT is associated with a prediction with a linkage type of FP
        ground_truths_index: Set[int] = set(linkage_df[(linkage_df['gt_label'].notnull()) & (linkage_df[
                                                                                                 'prediction_label'].notnull()) & (
                                                               linkage_df[
                                                                   'linkage_type'] == LinkageType.false_positive.value)].gt_index.to_list())

        # Get ground truths index that are not already associated with a linkage type of TP
        unassociated_ground_truths_index: Set[int] = set(
            linkage_df[(linkage_df["gt_index"].isin(ground_truths_index)) & (
                    linkage_df["linkage_type"] != LinkageType.true_positive.value)].gt_index.to_list())

        missing_linkages: List[LinkageObject] = []
        for ground_truth_index in unassociated_ground_truths_index:
            index: int = int(linkage_df["id"].max() + 1)
            image_path: str = ground_truths.loc[ground_truths.index == ground_truth_index]["image_path"].to_list()[0]
            label: str = ground_truths.loc[ground_truths.index == ground_truth_index]["class_name"].to_list()[0]
            linkage_row: LinkageObject = LinkageObject(id=index,
                                                       image_path=image_path,
                                                       gt_index=ground_truth_index,
                                                       gt_label=label,
                                                       linkage_type=LinkageType.false_negative.value)
            missing_linkages.append(linkage_row)

        temp_df = DataFrame([linkage.__dict__ for linkage in missing_linkages])
        linkage_df = pd.concat([linkage_df, temp_df], ignore_index=True)
        del temp_df
        return linkage_df

    def get_false_positive_cases(self, linkage_df: DataFrame, predictions_df: DataFrame) -> DataFrame:
        all_predictions_index: Set[int] = set(predictions_df[predictions_df['class_name'].notnull()].index.to_list())
        all_linkage_predictions_index: Set[int] = set(linkage_df["prediction_index"])

        missing_predictions_index: List[int] = list(all_predictions_index - all_linkage_predictions_index)
        missing_linkages: List[LinkageObject] = []

        for prediction_index in missing_predictions_index:
            index: int = int(linkage_df["id"].max() + 1) if not math.isnan(linkage_df["id"].max()) else 1
            image_path: str = predictions_df.loc[predictions_df.index == prediction_index]["image_path"].to_list()[0]
            label: str = predictions_df.loc[predictions_df.index == prediction_index]["class_name"].to_list()[0]
            linkage_row: LinkageObject = LinkageObject(id=index,
                                                       image_path=image_path,
                                                       prediction_index=prediction_index,
                                                       prediction_label=label,
                                                       linkage_type=LinkageType.false_positive.value)
            missing_linkages.append(linkage_row)

        temp_df = DataFrame([linkage.__dict__ for linkage in missing_linkages])
        linkage_df = pd.concat([linkage_df, temp_df], ignore_index=True)
        del temp_df
        return linkage_df
