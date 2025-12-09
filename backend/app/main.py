from fastapi import FastAPI
from .config import settings
from .routes import health_router


def create_app() -> FastAPI:
    """
    Application factory: creates and configures the FastAPI app.
    """
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
    )

    # Include routers
    app.include_router(health_router, tags=["Health"])

    @app.get("/")
    def root():
        return {
            "message": "Welcome to the AI News Web Digestor API",
            "docs_url": "/docs",
            "health_url": "/health",
        }

    return app


app = create_app()
