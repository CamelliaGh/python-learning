from fastapi import BaseModel, Optional
from typing import List


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
    
class RecipeOut(BaseModel):
    id: int
    name: Optional[str] = None
    ingredients: List[str] = []
    steps: Optional[str] = None    
    
    
class IngredientsIn(BaseModel):
    ingredients: List[str]    
