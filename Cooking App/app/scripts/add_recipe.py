import os
import sys
from app.db.models import Recipe, Ingredient
from app.db.session import SessionLocal

# Ensure project root is importable when running from ./scripts/
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
    os.chdir(PROJECT_ROOT)


def read_recipe():
    name = read_name()
    ingredients = prompt_for_ingredients()
    steps = prompt_for_steps()
    return name, ingredients, steps


def read_name():
    name = input("🍽️ Recipe name: ").strip()
    if not name:
        print("❌ Recipe name is required.")
        return
    return name


def prompt_for_ingredients():
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
    except Exception as e:
        session.rollback()
        print("❌ Error:", e)
        raise
    finally:
        session.close()


if __name__ == "__main__":
    name, ingredients, steps = read_recipe()
    print(f"You entered {name}\ningredients: {ingredients} \nsteps: {steps}")
    save_recipe(name, steps, ingredients)
