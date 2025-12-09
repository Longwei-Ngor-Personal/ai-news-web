from fastapi import APIRouter
from ..config import settings

router = APIRouter()


@router.get("/health")
def health_check():
    """
    Simple health check endpoint.
    Returns basic info so we know the API is alive.
    """
    return {
        "status": "ok",
        "app_name": settings.app_name,
        "environment": settings.environment,
    }
