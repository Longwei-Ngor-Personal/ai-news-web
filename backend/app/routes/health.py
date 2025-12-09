from fastapi import APIRouter
from ..config import settings

router = APIRouter()


@router.get("/health")
def health_check():
    """
    Simple health check endpoint.
    """
    return {
        "status": "ok",
        "app_name": settings.app_name,
        "environment": settings.environment,
    }
