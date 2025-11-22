from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter(prefix="/api/v1", tags=["v1"])


@router.get("/health")
def health():
    settings = get_settings()
    return {"status": "ok", "service": settings.app_name, "version": settings.app_version}
