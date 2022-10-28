import os
from typing import List, Dict

from pandas import DataFrame
import pandas as pd
import numpy

from application.excel_service.formatters.image_classification_excel_formatter import ImageClassificationExcelFormatter
from application.excel_service.formatters.object_detection_excel_formatter import ObjectDetectionExcelFormatter
from application.excel_service.models.excel_formatter_type import ExcelFormatterType
from application.excel_service.models.linkage_definition import LinkageDefinition
from application.output_images.services.object_detection_output_image_service import ObjectDetectionOutputImageService
from domain.contracts.abstract_excel_formatter import AbstractExcelFormatter
from domain.models.evaluation_job_parameters import EvaluationJobParameters


class ExcelService():

    def __init__(self):

        self.excel_formatter_instances: Dict[str, AbstractExcelFormatter] = dict()
        self.excel_formatter_mappings: Dict[str, AbstractExcelFormatter] = dict()
        self._initialize_mappings()

    def _initialize_mappings(self) -> None:
        self.excel_formatter_mappings = {
            ExcelFormatterType.image_classification.value: ImageClassificationExcelFormatter,
            ExcelFormatterType.object_detection.value: ObjectDetectionExcelFormatter
        }


    def _get_excel_formatter_instance(self, job_type: str) -> AbstractExcelFormatter:
        if job_type in self.excel_formatter_instances.keys():
            return self.excel_formatter_instances.get(job_type)
        else:
            excel_formatter_instance: AbstractExcelFormatter = self.excel_formatter_mappings.get(job_type)()
            self.excel_formatter_instances[job_type] = excel_formatter_instance
            return excel_formatter_instance


    def get_image_classification_detailed_df(self,linkages_df: DataFrame):
        all_data = linkages_df[['image_path', 'gt_label', 'prediction_label', 'confidence', 'linkage_type']].copy()
        all_data = all_data[['image_path', 'gt_label', 'prediction_label', 'linkage_type', 'confidence']]
        all_data.linkage_type = all_data.linkage_type.apply(lambda x: LinkageDefinition[x].value)
        all_data.sort_values('image_path', inplace=True)
        all_data.reset_index(drop=True, inplace=True)


    def get_object_detection_detailed_df(self, linkages_df: DataFrame, prediction_df: DataFrame, gt_df: DataFrame) -> DataFrame:
        all_df: DataFrame = linkages_df.copy()
        all_gt_index: List[int] = all_df.gt_index.tolist()
        all_pred_index: List[int] = all_df.prediction_index.tolist()

        gt_bbox = gt_df.loc[gt_df.index.isin(all_gt_index), ['left', 'right', 'top', 'bottom']].rename(columns={'left': 'gt_left', 'right': 'gt_right', 'top': 'gt_top', "bottom": "gt_bottom"})
        pred_bbox = prediction_df.loc[prediction_df.index.isin(all_pred_index), ['left', 'right', 'top', 'bottom']].rename(columns={'left': 'pred_left', 'right': 'pred_right', 'top': 'pred_top', "bottom": "pred_bottom"})

        df_all_cols = pd.concat([all_df, gt_bbox, pred_bbox], axis=1)
        df_all_cols.drop(['id'], axis=1, inplace=True)
        df_all_cols.drop(['gt_index', 'prediction_index'], axis=1, inplace=True)

        df_all_cols = df_all_cols[['image_path', 'gt_label', 'prediction_label', 'linkage_type', 'iou', 'ecludien_distance', 'confidence', 'gt_centroid', 'prediction_centroid','gt_left', 'gt_right', 'gt_top', 'gt_bottom', 'pred_left', 'pred_right', 'pred_top', 'pred_bottom']]
        df_all_cols.image_path = df_all_cols.image_path.apply(lambda x: os.path.basename(x))
        df_all_cols.linkage_type = df_all_cols.linkage_type.apply(lambda x: LinkageDefinition[x].value)

        df_all_cols[['iou', 'ed', 'conf']] = df_all_cols[['iou', 'ecludien_distance', 'confidence']].astype(float).round(2)
        df_all_cols.fillna(value='--', inplace=True)
        df_all_cols.sort_values('image_path', inplace=True)
        df_all_cols.reset_index(drop=True, inplace=True)

        return df_all_cols

    def create_excel_file(self, linkages_df: DataFrame, prediction_df: DataFrame, gt_df: DataFrame,
                          evaluation_job_parameter: EvaluationJobParameters, output_path: str):
        output_path = os.path.join(output_path,'01-General Evaluation')
        self._get_excel_formatter_instance(evaluation_job_parameter.job_type).create_report(
            linkages_df=linkages_df, gt_df=gt_df,
            prediction_df=prediction_df,evaluation_job_parameter=evaluation_job_parameter,
            output_path=output_path)
