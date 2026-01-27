"""Pytest configuration and fixtures for testing."""

# Use file-based SQLite database for testing (in-memory has connection isolation issues)
import tempfile

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.db.models import Base
from app.db.session import engine as production_engine
from app.db.session import get_db
from main import create_app

_test_db_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
_test_db_file.close()
TEST_DATABASE_URL = f"sqlite:///{_test_db_file.name}"

# Create test engine
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# Patch Base.metadata.create_all BEFORE importing main to prevent
# create_app() from creating tables on production engine during import
_original_create_all = Base.metadata.create_all


def _patched_create_all(bind=None, **kwargs):
    """Patch create_all to use test engine when production engine is used."""
    # If bind is the production engine, redirect to test engine
    if bind is production_engine:
        return _original_create_all(bind=test_engine, **kwargs)
    # Otherwise use the original
    return _original_create_all(bind=bind, **kwargs)


Base.metadata.create_all = _patched_create_all

# Now import main after patching - create_app() will be called at module level
# but our patching will redirect it to use test_engine


# Restore original create_all for use in fixtures (db_session will use it directly)
Base.metadata.create_all = _original_create_all

# Create test session factory
TestSessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    # Drop all tables first to ensure clean state
    Base.metadata.drop_all(bind=test_engine)
    # Create all tables
    Base.metadata.create_all(bind=test_engine)

    # Create a new session
    session = TestSessionLocal()

    try:
        yield session
    finally:
        session.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with overridden database dependency."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app = create_app()
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def sample_recipe_data(db_session):
    """Create sample recipe data for testing."""
    from app.db.models import Ingredient, Recipe, Review

    # Create ingredients
    ingredient1 = Ingredient(name="chicken")
    ingredient2 = Ingredient(name="rice")
    ingredient3 = Ingredient(name="onion")

    db_session.add_all([ingredient1, ingredient2, ingredient3])
    db_session.commit()

    # Create recipe
    recipe = Recipe(
        name="Chicken Rice Bowl", steps="1. Cook chicken\n2. Cook rice\n3. Mix together"
    )
    recipe.ingredients = [ingredient1, ingredient2, ingredient3]

    db_session.add(recipe)
    db_session.commit()

    # Create reviews
    review1 = Review(recipe_id=recipe.id, rating=5)
    review2 = Review(recipe_id=recipe.id, rating=4)
    db_session.add_all([review1, review2])
    db_session.commit()

    return {
        "recipe": recipe,
        "ingredients": [ingredient1, ingredient2, ingredient3],
        "reviews": [review1, review2],
    }
