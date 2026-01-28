"""FastAPI route handlers for ingredient-related endpoints.

This module defines API endpoints for retrieving ingredient information
from the database.
"""

from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.db.db_helpers import get_all_ingredients as db_helpers_get_all_ingredients
from app.db.session import get_db

router = APIRouter()


@router.get("/api/ingredients", response_model=List[str])
def get_all_ingredients(db: Session = Depends(get_db)):
    """Get all ingredients from the database.

    Args:
        db: Database session dependency.

    Returns:
        dict: Success message and the list of ingredients.
    """
    db_ingredients = db_helpers_get_all_ingredients(db)
    return JSONResponse(content={"ingredients": db_ingredients})
