from dependency_injector import providers, containers

from application.calculation.calculation_service import CalculationService
from application.dataset_archive_extraction.services.dataset_archive_extraction_service import \
    DatasetArchiveExtractionService
from application.dataset_preparation.services.dataset_preparation_service import DatasetPreparationService
from application.dataset_validation.services.dataset_validation_service import DatasetValidationService
from application.dataset_validation.validators.batch_size_validator import BatchSizeValidator
from application.datasets_fetching.services.datasets_fetching_service import DatasetsFetchingService
from application.evaluation_pipeline.evaluation_pipeline_manager import EvaluationPipelineManager
from application.evaluation_pipeline.services.evaluation_pipeline_service import EvaluationPipelineService
from application.excel_service.excelService import ExcelService
from application.image_drawing_service.services.image_drawing_service import ImageDrawingService
from application.inference_api_client.services.inference_retrieval_service import InferenceRetrievalService
from application.inference_api_client.services.models_discovery_service import ModelsDiscoveryService
from application.inference_api_client.services.testing_url_validity_service import TestingUrlValidityService
from application.inference_services.inference_services_manager import InferenceServicesManager
from application.inference_services.services.inference_service_details_creator_service import \
    InferenceServiceDetailsCreatorService
from application.jobs_details.services.jobs_details_service import JobsDetailsService
from application.metrics.job_metric_manager import JobMetricManager
from application.output.services.error_images_service import ErrorImagesService
from application.output.services.output_folder_creation_service import OutputFolderCreationService
from application.output_graphs.services.output_graphs_service import OutputGraphsService
from application.output_images.services.output_image_service import OutputImageService
from application.results.services.labels_retrieval_service import LabelsRetrievalService
from application.results.services.results_retrieval_service import ResultsRetrievalService
from application.results.services.results_storage_service import ResultsStorageService
from application.web_graphs.services.web_graph_service import WebGraphService
from application.web_images_extraction.services.web_images_extraction_service import WebImagesExtractionService
from domain.contracts.abstract_calculation_service import AbstractCalculationService
from domain.contracts.abstract_dataset_archive_extraction_service import AbstractDatasetArchiveExtractionService
from domain.contracts.abstract_dataset_preparartion_service import AbstractDatasetPreparationService
from domain.contracts.abstract_dataset_validaton_service import AbstractDatasetValidationService
from domain.contracts.abstract_dataset_validator import AbstractDatasetValidator
from domain.contracts.abstract_datasets_fetching_service import AbstractDatasetsFetchingService
from domain.contracts.abstract_error_images_service import AbstractErrorImagesService
from domain.contracts.abstract_evaluation_pipeline_service import AbstractEvaluationPipelineService
from domain.contracts.abstract_image_drawing_service import AbstractImageDrawingService
from domain.contracts.abstract_inference_retrieval_service import AbstractInferenceRetrievalService
from domain.contracts.abstract_inference_service_details_creator_service import \
    AbstractInferenceServiceDetailsCreatorService
from domain.contracts.abstract_job_metric_manager import AbstractJobMetricManager
from domain.contracts.abstract_jobs_details_service import AbstractJobsDetailsService
from domain.contracts.abstract_labels_retrieval_service import AbstractLabelsRetrievalService
from domain.contracts.abstract_models_discovery_service import AbstractModelsDiscoveryService
from domain.contracts.abstract_output_folder_creation_service import AbstractOutputFolderCreationService
from domain.contracts.abstract_output_graphs_service import AbstractOutputGraphsService
from domain.contracts.abstract_results_retrieval_service import AbstractResultsRetrievalService
from domain.contracts.abstract_results_storage_service import AbstractResultsStorageService
from domain.contracts.abstract_testing_url_validity_service import AbstractTestingUrlValidityService
from domain.contracts.abstract_web_graph_service import AbstractWebGraphService
from persistance.contracts.abstract_dataset_repository import AbstractDatasetRepository
from persistance.contracts.abstract_inference_services_repository import AbstractInferenceServicesRepository
from persistance.contracts.abstract_jobs_details_repository import AbstractJobsDetailsRepository
from persistance.contracts.abstract_path_service import AbstractPathService
from persistance.contracts.abstract_results_repository import AbstractResultsRepository
from persistance.repositories.dataset_repository import DatasetRepository
from persistance.repositories.inference_services_repository import InferenceServicesRepository
from persistance.repositories.jobs_details_repository import JobsDetailsRepository
from persistance.repositories.results_repository import ResultsRepository
from persistance.services.path_service import PathService
from shared.services.fomatting_service_factory import FormattingServiceFactory


class Repositories(containers.DeclarativeContainer):
    paths_service = providers.Singleton(AbstractPathService.register(PathService))
    dataset_repo = providers.Factory(AbstractDatasetRepository.register(DatasetRepository), paths_service=paths_service)

    inference_services_repository = providers.Factory(
        AbstractInferenceServicesRepository.register(InferenceServicesRepository),
        paths_service=paths_service)

    results_repository = providers.Singleton(AbstractResultsRepository.register(ResultsRepository))

    jobs_details_repository = providers.Singleton(AbstractJobsDetailsRepository.register(JobsDetailsRepository))


class Factories(containers.DeclarativeContainer):
    formatting_service_factory = providers.Factory(FormattingServiceFactory)


class CalculationManager(containers.DeclarativeContainer):
    calculation_service = providers.Factory(AbstractCalculationService.register(CalculationService))


class Services(containers.DeclarativeContainer):
    testing_url_validity_service = providers.Factory(
        AbstractTestingUrlValidityService.register(TestingUrlValidityService))

    models_discovery_service = providers.Factory(AbstractModelsDiscoveryService.register(ModelsDiscoveryService))

    inference_service_details_creator_service = providers.Factory(
        AbstractInferenceServiceDetailsCreatorService.register(InferenceServiceDetailsCreatorService),
        models_discovery_service=models_discovery_service()
    )

    results_retrieval_service = providers.Factory(
        AbstractResultsRetrievalService.register(ResultsRetrievalService),
        results_repository=Repositories.results_repository()
    )

    results_storage_service = providers.Factory(
        AbstractResultsStorageService.register(ResultsStorageService),
        results_retrieval_service=results_retrieval_service(),
        results_repository=Repositories.results_repository()
    )

    inference_retrieval_service = providers.Factory(
        AbstractInferenceRetrievalService.register(InferenceRetrievalService)
    )

    dataset_preparation_service = providers.Factory(
        AbstractDatasetPreparationService.register(DatasetPreparationService)
    )

    jobs_details_service = providers.Factory(AbstractJobsDetailsService.register(JobsDetailsService),
                                             jobs_details_repository=Repositories.jobs_details_repository()
                                             )

    labels_retrieval_service = providers.Factory(AbstractLabelsRetrievalService.register(LabelsRetrievalService),
                                                 results_retrieval_service=results_retrieval_service()
                                                 )

    output_folder_creation_service = providers.Factory(
        AbstractOutputFolderCreationService.register(OutputFolderCreationService),
        labels_retrieval_service=labels_retrieval_service()
    )

    error_images_service = providers.Factory(AbstractErrorImagesService.register(ErrorImagesService))

    image_drawing_service = providers.Factory(AbstractImageDrawingService.register(ImageDrawingService))

    output_graphs_service = providers.Factory(AbstractOutputGraphsService.register(OutputGraphsService))

    output_image_service = providers.Factory(OutputImageService, image_drawing_service=image_drawing_service)
    web_images_extraction_service = providers.Factory(WebImagesExtractionService,
                                                      image_drawing_service=image_drawing_service)
    excel_service = providers.Factory(ExcelService)

    evaluation_pipeline_service = providers.Factory(
        AbstractEvaluationPipelineService.register(EvaluationPipelineService),
        inference_retrieval_service=inference_retrieval_service(),
        dataset_preparation_service=dataset_preparation_service(),
        results_storage_service=results_storage_service(),
        results_retrieval_service=results_retrieval_service(),
        formatting_service_factory=Factories.formatting_service_factory(),
        jobs_details_service=jobs_details_service(),
        calculation_service=CalculationManager.calculation_service(),
        error_images_service=error_images_service(),
        output_folder_creation_service=output_folder_creation_service(),
        output_graphs_service=output_graphs_service(),
        output_image_service=output_image_service(),
        web_images_extraction_service=web_images_extraction_service(),
        excel_service=excel_service()
    )

    dataset_validaton_service = providers.Factory(AbstractDatasetValidationService.register(DatasetValidationService))

    batch_size_validation_service = providers.Factory(AbstractDatasetValidator.register(BatchSizeValidator))

    web_graph_service = providers.Factory(AbstractWebGraphService.register(WebGraphService))

    datasets_fetching_service = providers.Factory(AbstractDatasetsFetchingService.register(DatasetsFetchingService),
                                                  dataset_repository=Repositories.dataset_repo)

    dataset_archive_extracting_service = providers.Factory(
        AbstractDatasetArchiveExtractionService.register(DatasetArchiveExtractionService),
        dataset_validator=dataset_validaton_service)


class Managers(containers.DeclarativeContainer):
    job_metric_manager = providers.Factory(AbstractJobMetricManager.register(JobMetricManager),
                                           job_details_service=Services.jobs_details_service,
                                           label_service=Services.labels_retrieval_service,
                                           results_retrieval_service=Services.results_retrieval_service)

    inference_services_manager = providers.Factory(
        InferenceServicesManager,
        testing_url_validity_service=Services.testing_url_validity_service(),
        inference_service_details_creator_service=Services.inference_service_details_creator_service(),
        inference_services_repository=Repositories.inference_services_repository()
    )

    evaluation_pipeline_manager = providers.Factory(
        EvaluationPipelineManager,
        dataset_validation_service=Services.dataset_validaton_service(),
        models_discovery_service=Services.models_discovery_service(),
        testing_url_validity_service=Services.testing_url_validity_service(),
        evaluation_pipeline_service=Services.evaluation_pipeline_service(),
    )
