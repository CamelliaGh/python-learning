"""Script for resetting the database by deleting all data.

This script provides a safe way to clear all recipes, ingredients, and reviews
from the database. It requires user confirmation before proceeding and handles
foreign key constraints properly.
"""

from __future__ import annotations

import os
import sys

from sqlalchemy.exc import SQLAlchemyError

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
from app.db.models import Ingredient, Recipe, Review, recipe_ingredient  # noqa: E402
from app.db.session import get_db_session  # noqa: E402


def reset_database() -> None:
    """Reset the database by deleting all recipes, ingredients, and reviews.

    Completely clears the database by removing all data from recipes, ingredients,
    reviews, and their associations. Prompts for user confirmation before proceeding
    and handles foreign key constraints by deleting in the correct order.

    Returns:
        None

    Raises:
        SQLAlchemyError: If database operations fail, changes are rolled back

    Note:
        - Requires user confirmation (type 'y') before deletion
        - Deletes association table entries first to avoid constraint violations
        - All changes are committed as a single transaction
        - Database session is properly closed regardless of success/failure

    Warning:
        This operation is irreversible and will permanently delete all data!
    """
    confirm = input(
        "⚠️ This will delete ALL recipes, ingredients, and reviews. Are you sure? (y/N): "
    )
    if confirm.lower() != "y":
        print("Aborted.")
        return
    print("🔄 Deleting data...")

    with get_db_session() as session:
        try:
            # Delete association table entries first
            session.execute(recipe_ingredient.delete())

            # Then delete dependent tables
            session.query(Review).delete()
            session.query(Recipe).delete()
            session.query(Ingredient).delete()

            session.commit()
            print("✅ Database reset complete!")
        except SQLAlchemyError as e:
            session.rollback()
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    reset_database()
