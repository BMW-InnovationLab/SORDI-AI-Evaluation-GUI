from abc import ABC
from typing import Dict

from domain.contracts.abstract_job_metric_service import AbstractJobMetricService
from domain.models.linkage_type import LinkageType
from domain.models.metric_calculation_parameters import MetricsCalculationParameters


class BaseMetricLinkageType(AbstractJobMetricService, ABC):
    def get_linkage_type_result(self, calculation_parameters: MetricsCalculationParameters) \
            -> Dict[LinkageType, int]:
        res = self.get_general_linkage_type_result(
            calculation_parameters) \
            if calculation_parameters.per_label is None else \
            self.get_per_label_linkage_type_result(calculation_parameters)
        return res

    def get_general_linkage_type_result(self, calculation_parameters: MetricsCalculationParameters) \
            -> Dict[LinkageType, int]:
        prediction_linkage_results: Dict[LinkageType, int] = {
            linkage_type: (calculation_parameters.linkages_df.linkage_type.values == linkage_type.value).sum().tolist()
            for linkage_type in LinkageType}
        return prediction_linkage_results

    def get_per_label_linkage_type_result(self, calculation_parameters: MetricsCalculationParameters) \
            -> Dict[LinkageType, int]:
        prediction_linkage_results: Dict[LinkageType, int] = {
            linkage_type: int((calculation_parameters.linkages_df
                               .loc[(calculation_parameters.linkages_df["gt_label"] == calculation_parameters.per_label)
                                    | ((calculation_parameters.linkages_df.gt_label.isnull()) &
                                       (calculation_parameters.linkages_df[
                                            "prediction_label"] == calculation_parameters.per_label))]
                               .linkage_type.values == linkage_type.value).sum())
            for linkage_type in LinkageType}

        return prediction_linkage_results
