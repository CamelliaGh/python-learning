from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import app.db.db_helpers as db_helpers
from app.db.session import get_db
from app.routes.schemas import (
    IngredientsIn,
    PaginatedRecipes,
    RecipeDetail,
    RecipeOut,
    StepsOut,
)

router = APIRouter()


@router.get("/recipes/{recipe_id}", response_model=RecipeDetail)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db_helpers.get_db_recipe(recipe_id, db)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    average = db_helpers.avg_rating(recipe, db)
    return RecipeDetail(
        id=recipe.id,
        name=recipe.name,
        ingredients=[i.name for i in recipe.ingredients],
        steps=recipe.steps,
        average_rating=average,
    )


@router.get("/recipes", response_model=PaginatedRecipes)
def get_all_recipes_paginated(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    items, total, pages = db_helpers.get_db_recipes(page, per_page, db)

    return PaginatedRecipes(
        recipes=[
            RecipeOut(
                id=recipe.id,
                name=recipe.name,
                ingredients=[i.name for i in recipe.ingredients],
                steps=recipe.steps,
            )
            for recipe in items
        ],
        total=total,
        page=page,
        per_page=per_page,
        pages=pages,
        has_next=page < pages,
        has_prev=page > 1,
    )


@router.get("/recipes/{recipe_id}/steps", response_model=StepsOut)
def get_recipe_steps_array(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db_helpers.get_recipe(recipe_id, db)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    steps_list = []
    if recipe.steps:
        steps_list = [s.strip() for s in recipe.steps.split("\n") if s.strip()]
    return StepsOut(recipe_id=recipe.id, name=recipe.name, steps=steps_list)


@router.post("/recipes/by-ingredients", response_model=List[RecipeOut])
def get_recipes_by_ingredients(payload: IngredientsIn, db: Session = Depends(get_db)):
    if not payload.ingredients:
        raise HTTPException(status_code=400, detail='Missing "ingredients" in request')

    ingredient_names = [
        name.strip().lower() for name in payload.ingredients if name.strip()
    ]
    if not ingredient_names:
        raise HTTPException(status_code=400, detail="Empty ingredients list")


    recipes = db_helpers.get_recipe_by_ingredient(ingredient_names, db)
    return recipes


@router.get("/recipes/random", response_model=RecipeOut)
def get_random_recipe(db: Session = Depends(get_db)):
    recipe = db_helpers.get_random_recipe(db)
    if not recipe:
        raise HTTPException(status_code=404, detail="No recipes found")
    return recipe


@router.get("/recipes/popular", response_model=List[RecipeDetail])
def get_popular_recipes(db: Session = Depends(get_db)):
    recipes = get_popular_recipes(db)
    if not recipes:
        raise HTTPException(status_code=404, detail="No recipes found")
    return recipes
