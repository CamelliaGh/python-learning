"""Interactive script for adding recipes to the database.

This script provides a command-line interface for users to input recipe information
(name, ingredients, and steps) and save it to the database. It handles duplicate
detection and ingredient normalization.
"""

import importlib.util
import os
import sys

from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError

from app.db.models import Ingredient, Recipe
from app.db.session import SessionLocal

# Ensure project root is importable when running from ./scripts/
# MUST be done before any app imports
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))

# Verify local app directory exists
LOCAL_APP_DIR = os.path.join(PROJECT_ROOT, "app")
LOCAL_DB_HELPERS = os.path.join(LOCAL_APP_DIR, "db", "db_helpers.py")
if not os.path.exists(LOCAL_DB_HELPERS):
    raise ImportError(
        f"ERROR: Cannot find local app module at {LOCAL_DB_HELPERS}.\n"
        f"Project root: {PROJECT_ROOT}\n"
        f"Current directory: {os.getcwd()}"
    )

# Ensure our local project root is first in sys.path
# This makes Python check our local 'app' package before any installed one
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
else:
    # If it exists, move it to the front to ensure priority
    sys.path.remove(PROJECT_ROOT)
    sys.path.insert(0, PROJECT_ROOT)

os.chdir(PROJECT_ROOT)

# Force Python to use local source instead of installed package
# Remove any cached app modules to ensure fresh import from local source
modules_to_remove = [key for key in list(sys.modules.keys()) if key.startswith("app.")]
for module in modules_to_remove:
    del sys.modules[module]

# Also remove the base 'app' module if it exists
if "app" in sys.modules:
    del sys.modules["app"]

# noqa: E402

# Import db_helpers - handle case where installed package conflicts
try:
    # Verify we got the local version, not site-packages
    import app.db.db_helpers as _check_module
    from app.db.db_helpers import store_recipe_in_db

    _imported_path = os.path.abspath(_check_module.__file__)
    if "site-packages" in _imported_path:
        # Got wrong version - force load from local file
        raise ImportError("Imported from site-packages instead of local project")
except (ImportError, AttributeError) as e:
    # Either import failed or we got wrong version - load explicitly from file
    if not os.path.exists(LOCAL_DB_HELPERS):
        raise ImportError(
            f"Cannot find db_helpers.py at {LOCAL_DB_HELPERS}\n"
            f"Project root: {PROJECT_ROOT}"
        ) from e

    # Load explicitly from local file path
    spec = importlib.util.spec_from_file_location("app.db.db_helpers", LOCAL_DB_HELPERS)
    if not spec or not spec.loader:
        raise ImportError(f"Cannot create spec for {LOCAL_DB_HELPERS}") from e

    # Ensure parent package structure exists
    import types

    if "app" not in sys.modules:
        sys.modules["app"] = types.ModuleType("app")
        sys.modules["app"].__path__ = [LOCAL_APP_DIR]
    if "app.db" not in sys.modules:
        sys.modules["app.db"] = types.ModuleType("app.db")
        sys.modules["app.db"].__path__ = [os.path.join(LOCAL_APP_DIR, "db")]

    # Load the module
    _db_helpers_module = importlib.util.module_from_spec(spec)
    sys.modules["app.db.db_helpers"] = _db_helpers_module
    spec.loader.exec_module(_db_helpers_module)

    # Extract the function we need
    if not hasattr(_db_helpers_module, "store_recipe_in_db"):
        raise ImportError(
            f"store_recipe_in_db not found in {LOCAL_DB_HELPERS}\n"
            f"Available: {dir(_db_helpers_module)}"
        ) from e

    store_recipe_in_db = _db_helpers_module.store_recipe_in_db


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
    session = SessionLocal()
    try:
        # Check for duplicates (case-insensitive)
        existing = session.query(Recipe).filter(Recipe.name.ilike(name)).first()
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
                session.query(Ingredient).filter(Ingredient.name == norm).first()
            )
            if not ingredient:
                ingredient = Ingredient(name=norm)
                session.add(ingredient)
                session.flush()
            recipe.ingredients.append(ingredient)

        session.add(recipe)
        session.commit()
        print(
            f"✅ Recipe '{name}' added successfully with {len(recipe.ingredients)} ingredients (id={recipe.id})."
        )
    except IntegrityError as e:
        session.rollback()
        print(f"❌ Database constraint error: {e}")
        raise
    except OperationalError as e:
        session.rollback()
        print(f"❌ Database connection error: {e}")
        raise
    except SQLAlchemyError as e:
        session.rollback()
        print(f"❌ Database error: {e}")
        raise
    except (AttributeError, TypeError, ValueError) as e:
        session.rollback()
        print(f"❌ Data validation error: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    name, ingredients, steps = read_recipe()
    print(f"You entered {name}\ningredients: {ingredients} \nsteps: {steps}")
    # save_recipe(name, steps, ingredients)
    session = SessionLocal()
    try:
        store_recipe_in_db(
            {"name": name, "steps": steps, "ingredients": ingredients}, session
        )
    finally:
        session.close()
