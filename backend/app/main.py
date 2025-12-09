from fastapi import FastAPI

from .config import settings
from .db import Base, engine
from .routes import health_router, articles_router


def create_app() -> FastAPI:
    """
    Application factory: creates and configures the FastAPI app.
    """
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
    )

    # Create tables if they don't exist yet
    Base.metadata.create_all(bind=engine)

    # Routers
    app.include_router(health_router, tags=["Health"])
    app.include_router(articles_router)

    @app.get("/")
    def root():
        return {
            "message": "Welcome to the AI News Web Digestor API",
            "docs_url": "/docs",
            "health_url": "/health",
            "articles_url": "/articles/",
        }

    return app


app = create_app()
