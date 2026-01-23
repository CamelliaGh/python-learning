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
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
