"""Pydantic schemas for request and response models.

This module defines the data models used for API request validation and
response serialization, including recipe details, pagination, and ingredient filtering.
"""

from typing import List, Optional

from pydantic import BaseModel, field_validator


class RecipeOut(BaseModel):
    id: int
    name: Optional[str] = None
    ingredients: List[str] = []
    steps: Optional[str] = None


class RecipeDetail(RecipeOut):
    average_rating: Optional[float] = None


class PaginatedRecipes(BaseModel):
    recipes: List[RecipeOut]
    total: int
    page: int
    per_page: int
    pages: int
    has_next: bool
    has_prev: bool


class StepsOut(BaseModel):
    recipe_id: int
    name: Optional[str] = None
    steps: List[str]


class IngredientsIn(BaseModel):
    ingredients: List[str]

class ReviewIn(BaseModel):
    recipe_id: int
    rating: int

    @field_validator("rating")
    def rating_range(self, v):
        if not 1 <= v <= 5:
            raise ValueError("rating must be between 1 and 5")
        return v
