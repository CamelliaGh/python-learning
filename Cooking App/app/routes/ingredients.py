from fastapi import APIRouter
from fastapi.dependencies import Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.db.db_helpers import get_all_ingredients as db_helpers_get_all_ingredients
router = APIRouter()

@router.get("/api/ingredients", response_model=List[str])
def get_all_ingredients(db: Session = Depends(get_db)):
    db_ingredients = db_helpers_get_all_ingredients(db)
    return JSONResponse(content={"ingredients": db_ingredients})