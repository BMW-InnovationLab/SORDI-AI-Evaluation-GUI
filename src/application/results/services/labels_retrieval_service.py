from typing import List
from pandas import DataFrame

from domain.contracts.abstract_labels_retrieval_service import AbstractLabelsRetrievalService
from domain.excpetions.validation_exceptions import InvalidJobId

class LabelsRetrievalService(AbstractLabelsRetrievalService):

    def __init__(self, results_retrieval_service):
        self.results_retrieval_serivce = results_retrieval_service

    def get_labels(self, uid:str) -> List[str]:
        ground_truths: DataFrame = self.results_retrieval_serivce.get_results(uid).ground_truths

        try:
            return ground_truths.loc[ground_truths['class_name'].notnull(),'class_name'].unique().tolist()

        except KeyError:
            raise InvalidJobId
