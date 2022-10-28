from typing import List

from fastapi import APIRouter, HTTPException, File, UploadFile

from containers import Services
from domain.contracts.abstract_datasets_fetching_service import AbstractDatasetsFetchingService
from domain.excpetions.application_error import ApplicationError
from domain.models.dataset_information import DatasetInformation

datasets_fetching_service: AbstractDatasetsFetchingService = Services.datasets_fetching_service()

dataset_archive_extraction_service = Services.dataset_archive_extracting_service()

router = APIRouter()


@router.get("/", response_model=List[DatasetInformation])
async def get_datasets() -> List[DatasetInformation]:
    try:
        return datasets_fetching_service.get_datasets()
    except ApplicationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())


@router.post("/upload", response_model=DatasetInformation)
async def upload_dataset(dataset: UploadFile = File(...)) -> DatasetInformation:
    try:
        return dataset_archive_extraction_service.extract_dataset_archive(dataset.filename, dataset.file)
    except ApplicationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())
