"""Script for removing duplicate recipes from the database.

This module provides functionality to identify and remove duplicate recipes
based on name matching or other criteria.
"""

import os
import sys
from collections import defaultdict

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
from app.db.models import Recipe  # noqa: E402
from app.db.session import get_db_session  # noqa: E402


def normalize_name(name: str) -> str:
    """Normalize recipe names for duplicate detection.

    Converts recipe names to a standardized format by stripping whitespace
    and converting to lowercase for case-insensitive comparison.

    Args:
        name (str): The original recipe name to normalize

    Returns:
        str: The normalized name (stripped and lowercase)

    Example:
        >>> normalize_name("  Chocolate Cake  ")
        "chocolate cake"
    """
    print(f"Normalizing name: {name}")
    return name.strip().lower()


def find_duplicate_recipes(confirm: bool = True) -> None:
    """Find and remove duplicate recipes from the database.

    Scans all recipes in the database, identifies duplicates based on normalized
    name matching, and optionally removes them. When duplicates are found,
    the first occurrence is kept and subsequent duplicates are deleted.

    Args:
        confirm (bool): Whether to prompt for user confirmation before deletion.
                       Defaults to True for safety.

    Returns:
        None

    Raises:
        SQLAlchemyError: If a database error occurs during the operation.
        IntegrityError: If a database constraint violation occurs.
        OperationalError: If a database connection or operational error occurs.
        ValueError: If invalid data is encountered during processing.

    Note:
        - Normalization is case-insensitive and strips whitespace
        - Database changes are rolled back if any error occurs
        - Prints progress information and duplicate details to console
    """
    with get_db_session() as session:
        try:
            all_recipes = session.query(Recipe).all()

            name_map: dict[str, list[Recipe]] = defaultdict(list)
            for recipe in all_recipes:
                if not recipe.name:
                    continue
                key = normalize_name(recipe.name)
                name_map[key].append(recipe)

            duplicates = {name: recs for name, recs in name_map.items() if len(recs) > 1}

            if not duplicates:
                print("✅ No duplicate recipes found.")
                return

            print("⚠️ Duplicate recipes found:\n")
            for name, recs in duplicates.items():
                print(f"Recipe Name: {name}")
                for r in recs:
                    print(f"  - ID: {r.id}, Ingredients: {len(r.ingredients)}")
                print()
            if confirm:
                choice = (
                    input(
                        "Do you want to delete duplicates and keep one entry for each? (y/N): "
                    )
                    .strip()
                    .lower()
                )
                if choice != "y":
                    print("Aborted. No changes made.")
                    return

            for recs in duplicates.values():
                # to_keep = recs[0]
                to_delete = recs[1:]
                for r in to_delete:
                    session.delete(r)
            session.commit()
            print("✅ Duplicates removed.")
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
            print(f"❌ Data processing error: {e}")
            raise


if __name__ == "__main__":
    find_duplicate_recipes(confirm=True)
