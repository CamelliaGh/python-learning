"""Script for exporting all recipes to a CSV file.

This script provides a way to export all recipes from the database to a CSV file.
It uses the get_all_recipes function from the db_helpers module to retrieve all recipes
and then writes them to a CSV file.
"""

import csv
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
from app.db.db_helpers import get_all_recipes  # noqa: E402
from app.db.session import get_db_session  # noqa: E402


def export_to_csv(filename: str = "exported_recipes.csv") -> None:
    """Export all recipes to a CSV file.

    Args:
        filename: The name of the CSV file to create. Defaults to "exported_recipes.csv".
    """
    with get_db_session() as session:
        recipes = get_all_recipes(session)

        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["ID", "Name", "Ingredients", "Steps"])

            for r in recipes:
                ingredient_list = ", ".join(sorted(set(i.name for i in r.ingredients)))
                steps_flat = (r.steps or "").replace("\n", " ")
                writer.writerow([r.id, r.name, ingredient_list, steps_flat])

        print(f"✅ Exported {len(recipes)} recipes to '{filename}'")


if __name__ == "__main__":
    export_to_csv()
