from pandas import DataFrame
import pandas as pd
from domain.models.linkage_type import LinkageType
from domain.contracts.abstract_calculation_filter_service import AbstractCalculationFilterService


class CalculationFilterService(AbstractCalculationFilterService):

    def filter_same_labels(self, linkage_df: DataFrame) -> None:
        linkage_df.loc[
            linkage_df["gt_label"] != linkage_df["prediction_label"], "linkage_type"] = LinkageType.false_positive.value

    def check_iou_threshold(self, linkage_df: DataFrame, iou_threshold: float) -> None:
        linkage_df.loc[linkage_df["iou"] < iou_threshold, "linkage_type"] = LinkageType.false_positive.value
        linkage_df.loc[(linkage_df["iou"] >= iou_threshold) & (linkage_df[
                                                                   "linkage_type"] != LinkageType.false_positive.value), "linkage_type"] = LinkageType.true_positive.value

    def filter_overlapping_predictions(self, linkage_df: DataFrame) -> None:
        pd.reset_option('mode.chained_assignment')
        with pd.option_context('mode.chained_assignment', None):
            linkage_df.sort_values(by=['prediction_index', 'iou'], ascending=(True, False), inplace=True)
            linkage_df.drop_duplicates('prediction_index', inplace=True)
            linkage_df.sort_values(by=['gt_index', 'confidence'], ascending=(True, False), inplace=True)
            linkage_df.drop_duplicates('gt_index', inplace=True)
