"""Script to extract recipe data from HTML and store it in the database.

This script processes HTML content containing recipe information, uses OpenAI
to extract structured recipe data (name, ingredients, steps), and stores
the result in the database. It handles module path setup to ensure local
app modules are used instead of any installed packages.
"""
import importlib.util
import os
import sys

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

# Now import from local source
from app.db.session import SessionLocal  # noqa: E402
from app.services.openai_service import call_api  # noqa: E402
from app.tools.openai_response_parser import get_recipe_items  # noqa: E402

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


def extract_and_store_recipe(html_str):
    response = call_api(
        "system_extract_recipe", "user_extract_recipe", {"html": html_str}
    )

    if not response:
        raise ValueError("Failed to extract recipe from HTML.")

    return response


if __name__ == "__main__":
    html_file_path = os.path.join(PROJECT_ROOT, "static", "html", "chocolate_cake.html")
    with open(html_file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    response = extract_and_store_recipe(html_content)
    name, ingredients, steps = get_recipe_items(response)
    session = SessionLocal()
    try:
        store_recipe_in_db(
            {"name": name, "ingredients": ingredients, "steps": steps}, session
        )
    finally:
        session.close()
