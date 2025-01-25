# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings, Settings
from app.api.routes import router as api_router


def create_app(settings: Settings) -> FastAPI:
    """
    Create and configure the FastAPI application.

    This function initializes a FastAPI app with the given settings, optionally
    hiding the API documentation endpoints based on the environment.

    It also includes the router for the API under the prefix "/api/v1".

    Args:
        settings (Settings): The settings object containing configuration
            values like the environment (`ENV`) to determine whether
            the API documentation should be exposed.

    Returns:
        FastAPI: The configured FastAPI application instance.

    Example:
        ```python
        settings = Settings(ENV="production")
        app = create_app(settings)
        ```
    """
    docs_url = "/docs"
    redoc_url = "/redoc"
    if settings.ENV != "development":  # Hide API docs
        docs_url = None
        redoc_url = None

    app = FastAPI(
        docs_url=docs_url,
        redoc_url=redoc_url,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.ALLOW_CREDENTIALS,
        allow_methods=settings.ALLOW_METHODS,
        allow_headers=settings.ALLOW_HEADERS,
    )
    app.include_router(api_router, prefix="/api/v1")

    return app


app: FastAPI = create_app(settings=settings)
