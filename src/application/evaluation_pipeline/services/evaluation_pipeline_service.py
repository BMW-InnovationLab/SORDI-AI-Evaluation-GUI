from random import randint

from domain.contracts.abstract_evaluation_pipeline_service import AbstractEvaluationPipelineService
from domain.models.inference_retrieval_request_body import InferenceRetrievalRequestBody
from domain.models.evaluation_job_parameters import EvaluationJobParameters
from domain.models.inference_object import InferenceObject
from domain.models.evaluation_job_results import EvaluationJobResults
from domain.models.evaluation_job_details import EvaluationJobDetails
from domain.models.job_statuses import JobStatuses
from typing import List
from pandas import DataFrame
from shared.helpers.archive_helpers import create_archive
import time
from domain.models.linkage_job_result import LinkageJobResult
import pandas as pd

class EvaluationPipelineService(AbstractEvaluationPipelineService):

    def __init__(self, inference_retrieval_service, formatting_service_factory, dataset_preparation_service,
                 results_storage_service, results_retrieval_service, jobs_details_service, calculation_service,
                 output_folder_creation_service,
                 error_images_service, output_graphs_service, output_image_service,excel_service,web_images_extraction_service):
        self.inference_retrieval_service = inference_retrieval_service
        self.formatting_service_factory = formatting_service_factory
        self.dataset_preparation_service = dataset_preparation_service
        self.results_storage_service = results_storage_service
        self.web_images_extraction_service = web_images_extraction_service
        self.results_retrieval_service = results_retrieval_service
        self.jobs_details_service = jobs_details_service
        self.calculation_service = calculation_service
        self.output_folder_creation_service = output_folder_creation_service
        self.error_images_service = error_images_service
        self.output_graph_service = output_graphs_service
        self.output_image_service = output_image_service
        self.excel_service =excel_service

    def run_evaluation_pipeline(self, evaluation_job_parameters: EvaluationJobParameters) -> None:
        evaluation_job_details: EvaluationJobDetails = EvaluationJobDetails(
            status=JobStatuses.in_progress.value,
            parameters=evaluation_job_parameters
        )

        self.jobs_details_service.set_job_status(evaluation_job_details)

        ground_truths: List[InferenceObject] = self.dataset_preparation_service.get_ground_truths(
            evaluation_job_parameters)

        self.results_storage_service.save_ground_truths(evaluation_job_parameters.uid, ground_truths)

        output_folder: str = self.output_folder_creation_service.create_output_folder(evaluation_job_parameters)

        ground_truths_df: DataFrame = self.results_retrieval_service.get_results(
            evaluation_job_parameters.uid).ground_truths

        images: List[str] = ground_truths_df['image_path'].unique().tolist()

        batch_index: int = 0
        dataset_size: int = len(images)
        batch_image_paths = []
        while len(images) != 0:
            image = images[0]
            images.remove(image)
            batch_index += 1
            batch_image_paths.append(image)
            try:
                inference_retrieval_request_body: InferenceRetrievalRequestBody = InferenceRetrievalRequestBody(
                    url=evaluation_job_parameters.url,
                    model_name=evaluation_job_parameters.model_name,
                    image_path=image
                )

                response = self.inference_retrieval_service.get_inference(inference_retrieval_request_body)

                response = self.formatting_service_factory.get_instance(
                    evaluation_job_parameters).get_inference_objects_list(response, image)

                self.results_storage_service.save_predictions(evaluation_job_parameters.uid, response)

            except:
                self.error_images_service.save_error_image(image, output_folder)

            # update progress:
            evaluation_job_details.progress = int((batch_index / (dataset_size + 1)) * 100)
            self.jobs_details_service.set_job_status(evaluation_job_details)

            if batch_index % evaluation_job_parameters.batch_size == 0 or len(images) == 0:
                batch_results: EvaluationJobResults = self.results_retrieval_service.get_results(
                    evaluation_job_parameters.uid)
                batch_linkage_result = LinkageJobResult()
                batch_linkage_result.linkage_df = self.calculation_service.generate_linkage_results(
                    evaluation_result=batch_results,
                    evaluation_job_parameters=evaluation_job_parameters
                )
                if batch_linkage_result.linkage_df is not None and batch_linkage_result.linkage_df.empty is False:
                    batch_results.base_linkages = pd.concat(
                        [batch_results.base_linkages, batch_linkage_result.linkage_df],
                        ignore_index=True)
                results: EvaluationJobResults = self.results_retrieval_service.get_results(
                    evaluation_job_parameters.uid)
                results.linkages_by_iou = self.calculation_service.calculate(evaluation_result=results,
                                                                             iou_threshold=evaluation_job_parameters.iou_threshold,
                                                                             evaluation_job_parameters=evaluation_job_parameters,
                                                                             linkage_job_result=batch_linkage_result)
                self.results_storage_service.save_linkages(evaluation_job_parameters.uid, results.linkages_by_iou)

                self.web_images_extraction_service.extract_web_images(evaluation_job_results=results,
                                                                      evaluation_job_parameters=evaluation_job_parameters)
                batch_image_paths = []

        if results.linkages_by_iou.empty is False:
            time.sleep(10)
            self.output_graph_service.plot(linkages_df=results.linkages_by_iou, output_dir=output_folder,
                                           evaluation_job_parameters=evaluation_job_parameters)

            self.excel_service.create_excel_file(linkages_df=results.linkages_by_iou, prediction_df=results.predictions,
                                                 gt_df=results.ground_truths,
                                                 evaluation_job_parameter=evaluation_job_parameters,
                                                 output_path=output_folder)
            self.output_image_service.get_output_images(evaluation_job_results=results, output_path=output_folder,
                                                        evaluation_job_parameters=evaluation_job_parameters)

            create_archive(output_folder, evaluation_job_parameters.uid, "../servable")
            evaluation_job_details.status = JobStatuses.done.value
            evaluation_job_details.progress = 100
            self.jobs_details_service.set_job_status(evaluation_job_details)

