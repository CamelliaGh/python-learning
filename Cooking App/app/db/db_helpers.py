from sqlalchemy import func
from app.db.models import Review, Recipe, Ingredient, recipe_ingredient, Review
import math
from typing import List
from app.tools.serializers import serialize_recipe
from app.routes.schemas import RecipeDetail


def get_recipe(recipe_id, db):
    return db.get(Recipe, recipe_id)


def avg_rating(recipe, db):
    avg_rating = (
        db.query(func.avg(Review.rating)).filter(
            Review.recipe_id == recipe.id).scalar()
    )
    average = round(float(avg_rating), 2) if avg_rating is not None else None
    return average


def get_db_recipe(recipe_id, db):
    return db.get(Recipe, recipe_id)


def get_db_recipes(page, per_page, db):
    total: int = db.query(func.count(Recipe.id)).scalar() or 0
    offset = (page - 1) * per_page
    items: List[Recipe] = db.query(Recipe).offset(offset).limit(per_page).all()
    pages = math.ceil(total / per_page) if per_page else 0

    return items, total, pages


def get_ingredients_id(ingredient_names, db):
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
    subq = (
        db.query(
            recipe_ingredient.c.recipe_id.label("recipe_id"),
            func.count(func.distinct(func.lower(Ingredient.name))
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

    return [serialize_recipe(r) for r in recipes]


def get_random_recipe(db):
    recipe = db.query(Recipe).order_by(func.random()).first()
    if recipe:
        return serialize_recipe(recipe)
    return None


def get_popular_recipes(db):
    subq = (
        db.query(
            Review.recipe_id.label("recipe_id"),
            func.avg(Review.rating).label("avg_rating"),
        )
        .group_by(Review.recipe_id)
        .subquery()
    )
    rows = db.query(Recipe, subq.c.avg_rating).join(
        Recipe, subq, Recipe.id == subq.c.recipe_id).order_by(subq.c.avg_rating.desc()).limit(10).all()
    return [
        RecipeDetail( #TODO:remove RecipeDetail from db_helper 
            **serialize_recipe(recipe).dict(),
            average_rating=round(
                float(avg_rating), 2) if avg_rating is not None else None
        )
        for recipe, avg_rating in rows
    ]
