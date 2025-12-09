from .health import router as health_router
from .articles import router as articles_router
from .admin import router as admin_router

__all__ = ["health_router", "articles_router", "admin_router"]
