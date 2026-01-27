"""Serialization and utility functions for converting database models to API response models.

This module provides functions to convert SQLAlchemy ORM models into Pydantic
models suitable for API responses, as well as utility functions for processing
recipe data transformations.
"""

from typing import List

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


def parse_steps(steps: str | None) -> List[str]:
    """Parse recipe steps string into a list of individual step strings.
    
    Splits a multi-line steps string by newline characters and returns
    a cleaned list of non-empty step strings. Each step is stripped of
    leading and trailing whitespace.
    
    Args:
        steps: The recipe steps as a string (may contain newlines),
               or None if no steps are provided.
    
    Returns:
        List[str]: A list of step strings, with empty lines filtered out.
                   Returns an empty list if steps is None or empty.
    
    Example:
        >>> steps = "1. Heat the pan\\n2. Add oil\\n\\n3. Cook chicken"
        >>> parse_steps(steps)
        ['1. Heat the pan', '2. Add oil', '3. Cook chicken']
        
        >>> parse_steps(None)
        []
        
        >>> parse_steps("")
        []
    """
    if not steps:
        return []
    
    return [s.strip() for s in steps.split("\n") if s.strip()]

