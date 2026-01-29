"""Script to extract recipe data from HTML and store it in the database.

This script processes HTML content containing recipe information, uses OpenAI
to extract structured recipe data (name, ingredients, steps), and stores
the result in the database. It handles module path setup to ensure local
app modules are used instead of any installed packages.
"""

import os
import sys

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
from app.db.session import get_db_session  # noqa: E402
from app.services.openai_service import call_api  # noqa: E402
from app.tools.openai_response_parser import get_recipe_items  # noqa: E402


def extract_and_store_recipe(html_str):
    """Extract and store a recipe from HTML content.

    Args:
        html_str: The HTML content to extract the recipe from.

    Returns:
        dict: The extracted recipe data.
    """
    api_response = call_api(
        "system_extract_recipe", "user_extract_recipe", {"html": html_str}
    )

    if not api_response:
        raise ValueError("Failed to extract recipe from HTML.")

    return api_response


if __name__ == "__main__":
    html_file_path = os.path.join(
        _PROJECT_ROOT, "static", "html", "chocolate_cake.html"
    )
    with open(html_file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    response = extract_and_store_recipe(html_content)
    name, ingredients, steps = get_recipe_items(response)
    with get_db_session() as session:
        store_recipe_in_db(
            {"name": name, "ingredients": ingredients, "steps": steps}, session
        )
