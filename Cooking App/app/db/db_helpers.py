"""Database helper functions for recipe operations.

This module provides utility functions for querying and manipulating recipe data
in the database, including pagination, filtering, and aggregation operations.
"""

import math
from typing import List

from sqlalchemy import func

from app.db.models import Ingredient, Recipe, Review, recipe_ingredient


def get_recipe(recipe_id, db):
    """Retrieve a recipe by its ID from the database.
    
    Args:
        recipe_id: The unique identifier of the recipe to retrieve.
        db: The database session object.
    
    Returns:
        Recipe object if found, None otherwise.
    """
    return db.get(Recipe, recipe_id)


def avg_rating(recipe, db):
    """Calculate the average rating for a given recipe.
    
    Args:
        recipe: The Recipe object to calculate the average rating for.
        db: The database session object.
    
    Returns:
        float: The average rating rounded to 2 decimal places, or None if no ratings exist.
    """
    avg_rating_value = (
        db.query(func.avg(Review.rating)).filter(Review.recipe_id == recipe.id).scalar()
    )
    average = round(float(avg_rating_value), 2) if avg_rating_value is not None else None
    return average





def get_db_recipes(page, per_page, db):
    """Retrieve paginated recipes from the database.
    
    Args:
        page: The page number (1-indexed) to retrieve.
        per_page: The number of recipes per page.
        db: The database session object.
    
    Returns:
        tuple: A tuple containing:
            - items: List of Recipe objects for the requested page.
            - total: Total number of recipes in the database.
            - pages: Total number of pages available.
    """
    total: int = db.query(func.count(Recipe.id)).scalar() or 0  # pylint: disable=not-callable
    offset = (page - 1) * per_page
    items: List[Recipe] = db.query(Recipe).offset(offset).limit(per_page).all()
    pages = math.ceil(total / per_page) if per_page else 0

    return items, total, pages


def get_ingredients_id(ingredient_names, db):
    """Get ingredient IDs for a list of ingredient names (case-insensitive).
    
    Args:
        ingredient_names: List of ingredient names to search for (should be lowercase).
        db: The database session object.
    
    Returns:
        List[int]: List of ingredient IDs that match the provided names, or empty list if none found.
    """
    ingredient_ids = (
        db.query(Ingredient.id)
        .filter(func.lower(Ingredient.name).in_(ingredient_names))
        .all()
    )
    ingredient_ids = [i[0] for i in ingredient_ids]
    if not ingredient_ids:
        return []

    return ingredient_ids


def get_recipe_by_ingredient(ingredient_names, db):
    """Find recipes that contain all of the specified ingredients.
    
    Args:
        ingredient_names: List of ingredient names (case-insensitive) that the recipe must contain.
        db: The database session object.
    
    Returns:
        List[Recipe]: List of Recipe objects that contain all the specified ingredients.
    """
    subq = (
        db.query(
            recipe_ingredient.c.recipe_id.label("recipe_id"),
            func.count(  # pylint: disable=not-callable
                func.distinct(func.lower(Ingredient.name))
            ).label("match_count"),
        )
        .join(Ingredient, recipe_ingredient.c.ingredient_id == Ingredient.id)
        .filter(func.lower(Ingredient.name).in_(ingredient_names))
        .group_by(recipe_ingredient.c.recipe_id)
        .subquery()
    )

    recipes = (
        db.query(Recipe)
        .join(subq, Recipe.id == subq.c.recipe_id)
        .filter(subq.c.match_count == len(ingredient_names))
        .all()
    )

    return recipes


def get_random_recipe(db):
    """Retrieve a random recipe from the database.
    
    Args:
        db: The database session object.
    
    Returns:
        Recipe: A random Recipe object, or None if no recipes exist.
    """
    recipe = db.query(Recipe).order_by(func.random()).first()  # pylint: disable=not-callable
    return recipe


def get_popular_recipes(db, limit: int = 10):
    """Retrieve the top N most popular recipes based on average rating.
    
    Args:
        db: The database session object.
        limit: Maximum number of recipes to return (default: 10).
    
    Returns:
        List[RecipeDetail]: List of the top 10 recipes with their average ratings,
            ordered by average rating in descending order.
            avg_rating is a float rounded to 2 decimal places, or None if no ratings exist.
    """
    subq = (
        db.query(
            Review.recipe_id.label("recipe_id"),
            func.avg(Review.rating).label("avg_rating"),
        )
        .group_by(Review.recipe_id)
        .subquery()
    )
    rows = (
        db.query(Recipe, subq.c.avg_rating)
        .join(subq, Recipe.id == subq.c.recipe_id)
        .order_by(subq.c.avg_rating.desc())
        .limit(limit)
        .all()
    )
    return [
        (
            recipe,
            round(float(avg_rating), 2) if avg_rating is not None else None,
        )
        for recipe, avg_rating in rows
    ]
