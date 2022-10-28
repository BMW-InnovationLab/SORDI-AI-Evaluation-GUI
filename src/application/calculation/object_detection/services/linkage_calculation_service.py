from typing import List, Dict

from pandas import DataFrame

from domain.contracts.abstract_linkage_calculation_service import AbstractLinkageCalculationService
from domain.models.bounding_box import BoundingBox
from domain.models.linkage_object import LinkageObject
from domain.models.linkage_type import LinkageType
from domain.models.evaluation_job_parameters import EvaluationJobParameters
from shared.helpers.calculation_helpers import get_bounding_box_info, get_iou, get_euclidean_distance


class LinkageCalculationService(AbstractLinkageCalculationService):

    def get_linkage_result(self, ground_truths_df: DataFrame, predictions_df: DataFrame,
                           evaluation_job_parameters: EvaluationJobParameters) -> DataFrame:
        linkage_list: List[Dict] = []
        index: int = 0
        pred_data_group = predictions_df.groupby(["image_path"])
        for image_path, grouped_df in pred_data_group:
            for index_pred, prediction in grouped_df.iterrows():
                if prediction["left"] is not None:

                    confidence: float = round(prediction["confidence"], 2)
                    prediction_bbox: BoundingBox = BoundingBox(left=prediction["left"], right=prediction["right"],
                                                               top=prediction["top"], bottom=prediction["bottom"])
                    prediction_bbox: BoundingBox = get_bounding_box_info(prediction_bbox)
                    # Multiply confidence threshold by 100 (Go from 0->1 to 0->100)
                    if prediction["confidence"] > evaluation_job_parameters.confidence_threshold * 100:
                        for index_gt, gt in ground_truths_df.loc[ground_truths_df.image_path == image_path].iterrows():
                            if gt["left"] is not None:
                                ground_truth_bbox: BoundingBox = BoundingBox(left=gt["left"], right=gt["right"],
                                                                             top=gt["top"],
                                                                             bottom=gt["bottom"])
                                ground_truth_bbox: BoundingBox = get_bounding_box_info(ground_truth_bbox)

                                iou: float = round(
                                    get_iou(gt_bounding_box=ground_truth_bbox, prediction_bounding_box=prediction_bbox),
                                    4)
                                euclidean_distance: float = round(
                                    get_euclidean_distance(gt_centroid=ground_truth_bbox.centroid,
                                                           prediction_centroid=prediction_bbox.centroid), 4)

                                if iou > 0:
                                    gt_prediction_linkage: LinkageObject = LinkageObject(id=index,
                                                                                         image_path=gt["image_path"],
                                                                                         gt_index=index_gt,
                                                                                         gt_label=gt["class_name"],
                                                                                         prediction_index=index_pred,
                                                                                         prediction_label=prediction[
                                                                                             "class_name"],
                                                                                         iou=iou,
                                                                                         ecludien_distance=float(euclidean_distance),
                                                                                         gt_centroid=ground_truth_bbox.centroid,
                                                                                         prediction_centroid=prediction_bbox.centroid,
                                                                                         confidence=confidence)
                                    index += 1
                                    linkage_list.append(gt_prediction_linkage.dict())
                    else:
                        low_confidence_linkage: LinkageObject = LinkageObject(id=index,
                                                                              image_path=prediction["image_path"],
                                                                              prediction_index=index_pred,
                                                                              prediction_label=prediction[
                                                                                  "class_name"],
                                                                              prediction_centroid=prediction_bbox.centroid,
                                                                              confidence=confidence,
                                                                              linkage_type=LinkageType.false_positive.value)
                        index += 1
                        linkage_list.append(low_confidence_linkage.dict())

        return DataFrame(linkage_list, columns=LinkageObject.__fields__)
