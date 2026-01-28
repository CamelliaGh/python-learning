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
from app.config import (
    ERROR_EMPTY_INGREDIENTS_LIST,
    ERROR_FAILED_TO_GENERATE_RECIPE,
    ERROR_FAILED_TO_PARSE_AI_RESPONSE,
    ERROR_INVALID_AI_RESPONSE_FORMAT,
    ERROR_INVALID_RECIPE_FORMAT,
    ERROR_MISSING_INGREDIENTS,
    ERROR_NO_INGREDIENTS_PROVIDED,
    ERROR_NO_RECIPES_FOUND,
    ERROR_RECIPE_NOT_FOUND,
    HTTP_STATUS_BAD_REQUEST,
    HTTP_STATUS_INTERNAL_SERVER_ERROR,
    HTTP_STATUS_NOT_FOUND,
    PAGINATION_DEFAULT_PAGE,
    PAGINATION_DEFAULT_PER_PAGE,
    PAGINATION_MAX_PER_PAGE,
    PAGINATION_MIN_PAGE,
    PAGINATION_MIN_PER_PAGE,
    PROMPT_SYSTEM_RECIPE_PROMPT,
    PROMPT_USER_RECIPE_PROMPT,
)
from app.db.session import get_db
from app.routes.schemas import (
    IngredientsIn,
    PaginatedRecipes,
    RecipeDetail,
    RecipeOut,
    StepsOut,
)
from app.services.openai_service import call_api as openai
from app.tools.openai_response_parser import RecipeParseError
from app.tools.serializers import parse_steps, serialize_recipe, serialize_recipe_detail

router = APIRouter()


@router.get("/recipes", response_model=PaginatedRecipes)
def get_all_recipes_paginated(
    page: int = Query(PAGINATION_DEFAULT_PAGE, ge=PAGINATION_MIN_PAGE),
    per_page: int = Query(
        PAGINATION_DEFAULT_PER_PAGE,
        ge=PAGINATION_MIN_PER_PAGE,
        le=PAGINATION_MAX_PER_PAGE,
    ),
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
        recipes=[serialize_recipe(recipe) for recipe in items],
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
        raise HTTPException(
            status_code=HTTP_STATUS_NOT_FOUND, detail=ERROR_RECIPE_NOT_FOUND
        )

    steps_list = parse_steps(recipe.steps)
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
        raise HTTPException(
            status_code=HTTP_STATUS_BAD_REQUEST, detail=ERROR_MISSING_INGREDIENTS
        )

    ingredient_names = [
        name.strip().lower() for name in payload.ingredients if name.strip()
    ]
    if not ingredient_names:
        raise HTTPException(
            status_code=HTTP_STATUS_BAD_REQUEST, detail=ERROR_EMPTY_INGREDIENTS_LIST
        )

    recipes = db_helpers.get_recipe_by_ingredient(ingredient_names, db)
    return [serialize_recipe(recipe) for recipe in recipes]


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
        raise HTTPException(
            status_code=HTTP_STATUS_NOT_FOUND, detail=ERROR_NO_RECIPES_FOUND
        )
    return serialize_recipe(recipe)


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
    recipe_ratings = db_helpers.get_popular_recipes(db)
    if not recipe_ratings:
        raise HTTPException(
            status_code=HTTP_STATUS_NOT_FOUND, detail=ERROR_NO_RECIPES_FOUND
        )

    return [
        serialize_recipe_detail(recipe, avg_rating)
        for recipe, avg_rating in recipe_ratings
    ]


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
    recipe = db_helpers.get_recipe(recipe_id, db)
    if not recipe:
        raise HTTPException(
            status_code=HTTP_STATUS_NOT_FOUND, detail=ERROR_RECIPE_NOT_FOUND
        )

    average = db_helpers.avg_rating(recipe, db)
    return serialize_recipe_detail(recipe, average)


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
        raise HTTPException(
            status_code=HTTP_STATUS_BAD_REQUEST, detail=ERROR_NO_INGREDIENTS_PROVIDED
        )

    ingredient_str = ", ".join(ingredients)
    response = openai(
        system_prompt_name=PROMPT_SYSTEM_RECIPE_PROMPT,
        user_prompt_name=PROMPT_USER_RECIPE_PROMPT,
        variables={"ingredients": ingredient_str},
    )

    if response is None:
        raise HTTPException(
            status_code=HTTP_STATUS_INTERNAL_SERVER_ERROR,
            detail=ERROR_FAILED_TO_GENERATE_RECIPE,
        )

    try:
        name, parsed_ingredients, steps = openai_parser.get_recipe_items(response)
        return JSONResponse(
            {
                "name": name,
                "ingredients": parsed_ingredients,
                "steps": steps,
            }
        )
    except RecipeParseError as e:
        raise HTTPException(
            status_code=HTTP_STATUS_INTERNAL_SERVER_ERROR,
            detail=ERROR_FAILED_TO_PARSE_AI_RESPONSE.format(error=str(e)),
        )
    except (TypeError, AttributeError, ValueError) as e:
        raise HTTPException(
            status_code=HTTP_STATUS_INTERNAL_SERVER_ERROR,
            detail=ERROR_INVALID_AI_RESPONSE_FORMAT.format(error=str(e)),
        )
    except Exception:
        raise HTTPException(
            status_code=HTTP_STATUS_INTERNAL_SERVER_ERROR,
            detail=ERROR_INVALID_RECIPE_FORMAT,
        )
