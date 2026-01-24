"""Pydantic schemas for request and response models.

This module defines the data models used for API request validation and
response serialization, including recipe details, pagination, and ingredient filtering.
"""

from typing import List, Optional

from pydantic import BaseModel


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
