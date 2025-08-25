"""
Database configuration and session management.
This sets up SQLAlchemy for our SQLite database.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create database engine
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}  # Only needed for SQLite
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our database models
Base = declarative_base()

def get_db():
    """
    Dependency function to get database session.
    FastAPI will use this to inject database sessions into endpoints.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()