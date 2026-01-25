"""Serialization utilities for converting database models to API response models.

This module provides functions to convert SQLAlchemy ORM models into Pydantic
models suitable for API responses.
"""

from app.db.models import Recipe
from app.routes.schemas import RecipeOut


def serialize_recipe(recipe: Recipe) -> RecipeOut:
    """Serialize a Recipe database model to a RecipeOut Pydantic model.
    
    Args:
        recipe: The Recipe database model instance to serialize.
    
    Returns:
        RecipeOut: A Pydantic model containing the recipe data.
    """
    return RecipeOut(
        id=recipe.id,
        name=recipe.name,
        ingredients=[i.name for i in recipe.ingredients],
        steps=recipe.steps,
    )

