"""Main application entry point for the Cooking App.

This module creates and configures the FastAPI application instance, including
database initialization, CORS middleware, static file serving, and route registration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.db.session import Base, engine
from app.routes.routes import router

def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance.
    
    Sets up the database tables, static file serving, CORS middleware,
    and includes the API router.
    
    Returns:
        FastAPI: The configured FastAPI application instance.
    """
    app = FastAPI()
    Base.metadata.create_all(bind=engine)
    
    app.mount("/static", StaticFiles(directory="static"), name="static")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router, prefix="/api")
    return app

app = create_app()