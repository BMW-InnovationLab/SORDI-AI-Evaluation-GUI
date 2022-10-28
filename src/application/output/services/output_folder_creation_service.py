import os
from typing import List
from domain.contracts.abstract_output_folder_creation_service import AbstractOutputFolderCreationService
from domain.models.evaluation_job_parameters import EvaluationJobParameters
from shared.helpers.filename_helpers import get_name_with_timestamp
class OutputFolderCreationService(AbstractOutputFolderCreationService):

    def __init__(self, labels_retrieval_service):
        self.labels_retrieval_service = labels_retrieval_service


    def create_output_folder(self, evaluation_job_parameters:EvaluationJobParameters) -> str:
        
        output_folder_name: str = get_name_with_timestamp(evaluation_job_parameters.job_name)
        output_folder_path: str = os.path.join("../output", output_folder_name)
        os.makedirs(output_folder_path)

        os.makedirs(os.path.join(output_folder_path, "03-Error Images"))

        os.makedirs(os.path.join(output_folder_path, "01-General Evaluation"))

        classes_folder: str = os.path.join(output_folder_path, "02-Specific Per Label Evaluation")

        os.makedirs(classes_folder)

        labels: List[str] = self.labels_retrieval_service.get_labels(evaluation_job_parameters.uid)

        for label in labels:
            os.makedirs(os.path.join(classes_folder, label))

            if evaluation_job_parameters.job_type == "object_detection":
                os.makedirs(os.path.join(classes_folder, label ,"plots"))
                os.makedirs(os.path.join(classes_folder, label, "bounding_boxes"))


        return output_folder_path