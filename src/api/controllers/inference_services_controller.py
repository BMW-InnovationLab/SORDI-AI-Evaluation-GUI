from fastapi import APIRouter, HTTPException
from containers import Managers
from domain.excpetions.application_error import ApplicationError

from domain.models.inference_service_request_body import InferenceServiceRequestBody
from domain.models.inference_service_details import InferenceServiceDetails

from typing import List

inference_services_manager = Managers.inference_services_manager()

router = APIRouter()


@router.get("/", response_model=List[InferenceServiceDetails])
async def get_inference_services() -> List[InferenceServiceDetails]:
    try:
        return inference_services_manager.get_all_services()
    except ApplicationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())


@router.post("/add")
async def add_inference_service(inference_service_request_body: InferenceServiceRequestBody) -> None:
    try:
        return inference_services_manager.add_service(inference_service_request_body)
    except ApplicationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())


@router.post("/edit")
async def edit_inference_service(inference_service_request_body: InferenceServiceRequestBody) -> None:
    try:
        return inference_services_manager.edit_service(inference_service_request_body)
    except ApplicationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())


@router.post("/delete")
async def delete_inference_service(uuid: str) -> None:
    try:
        return inference_services_manager.remove_service(uuid)
    except ApplicationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())
