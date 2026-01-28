"""Main application entry point for the Cooking App.

This module creates and configures the FastAPI application instance, including
database initialization, CORS middleware, static file serving, and route registration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import (
    API_PREFIX,
    CORS_ALLOW_HEADERS,
    CORS_ALLOW_METHODS,
    CORS_ALLOW_ORIGINS,
    STATIC_DIRECTORY,
)
from app.db.session import Base, engine
from app.routes.routes import router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance.

    Sets up the database tables, static file serving, CORS middleware,
    and includes the API router.

    Returns:
        FastAPI: The configured FastAPI application instance.
    """
    app_instance = FastAPI()
    Base.metadata.create_all(bind=engine)

    app_instance.mount(
        "/static", StaticFiles(directory=STATIC_DIRECTORY), name="static"
    )

    app_instance.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ALLOW_ORIGINS,
        allow_methods=CORS_ALLOW_METHODS,
        allow_headers=CORS_ALLOW_HEADERS,
    )

    app_instance.include_router(router, prefix=API_PREFIX)
    return app_instance


app = create_app()
