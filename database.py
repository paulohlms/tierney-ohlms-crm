"""
Database configuration and session management.

Uses SQLite for simplicity - perfect for a small internal tool.
SQLAlchemy provides ORM capabilities and relationship management.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database file - stored in project root
SQLALCHEMY_DATABASE_URL = "sqlite:///./crm.db"

# Create engine with check_same_thread=False for SQLite compatibility with FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Session factory - each request will create a new session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()


def get_db():
    """
    Dependency function for FastAPI to get database session.
    Ensures proper session cleanup after request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

