"""
Database connection and session management.

Uses SQLAlchemy ORM for database operations.
All database operations are managed through session contexts.

NOTE: Kept synchronous for backward compatibility with existing code.
Revenue calculation uses async wrapper to prevent blocking.
"""
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

# Initialize engine with connection pooling and error handling
if DATABASE_URL:
    # PostgreSQL (for production on Render)
    # Convert postgres:// to postgresql:// if needed
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
    elif DATABASE_URL.startswith("postgresql://"):
        # Use psycopg driver (version 3) instead of psycopg2 (Python 3.13 compatible)
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)
    
    try:
        # PostgreSQL engine with optimized connection pooling
        engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,      # Verify connections before using
            pool_recycle=300,        # Recycle connections after 5 minutes
            pool_size=20,            # Increased pool size for better concurrency
            max_overflow=40,          # Allow overflow connections under load
            pool_timeout=30,         # Timeout for getting connection from pool
            echo=False,              # Set to True for SQL debugging
            connect_args={
                "connect_timeout": 10,  # Connection timeout
                "application_name": "tierney_ohlms_crm"
            }
        )
        logger.info("Database engine created: PostgreSQL")
    except Exception as e:
        logger.error(f"Failed to create PostgreSQL engine: {e}")
        raise
else:
    # SQLite (for local development)
    SQLALCHEMY_DATABASE_URL = "sqlite:///./crm.db"
    try:
        engine = create_engine(
            SQLALCHEMY_DATABASE_URL,
            connect_args={"check_same_thread": False},
            echo=False  # Set to True for SQL debugging
        )
        logger.info("Database engine created: SQLite")
    except Exception as e:
        logger.error(f"Failed to create SQLite engine: {e}")
        raise

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency for getting database session.
    
    Uses context manager pattern - session is automatically closed after use.
    All database operations should use this function via FastAPI dependency injection.
    
    Example:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Database error in session: {e}", exc_info=True)
        db.rollback()
        raise
    except Exception as e:
        logger.error(f"Unexpected error in database session: {e}", exc_info=True)
        db.rollback()
        raise
    finally:
        db.close()

