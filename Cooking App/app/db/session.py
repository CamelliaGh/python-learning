"""Database session management for the Cooking App.

This module handles database connection setup, session creation, and provides
a dependency injection function for FastAPI route handlers.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from typing import Generator


DATABASE_URL = "sqlite:///./recipes.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()



def get_db() -> Generator:
    """Create and manage a database session for dependency injection.
    
    This function is used as a FastAPI dependency to provide database sessions
    to route handlers. It ensures the session is properly closed after use.
    
    Yields:
        Session: A SQLAlchemy database session object.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
