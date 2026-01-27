"""FastAPI route handlers for recipe-related endpoints.

This module defines all the API endpoints for managing and retrieving recipes,
including pagination, filtering by ingredients, and retrieving popular recipes.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

import app.db.db_helpers as db_helpers
import app.tools.openai_response_parser as openai_parser
from app.db.session import get_db
from app.routes.schemas import (
    IngredientsIn,
    PaginatedRecipes,
    RecipeDetail,
    RecipeOut,
    StepsOut,
)
from app.services.openai_service import call_api as openai

router = APIRouter()


@router.get("/recipes/{recipe_id}", response_model=RecipeDetail)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific recipe by ID with its average rating.

    Args:
        recipe_id: The unique identifier of the recipe to retrieve.
        db: The database session (injected dependency).

    Returns:
        RecipeDetail: The recipe details including average rating.

    Raises:
        HTTPException: 404 if the recipe is not found.
    """
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
    """Retrieve all recipes with pagination support.

    Args:
        page: The page number to retrieve (default: 1, minimum: 1).
        per_page: Number of recipes per page (default: 10, range: 1-100).
        db: The database session (injected dependency).

    Returns:
        PaginatedRecipes: A paginated response containing recipes and pagination metadata.
    """
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
    """Retrieve recipe steps as an array of strings.

    Args:
        recipe_id: The unique identifier of the recipe.
        db: The database session (injected dependency).

    Returns:
        StepsOut: The recipe with steps split into an array of strings.

    Raises:
        HTTPException: 404 if the recipe is not found.
    """
    recipe = db_helpers.get_recipe(recipe_id, db)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    steps_list = []
    if recipe.steps:
        steps_list = [s.strip() for s in recipe.steps.split("\n") if s.strip()]
    return StepsOut(recipe_id=recipe.id, name=recipe.name, steps=steps_list)


@router.post("/recipes/by-ingredients", response_model=List[RecipeOut])
def get_recipes_by_ingredients(payload: IngredientsIn, db: Session = Depends(get_db)):
    """Find recipes that contain all of the specified ingredients.

    Args:
        payload: Request body containing a list of ingredient names.
        db: The database session (injected dependency).

    Returns:
        List[RecipeOut]: List of recipes that contain all the specified ingredients.

    Raises:
        HTTPException: 400 if ingredients are missing or empty.
    """
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
    """Retrieve a random recipe from the database.

    Args:
        db: The database session (injected dependency).

    Returns:
        RecipeOut: A randomly selected recipe.

    Raises:
        HTTPException: 404 if no recipes exist in the database.
    """
    recipe = db_helpers.get_random_recipe(db)
    if not recipe:
        raise HTTPException(status_code=404, detail="No recipes found")
    return recipe


@router.get("/recipes/popular", response_model=List[RecipeDetail])
def get_popular_recipes(db: Session = Depends(get_db)):
    """Retrieve the top 10 most popular recipes based on average rating.

    Args:
        db: The database session (injected dependency).

    Returns:
        List[RecipeDetail]: List of top 10 recipes with their average ratings.

    Raises:
        HTTPException: 404 if no recipes with ratings exist.
    """
    recipes = db_helpers.get_popular_recipes(db)
    if not recipes:
        raise HTTPException(status_code=404, detail="No recipes found")
    return recipes


@router.post("/recipes/generate")
def generate_recipe(payload: IngredientsIn):
    """Generate a new recipe using AI based on provided ingredients.

    Takes a list of ingredients and uses OpenAI to generate a complete recipe
    including name, ingredients list, and cooking steps. The generated recipe
    is parsed and returned as a JSON response.

    Args:
        payload: Request body containing a list of ingredient names to use
            for recipe generation.

    Returns:
        JSONResponse: A JSON object containing:
            - name: The generated recipe name
            - ingredients: List of ingredients for the recipe
            - steps: List of cooking steps

    Raises:
        HTTPException: 400 if no ingredients are provided.
        HTTPException: 500 if recipe generation fails or the response format
            is invalid.
    """
    ingredients = payload.ingredients or []
    if not ingredients:
        raise HTTPException(status_code=400, detail="No ingredients provided")

    ingredient_str = ", ".join(ingredients)
    response = openai(
        system_prompt_name="system_recipe_prompt",
        user_prompt_name="user_recipe_prompt",
        variables={"ingredients": ingredient_str},
    )

    if response is None:
        raise HTTPException(status_code=500, detail="Failed to generate recipe")

    lines = response.strip().splitlines()
    name, parsed_ingredients,steps =  openai_parser.get_recipe_items(lines)
    try:
        return JSONResponse(
            {
                "name": name,
                "ingredients": parsed_ingredients,
                "steps": steps,
            }
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Invalid recipe format from AI")
