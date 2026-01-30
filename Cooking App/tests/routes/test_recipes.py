"""Tests for recipe route handlers."""

from unittest.mock import patch

from app.db.models import Ingredient, Recipe, Review
from app.tools.openai_response_parser import RecipeParseError


class TestGetRecipe:
    """Tests for GET /api/recipes/{recipe_id} endpoint."""

    def test_get_recipe_success(self, client, sample_recipe_data):
        """Test successfully retrieving a recipe by ID."""
        recipe = sample_recipe_data["recipe"]
        response = client.get(f"/api/recipes/{recipe.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == recipe.id
        assert data["name"] == recipe.name
        assert data["average_rating"] == 4.5
        assert len(data["ingredients"]) == 3
        assert "chicken" in data["ingredients"]
        assert "rice" in data["ingredients"]
        assert "onion" in data["ingredients"]

    def test_get_recipe_not_found(self, client, db_session):
        """Test retrieving a non-existent recipe."""
        response = client.get("/api/recipes/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Recipe not found"


class TestGetAllRecipesPaginated:
    """Tests for GET /api/recipes endpoint."""

    def test_get_all_recipes_default_pagination(self, client, db_session):
        """Test getting recipes with default pagination."""

        # Create multiple recipes
        ingredient = Ingredient(name="flour")
        db_session.add(ingredient)
        db_session.commit()

        for i in range(15):
            recipe = Recipe(name=f"Recipe {i}", steps=f"Steps {i}")
            recipe.ingredients = [ingredient]
            db_session.add(recipe)
        db_session.commit()

        response = client.get("/api/recipes")

        assert response.status_code == 200
        data = response.json()
        assert len(data["recipes"]) == 10  # Default per_page
        assert data["total"] == 15
        assert data["page"] == 1
        assert data["per_page"] == 10
        assert data["has_next"] is True
        assert data["has_prev"] is False

    def test_get_all_recipes_custom_pagination(self, client, db_session):
        """Test getting recipes with custom pagination."""

        ingredient = Ingredient(name="flour")
        db_session.add(ingredient)
        db_session.commit()

        for i in range(5):
            recipe = Recipe(name=f"Recipe {i}", steps=f"Steps {i}")
            recipe.ingredients = [ingredient]
            db_session.add(recipe)
        db_session.commit()

        response = client.get("/api/recipes?page=2&per_page=2")

        assert response.status_code == 200
        data = response.json()
        assert len(data["recipes"]) == 2
        assert data["page"] == 2
        assert data["per_page"] == 2
        assert data["has_next"] is True
        assert data["has_prev"] is True

    def test_get_all_recipes_empty(self, client, db_session):
        """Test getting recipes when database is empty."""
        response = client.get("/api/recipes")

        assert response.status_code == 200
        data = response.json()
        assert len(data["recipes"]) == 0
        assert data["total"] == 0

    def test_get_all_recipes_invalid_page(self, client):
        """Test pagination with invalid page number."""
        response = client.get("/api/recipes?page=0")

        assert response.status_code == 422

    def test_get_all_recipes_invalid_per_page(self, client):
        """Test pagination with per_page exceeding maximum."""
        response = client.get("/api/recipes?per_page=101")

        assert response.status_code == 422


class TestGetRecipeSteps:
    """Tests for GET /api/recipes/{recipe_id}/steps endpoint."""

    def test_get_recipe_steps_success(self, client, sample_recipe_data):
        """Test successfully retrieving recipe steps as array."""
        recipe = sample_recipe_data["recipe"]
        response = client.get(f"/api/recipes/{recipe.id}/steps")

        assert response.status_code == 200
        data = response.json()
        assert data["recipe_id"] == recipe.id
        assert data["name"] == recipe.name
        assert isinstance(data["steps"], list)
        assert len(data["steps"]) == 3
        # Steps include the number prefix, so check for the actual format
        assert any("Cook chicken" in step for step in data["steps"])

    def test_get_recipe_steps_not_found(self, client, db_session):
        """Test retrieving steps for non-existent recipe."""
        response = client.get("/api/recipes/999/steps")

        assert response.status_code == 404
        assert response.json()["detail"] == "Recipe not found"

    def test_get_recipe_steps_empty(self, client, db_session):
        """Test retrieving steps for recipe with no steps."""

        recipe = Recipe(name="No Steps Recipe", steps=None)
        db_session.add(recipe)
        db_session.commit()

        response = client.get(f"/api/recipes/{recipe.id}/steps")

        assert response.status_code == 200
        data = response.json()
        assert data["steps"] == []


class TestGetRecipesByIngredients:
    """Tests for POST /api/recipes/by-ingredients endpoint."""

    def test_get_recipes_by_ingredients_success(self, client, sample_recipe_data):
        """Test finding recipes by ingredients."""
        response = client.post(
            "/api/recipes/by-ingredients", json={"ingredients": ["chicken", "rice"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Chicken Rice Bowl"
        assert "chicken" in data[0]["ingredients"]
        assert "rice" in data[0]["ingredients"]

    def test_get_recipes_by_ingredients_no_match(self, client, db_session):
        """Test finding recipes with ingredients that don't exist."""
        response = client.post(
            "/api/recipes/by-ingredients", json={"ingredients": ["unicorn", "dragon"]}
        )

        assert response.status_code == 200
        assert response.json() == []

    def test_get_recipes_by_ingredients_missing_field(self, client):
        """Test request with missing ingredients field."""
        # FastAPI returns 422 for validation errors (missing required field)
        response = client.post("/api/recipes/by-ingredients", json={})

        assert response.status_code == 422  # FastAPI validation error

    def test_get_recipes_by_ingredients_empty_list(self, client):
        """Test request with empty ingredients list."""
        response = client.post("/api/recipes/by-ingredients", json={"ingredients": []})

        assert response.status_code == 400
        # The error message could be "empty" or "missing"
        detail = response.json()["detail"].lower()
        assert "empty" in detail or "missing" in detail

    def test_get_recipes_by_ingredients_case_insensitive(
        self, client, sample_recipe_data
    ):
        """Test that ingredient search is case-insensitive."""
        response = client.post(
            "/api/recipes/by-ingredients", json={"ingredients": ["CHICKEN", "Rice"]}
        )

        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_get_recipes_by_ingredients_whitespace_only(self, client):
        """Test request with ingredients list containing only whitespace."""
        response = client.post(
            "/api/recipes/by-ingredients", json={"ingredients": ["   ", "\t"]}
        )

        assert response.status_code == 400
        assert "empty" in response.json()["detail"].lower()


class TestGetRandomRecipe:
    """Tests for GET /api/recipes/random endpoint."""

    def test_get_random_recipe_success(self, client, sample_recipe_data):
        """Test successfully retrieving a random recipe."""
        response = client.get("/api/recipes/random")

        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "name" in data
        assert "ingredients" in data

    def test_get_random_recipe_not_found(self, client, db_session):
        """Test retrieving random recipe when database is empty."""
        response = client.get("/api/recipes/random")

        assert response.status_code == 404
        assert response.json()["detail"] == "No recipes found"


class TestGetPopularRecipes:
    """Tests for GET /api/recipes/popular endpoint."""

    def test_get_popular_recipes_success(self, client, sample_recipe_data, db_session):
        """Test successfully retrieving popular recipes."""
        # Create another recipe with lower rating
        ingredient = Ingredient(name="pasta")
        db_session.add(ingredient)
        db_session.commit()

        recipe2 = Recipe(name="Pasta Dish", steps="Cook pasta")
        recipe2.ingredients = [ingredient]
        db_session.add(recipe2)
        db_session.commit()

        review = Review(recipe_id=recipe2.id, rating=3)
        db_session.add(review)
        db_session.commit()

        response = client.get("/api/recipes/popular")

        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        # Should be ordered by rating descending
        assert data[0]["average_rating"] >= data[-1]["average_rating"]

    def test_get_popular_recipes_not_found(self, client, db_session):
        """Test retrieving popular recipes when none exist."""
        response = client.get("/api/recipes/popular")

        assert response.status_code == 404
        assert response.json()["detail"] == "No recipes found"


class TestGenerateRecipe:
    """Tests for POST /api/recipes/generate endpoint."""

    @patch("app.routes.recipes.openai")
    def test_generate_recipe_success(self, mock_openai, client):
        """Test successfully generating a recipe."""
        # Mock OpenAI response
        mock_response = """Name: Test Recipe
Ingredients:
- ingredient1
- ingredient2
Steps:
1. Step one
2. Step two"""
        mock_openai.return_value = mock_response

        response = client.post(
            "/api/recipes/generate", json={"ingredients": ["chicken", "rice"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Recipe"
        assert len(data["ingredients"]) == 2
        assert len(data["steps"]) == 2
        mock_openai.assert_called_once()

    def test_generate_recipe_no_ingredients(self, client):
        """Test generating recipe with no ingredients."""
        response = client.post("/api/recipes/generate", json={"ingredients": []})

        assert response.status_code == 400
        assert "ingredients" in response.json()["detail"].lower()

    @patch("app.routes.recipes.openai")
    def test_generate_recipe_api_failure(self, mock_openai, client):
        """Test handling OpenAI API failure."""
        mock_openai.return_value = None

        response = client.post(
            "/api/recipes/generate", json={"ingredients": ["chicken"]}
        )

        assert response.status_code == 500
        assert "Failed to generate recipe" in response.json()["detail"]

    @patch("app.routes.recipes.openai")
    @patch("app.routes.recipes.openai_parser.get_recipe_items")
    def test_generate_recipe_invalid_format(self, mock_parser, mock_openai, client):
        """Test handling invalid recipe format from AI."""
        mock_openai.return_value = "Some response"
        # Make parser raise an exception to simulate invalid format
        mock_parser.side_effect = Exception("Parse error")

        response = client.post(
            "/api/recipes/generate", json={"ingredients": ["chicken"]}
        )

        # Should handle the exception and return 500
        assert response.status_code == 500
        assert "Invalid recipe format" in response.json()["detail"]

    @patch("app.routes.recipes.openai")
    @patch("app.routes.recipes.openai_parser.get_recipe_items")
    def test_generate_recipe_parse_error(self, mock_parser, mock_openai, client):
        """Test handling RecipeParseError from parser."""
        mock_openai.return_value = "Malformed response"
        mock_parser.side_effect = RecipeParseError("Invalid name format")

        response = client.post(
            "/api/recipes/generate", json={"ingredients": ["chicken"]}
        )

        assert response.status_code == 500
        assert "Failed to parse AI response" in response.json()["detail"]

    @patch("app.routes.recipes.openai")
    @patch("app.routes.recipes.openai_parser.get_recipe_items")
    def test_generate_recipe_invalid_response_format(self, mock_parser, mock_openai, client):
        """Test handling TypeError/ValueError from parser (invalid AI response format)."""
        mock_openai.return_value = "Some response"
        mock_parser.side_effect = ValueError("Invalid structure")

        response = client.post(
            "/api/recipes/generate", json={"ingredients": ["chicken"]}
        )

        assert response.status_code == 500
        assert "Invalid response format" in response.json()["detail"]

    def test_generate_recipe_missing_body(self, client):
        """Test generating recipe with missing request body."""
        response = client.post("/api/recipes/generate")

        assert response.status_code == 422
