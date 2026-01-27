"""Configuration settings for the Cooking App.

This module centralizes all magic numbers, strings, and configuration values
used throughout the application, making them easier to maintain and modify.

Values can be overridden via environment variables (loaded from .env file).
Environment-specific or sensitive values should be set in .env.
Application constants and defaults are defined here and committed to git.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / ".env"
if not env_path.exists():
    env_path = Path.cwd() / ".env"
load_dotenv(env_path)

# HTTP Status Codes
HTTP_STATUS_OK = 200
HTTP_STATUS_BAD_REQUEST = 400
HTTP_STATUS_NOT_FOUND = 404
HTTP_STATUS_INTERNAL_SERVER_ERROR = 500
HTTP_STATUS_UNPROCESSABLE_ENTITY = 422

# Pagination Settings
# Can be overridden via PAGINATION_* env vars
PAGINATION_DEFAULT_PAGE = int(os.getenv("PAGINATION_DEFAULT_PAGE", "1"))
PAGINATION_DEFAULT_PER_PAGE = int(os.getenv("PAGINATION_DEFAULT_PER_PAGE", "10"))
PAGINATION_MAX_PER_PAGE = int(os.getenv("PAGINATION_MAX_PER_PAGE", "100"))
PAGINATION_MIN_PAGE = int(os.getenv("PAGINATION_MIN_PAGE", "1"))
PAGINATION_MIN_PER_PAGE = int(os.getenv("PAGINATION_MIN_PER_PAGE", "1"))

# Popular Recipes Settings
# Can be overridden via POPULAR_RECIPES_LIMIT env var
POPULAR_RECIPES_DEFAULT_LIMIT = int(os.getenv("POPULAR_RECIPES_LIMIT", "10"))

# Rating Settings
RATING_DECIMAL_PLACES = 2

# OpenAI API Settings
# Can be overridden via OPENAI_MODEL and OPENAI_TEMPERATURE env vars
OPENAI_DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
OPENAI_DEFAULT_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))

# Prompt Template Settings
PROMPT_SYSTEM_RECIPE_PROMPT = "system_recipe_prompt"
PROMPT_USER_RECIPE_PROMPT = "user_recipe_prompt"
PROMPT_FILE_EXTENSION = ".txt"

# Directory and Path Settings
STATIC_DIRECTORY = os.getenv("STATIC_DIRECTORY", "static")
PROMPTS_DIRECTORY = os.getenv("PROMPTS_DIRECTORY", "prompts")
API_PREFIX = os.getenv("API_PREFIX", "/api")

# CORS Settings
# Can be overridden via CORS_ALLOW_ORIGINS env var (comma-separated)
_cors_origins = os.getenv("CORS_ALLOW_ORIGINS", "*")
CORS_ALLOW_ORIGINS = _cors_origins.split(",") if _cors_origins != "*" else ["*"]
CORS_ALLOW_METHODS = (
    os.getenv("CORS_ALLOW_METHODS", "*").split(",")
    if os.getenv("CORS_ALLOW_METHODS")
    else ["*"]
)
CORS_ALLOW_HEADERS = (
    os.getenv("CORS_ALLOW_HEADERS", "*").split(",")
    if os.getenv("CORS_ALLOW_HEADERS")
    else ["*"]
)

# Database Settings
# Can be overridden via DATABASE_URL env var
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./recipes.db")

# Database Field Lengths
DB_RECIPE_NAME_MAX_LENGTH = 100
DB_INGREDIENT_NAME_MAX_LENGTH = 50

# Error Messages
ERROR_RECIPE_NOT_FOUND = "Recipe not found"
ERROR_NO_RECIPES_FOUND = "No recipes found"
ERROR_MISSING_INGREDIENTS = 'Missing "ingredients" in request'
ERROR_EMPTY_INGREDIENTS_LIST = "Empty ingredients list"
ERROR_NO_INGREDIENTS_PROVIDED = "No ingredients provided"
ERROR_FAILED_TO_GENERATE_RECIPE = "Failed to generate recipe"
ERROR_FAILED_TO_PARSE_AI_RESPONSE = "Failed to parse AI response: {error}"
ERROR_INVALID_AI_RESPONSE_FORMAT = "Invalid response format from AI: {error}"
ERROR_INVALID_RECIPE_FORMAT = "Invalid recipe format"

# Parser Settings
PARSER_MIN_PARTS_FOR_NAME = 2
PARSER_STEP_PREFIX_CHECK_LENGTH = 2
