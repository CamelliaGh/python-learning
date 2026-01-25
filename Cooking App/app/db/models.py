"""Database models for the Cooking App.

This module defines the SQLAlchemy ORM models for recipes, ingredients, and reviews,
including the many-to-many relationship between recipes and ingredients.
"""

from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship

from app.db.session import Base, engine

recipe_ingredient = Table(
    "recipe_ingredient",
    Base.metadata,
    Column(
        "recipe_id",
        Integer,
        ForeignKey("recipe.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "ingredient_id",
        Integer,
        ForeignKey("ingredient.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Ingredient(Base):
    """Ingredient model for storing recipe ingredients.
    
    Represents an ingredient that can be used in multiple recipes.
    Has a many-to-many relationship with Recipe through the recipe_ingredient table.
    
    Attributes:
        id (int): Primary key for the ingredient
        name (str): Name of the ingredient (max 50 characters)
        recipes (List[Recipe]): List of recipes that use this ingredient
    """
    __tablename__ = "ingredient"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=True)

    recipes = relationship(
        "Recipe",
        secondary=recipe_ingredient,
        back_populates="ingredients",
        passive_deletes=True,
    )


class Recipe(Base):
    """Recipe model for storing cooking recipes.
    
    Represents a recipe with ingredients, preparation steps, and associated reviews.
    Has many-to-many relationships with ingredients and one-to-many with reviews.
    
    Attributes:
        id (int): Primary key for the recipe
        name (str): Name of the recipe (max 100 characters)
        steps (str): Detailed cooking instructions/steps
        ingredients (List[Ingredient]): List of ingredients needed for this recipe
        reviews (List[Review]): List of reviews for this recipe
    """
    __tablename__ = "recipe"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=True)
    steps = Column(Text, nullable=True)

    ingredients = relationship(
        "Ingredient",
        secondary=recipe_ingredient,
        back_populates="recipes",
        passive_deletes=True,
    )

    reviews = relationship(
        "Review",
        back_populates="recipe",
        passive_deletes=True,
    )


class Review(Base):
    """Review model for storing recipe ratings and feedback.
    
    Represents a user review for a specific recipe. Each review is linked
    to a recipe through a foreign key relationship.
    
    Attributes:
        id (int): Primary key for the review
        recipe_id (int): Foreign key linking to the recipe being reviewed
        rating (int): Numerical rating for the recipe
        recipe (Recipe): The recipe this review belongs to
    """
    __tablename__ = "review"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(
        Integer,
        ForeignKey("recipe.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    rating = Column(Integer, nullable=True)

    recipe = relationship("Recipe", back_populates="reviews")


if __name__ == "__main__":
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables created")
    except SQLAlchemyError as e:
        print(f"Error creating tables: {e}")
