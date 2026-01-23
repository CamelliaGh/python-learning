from __future__ import annotations

import sys
import os

from app.db.session import SessionLocal
from app.db.models import Recipe, Ingredient, Review, recipe_ingredient

# Adjust sys.path so "app" is importable when run directly
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if PROJECT_ROOT not in sys.path:
    os.chdir(PROJECT_ROOT)
    sys.path.insert(0, PROJECT_ROOT)


def reset_database():
    confirm = input("⚠️ This will delete ALL recipes, ingredients, and reviews. Are you sure? (y/N): ")
    if confirm.lower() != 'y':
        print("Aborted.")
        return
    print("🔄 Deleting data...")

    session = SessionLocal()
    try:
            # Delete association table entries first
            session.execute(recipe_ingredient.delete())

            # Then delete dependent tables
            session.query(Review).delete()
            session.query(Recipe).delete()
            session.query(Ingredient).delete()

            session.commit()
            print("✅ Database reset complete!")
    except Exception as e:
            session.rollback()
            print(f"❌ Error: {e}")
    finally:
            session.close()


if __name__ == "__main__":
    reset_database()
