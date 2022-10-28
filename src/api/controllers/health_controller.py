from fastapi import APIRouter
from starlette.responses import Response

router = APIRouter()


@router.get("/")
def health():
    return Response(status_code=200)
