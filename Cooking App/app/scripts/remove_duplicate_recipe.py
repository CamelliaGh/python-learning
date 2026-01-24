"""Script for removing duplicate recipes from the database.

This module provides functionality to identify and remove duplicate recipes
based on name matching or other criteria.
"""

import os
import sys
from collections import defaultdict

from sqlalchemy.orm import Session

from app.db.models import Recipe
from app.db.session import SessionLocal

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if PROJECT_ROOT not in sys.path:
    os.chdir(PROJECT_ROOT)
    sys.path.insert(0, PROJECT_ROOT)


def normalize_name(name: str) -> str:
    print(f"Normalizing name: {name}")
    return name.strip().lower()


def find_duplicate_recipes(confirm: bool = True) -> None:
    session: Session = SessionLocal()
    try:
        all_recipes = session.query(Recipe).all()

        name_map: dict[str, list[Recipe]] = defaultdict(list)
        for recipe in all_recipes:
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
    except Exception as e:
        session.rollback()
        print("❌ Error:", e)
        raise
    finally:
        session.close()


if __name__ == "__main__":
    find_duplicate_recipes(confirm=True)
