import pandas as pd
from pandas import DataFrame
from typing import List, Dict

from domain.models.linkage_type import LinkageType
from domain.contracts.abstract_classification_linkage_service import AbstractClassificationLinkageService
from domain.models.linkage_object import LinkageObject


class ImageClassificationLinkageService(AbstractClassificationLinkageService):

    def get_classification_linkage_result(self, ground_truths: DataFrame, predictions: DataFrame) -> DataFrame:

        classification_linkage_list: List[Dict] = []

        for prediction_index, prediction_row in predictions.iterrows():

            image_path: str = prediction_row["image_path"]
            gt_label: str = ground_truths.loc[ground_truths["image_path"] == image_path, "class_name"].to_list()[0]
            pred_label: str = prediction_row["class_name"]
            confidence: float = prediction_row["confidence"]

            if gt_label == pred_label:
                linkage_type: str = LinkageType.true_positive.value

            elif pred_label is None:
                linkage_type: str = LinkageType.false_negative.value

            elif gt_label != pred_label:
                linkage_type: str = LinkageType.false_positive.value

            classification_linkage_row: LinkageObject = LinkageObject(id=prediction_index, image_path=image_path,
                                                                      gt_label=gt_label,
                                                                      prediction_label=pred_label,
                                                                      confidence=confidence, linkage_type=linkage_type)
            classification_linkage_list.append(classification_linkage_row.dict())
        # todo adjust columns names
        return pd.DataFrame(classification_linkage_list, columns=['id','image_path', 'gt_label', 'prediction_label', 'confidence', 'linkage_type'])
