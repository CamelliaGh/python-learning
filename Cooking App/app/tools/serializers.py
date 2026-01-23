from app.routes.schemas import RecipeOut
from app.db.models import Recipe

def serialize_recipe(recipe: Recipe) -> RecipeOut:
    return RecipeOut(
        id=recipe.id,
        name=recipe.name,
        ingredients=[i.name for i in recipe.ingredients],
        steps=recipe.steps,
    )