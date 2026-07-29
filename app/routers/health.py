from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas.response import SuccessResponse

router = APIRouter()


@router.get("/health", response_model=SuccessResponse, tags=["system"])
def health_check() -> SuccessResponse:
    settings = get_settings()
    return SuccessResponse(
        data={"status": "ok", "service": settings.app_name, "version": settings.app_version}
    )
