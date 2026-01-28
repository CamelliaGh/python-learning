"""FastAPI route handlers for review-related endpoints.

This module defines API endpoints for submitting reviews for recipes.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import db_helpers
from app.db.session import get_db
from app.routes.schemas import ReviewIn

router = APIRouter()


@router.post("/api/reviews", status_code=201)
def submit_review(payload: ReviewIn, db: Session = Depends(get_db)):
    """Submit a review for a recipe.

    Args:
        payload: Review data containing recipe_id and rating (1-5).
        db: Database session dependency.

    Returns:
        dict: Success message and the created review object.

    Raises:
        HTTPException: If the review data is invalid (400 status code).
    """
    try:
        review = db_helpers.store_review_in_db(payload.model_dump(), db)
        return {"message": "Review submitted successfully", "review": review}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    