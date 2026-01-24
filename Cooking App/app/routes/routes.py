"""Main router configuration for the Cooking App API.

This module sets up the main API router and includes all route modules.
"""

from fastapi import APIRouter

from app.routes.recipes import router as recipes_router

router = APIRouter()
router.include_router(recipes_router)
