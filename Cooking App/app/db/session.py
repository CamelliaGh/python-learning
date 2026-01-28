"""Database session management for the Cooking App.

This module handles database connection setup, session creation, and provides
a dependency injection function for FastAPI route handlers and a context manager
for scripts.
"""

from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, scoped_session, sessionmaker

from app.config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {},
)

_SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Base = declarative_base()


def get_db() -> Generator:
    """Create and manage a database session for dependency injection.

    This function is used as a FastAPI dependency to provide database sessions
    to route handlers. It ensures the session is properly closed after use.

    Yields:
        Session: A SQLAlchemy database session object.
    """
    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """Context manager for database sessions in scripts.

    Use this function in scripts instead of calling SessionLocal() directly.
    It ensures the session is properly closed after use.

    Yields:
        Session: A SQLAlchemy database session object.

    Example:
        with get_db_session() as session:
            recipes = session.query(Recipe).all()
    """
    session = _SessionLocal()
    try:
        yield session
    finally:
        session.close()
