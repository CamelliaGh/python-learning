"""Main router configuration for the Cooking App API.

This module sets up the FastAPI application and includes all route modules.
"""

from fastapi import FastAPI

from app.routes.recipes import router as recipes_router

app = FastAPI()
app.include_router(recipes_router)
