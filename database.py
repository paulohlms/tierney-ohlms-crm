"""
Database configuration and session management.

Uses PostgreSQL for production (hosted environments) or SQLite for local development.
SQLAlchemy provides ORM capabilities and relationship management.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use PostgreSQL if DATABASE_URL is set (production/hosting), otherwise SQLite (local)
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # PostgreSQL (for production/hosting - Render, Railway, etc.)
    # Render provides DATABASE_URL automatically when PostgreSQL is connected
    # Convert postgres:// to postgresql:// (SQLAlchemy requirement)
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    engine = create_engine(DATABASE_URL)
else:
    # SQLite (for local development)
    SQLALCHEMY_DATABASE_URL = "sqlite:///./crm.db"
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

