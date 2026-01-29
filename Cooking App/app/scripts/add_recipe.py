"""Interactive script for adding recipes to the database.

This script provides a command-line interface for users to input recipe information
(name, ingredients, and steps) and save it to the database. It handles duplicate
detection and ingredient normalization.
"""

import os
import sys

from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError

# Setup: Ensure project root is in Python path when running from scripts directory
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_SCRIPT_DIR, "..", ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

# Clear any cached app modules to ensure fresh imports from local source
for key in list(sys.modules.keys()):
    if key.startswith("app.") or key == "app":
        del sys.modules[key]

# Now import normally - Python will use local source since PROJECT_ROOT is first in path
from app.db.db_helpers import store_recipe_in_db  # noqa: E402
from app.db.models import Ingredient, Recipe  # noqa: E402
from app.db.session import get_db_session  # noqa: E402


def read_recipe():
    """Read recipe information from user input.

    Prompts the user for recipe name, ingredients, and steps.

    Returns:
        tuple: A tuple containing (name, ingredients, steps).
            - name: The recipe name as a string.
            - ingredients: A list of ingredient names.
            - steps: The recipe steps as a string.
    """
    name = read_name()
    ingredients = prompt_for_ingredients()
    steps = prompt_for_steps()
    return name, ingredients, steps


def read_name():
    """Prompt the user for a recipe name.

    Returns:
        str: The recipe name entered by the user, or None if empty.
    """
    name = input("🍽️ Recipe name: ").strip()
    if not name:
        print("❌ Recipe name is required.")
        return
    return name


def prompt_for_ingredients():
    """Prompt the user to enter ingredients one by one.

    Continues reading ingredients until an empty line is entered.

    Returns:
        List[str]: A list of ingredient names entered by the user.
    """
    print("Enter ingredients (one per line). Leave empty and press Enter to finish.")
    ingredients = []
    while True:
        try:
            item = input("> ")
        except EOFError:
            break
        item = item.strip()
        if not item:
            break
        ingredients.append(item)
    return ingredients


def prompt_for_steps():
    """Prompt the user to enter recipe steps.

    Continues reading lines until "END" is entered on a line by itself.

    Returns:
        str: The recipe steps as a newline-separated string.
    """
    print("Enter steps (multiple lines). Type END on a line by itself to finish.")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip().upper() == "END":
            break
        lines.append(line)
    return "\n".join(lines)


def save_recipe(name, steps, ingredients_input):
    """Save a recipe to the database.

    Checks for duplicate recipes (case-insensitive) and reuses existing ingredients
    or creates new ones as needed. Ingredients are stored in lowercase.

    Args:
        name: The name of the recipe.
        steps: The recipe steps as a string.
        ingredients_input: A list of ingredient names to associate with the recipe.

    Raises:
        SQLAlchemyError: If a database error occurs during the operation.
        IntegrityError: If a database constraint violation occurs.
        OperationalError: If a database connection or operational error occurs.
    """
    with get_db_session() as db_session:
        try:
            # Check for duplicates (case-insensitive)
            existing = db_session.query(Recipe).filter(Recipe.name.ilike(name)).first()
            if existing:
                print(f"⚠️ Recipe '{name}' already exists (id={existing.id}).")
                return

            recipe = Recipe(name=name, steps=steps)

            # Reuse or create ingredients (stored lowercase)
            for ing_name in ingredients_input:
                norm = ing_name.strip().lower()
                if not norm:
                    continue
                ingredient = (
                    db_session.query(Ingredient).filter(Ingredient.name == norm).first()
                )
                if not ingredient:
                    ingredient = Ingredient(name=norm)
                    db_session.add(ingredient)
                    db_session.flush()
                recipe.ingredients.append(ingredient)

            db_session.add(recipe)
            db_session.commit()
            print(
                f"✅ Recipe '{name}' added successfully with {len(recipe.ingredients)} ingredients (id={recipe.id})."
            )
        except IntegrityError as e:
            db_session.rollback()
            print(f"❌ Database constraint error: {e}")
            raise
        except OperationalError as e:
            db_session.rollback()
            print(f"❌ Database connection error: {e}")
            raise
        except SQLAlchemyError as e:
            db_session.rollback()
            print(f"❌ Database error: {e}")
            raise
        except (AttributeError, TypeError, ValueError) as e:
            db_session.rollback()
            print(f"❌ Data validation error: {e}")
            raise


if __name__ == "__main__":
    recipe_name, recipe_ingredients, recipe_steps = read_recipe()
    print(f"You entered {recipe_name}\ningredients: {recipe_ingredients} \nsteps: {recipe_steps}")
    # save_recipe(recipe_name, steps, ingredients)
    with get_db_session() as session:
        store_recipe_in_db(
            {"name": recipe_name, "steps": recipe_steps, "ingredients": recipe_ingredients}, session
        )
