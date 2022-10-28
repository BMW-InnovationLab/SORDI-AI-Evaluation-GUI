from typing import List

from fastapi import APIRouter, HTTPException, BackgroundTasks
from starlette.responses import Response

from containers import Managers, Services
from domain.contracts.abstract_job_metric_manager import AbstractJobMetricManager
from domain.excpetions.application_error import ApplicationError
from domain.models.dataset_parameters import DatasetParameters
from domain.models.evaluation_job_parameters import EvaluationJobParameters
from domain.models.job_status_object import JobStatusObject
from domain.models.metric_result import MetricResult

evaluation_pipeline_manager = Managers.evaluation_pipeline_manager()

jobs_details_service = Services.jobs_details_service()
results_storage_service = Services.results_storage_service()

labels_retrieval_service = Services.labels_retrieval_service()
batch_size_validator = Services.batch_size_validation_service()
metrics_service: AbstractJobMetricManager = Managers.job_metric_manager()

router = APIRouter()


@router.post("/", response_model=EvaluationJobParameters)
async def run_evaluation_job(evaluation_job_parameters: EvaluationJobParameters,
                             background_tasks: BackgroundTasks) -> EvaluationJobParameters:
    try:
        evaluation_job_parameters = evaluation_pipeline_manager.check_evaluation_job_parameters(
            evaluation_job_parameters)
        background_tasks.add_task(evaluation_pipeline_manager.run_evaluation_job, evaluation_job_parameters)
        return evaluation_job_parameters

    except ApplicationError as e:

        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())


@router.get("/status", response_model=List[JobStatusObject])
async def get_jobs_statuses() -> List[JobStatusObject]:
    try:
        return jobs_details_service.get_jobs_statuses()
    except ApplicationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())


@router.get("/status/{uuid}", response_model=JobStatusObject)
async def get_job_statuses(uuid: str) -> JobStatusObject:
    try:
        return jobs_details_service.get_job_status(uuid)
    except ApplicationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())


@router.get("/parameters", response_model=EvaluationJobParameters)
async def get_job_parameters(uid: str) -> EvaluationJobParameters:
    try:
        return jobs_details_service.get_job_parameters(uid)
    except ApplicationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())


@router.post("/remove")
async def remove_job(uid: str) -> None:
    try:
        results_storage_service.delete_results(uid)
        jobs_details_service.delete_job_details(uid)
    except ApplicationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())


@router.get("/labels", response_model=List[str])
async def get_job_labels(uid: str) -> List[str]:
    try:
        return labels_retrieval_service.get_labels(uid)

    except ApplicationError as e:

        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())


@router.get("/validate/batch_size", response_model=List[str])
async def get_job_labels(dataset_parameters: DatasetParameters) -> Response:
    if batch_size_validator.check_dataset_valid(dataset_parameters): return Response(status_code=200)

    raise HTTPException(status_code=400, detail='Invalid batch size')


@router.get("/metrics/{uuid}")
async def get_job_statuses(uuid: str) -> List[MetricResult]:
    try:
        return metrics_service.get_metrics(uuid)
    except ApplicationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())


@router.get("/metrics/{uuid}/{label}")
async def get_job_statuses(uuid: str, label: str) -> List[MetricResult]:
    try:
        return metrics_service.get_metrics(uuid, label)
    except ApplicationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())
