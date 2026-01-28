"""Pydantic schemas for request and response models.

This module defines the data models used for API request validation and
response serialization, including recipe details, pagination, and ingredient filtering.
"""

from typing import List, Optional

from pydantic import BaseModel, field_validator


class RecipeOut(BaseModel):
    """Schema for a recipe output.

    Attributes:
        id: The ID of the recipe.
        name: The name of the recipe.
        ingredients: The ingredients of the recipe.
        steps: The steps of the recipe.
    """
    id: int
    name: Optional[str] = None
    ingredients: List[str] = []
    steps: Optional[str] = None


class RecipeDetail(RecipeOut):
    """Schema for a recipe detail output.

    Attributes:
        average_rating: The average rating of the recipe.
    """
    average_rating: Optional[float] = None


class PaginatedRecipes(BaseModel):
    """Schema for a paginated recipes output.

    Attributes:
        recipes: The list of recipes.
        total: The total number of recipes.
        page: The current page number.
        per_page: The number of recipes per page.
        pages: The total number of pages.
        has_next: Whether there is a next page.
        has_prev: Whether there is a previous page.
    """
    recipes: List[RecipeOut]
    total: int
    page: int
    per_page: int
    pages: int
    has_next: bool
    has_prev: bool


class StepsOut(BaseModel):
    """Schema for a steps output.

    Attributes:
        recipe_id: The ID of the recipe.
        name: The name of the recipe.
        steps: The steps of the recipe.
    """
    recipe_id: int
    name: Optional[str] = None
    steps: List[str]


class IngredientsIn(BaseModel):
    """Schema for a ingredients input.

    Attributes:
        ingredients: The list of ingredients.
    """
    ingredients: List[str]


class ReviewIn(BaseModel):
    """Schema for a review input.

    Attributes:
        recipe_id: The ID of the recipe.
        rating: The rating of the recipe.
    """
    recipe_id: int
    rating: int

    @field_validator("rating")
    @classmethod
    def validate_rating(cls, v):
        """Validate the rating.

        Args:
            v: The rating to validate.

        Returns:
            The validated rating.
        """
        if not 1 <= v <= 5:
            raise ValueError("rating must be between 1 and 5")
        return v
