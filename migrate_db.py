"""
Comprehensive Database Migration Script

This script ensures the PostgreSQL database schema matches SQLAlchemy models exactly.
It is idempotent - can be run multiple times safely.

Usage:
    python migrate_db.py

Or set DATABASE_URL environment variable:
    DATABASE_URL=postgresql://... python migrate_db.py
"""
import os
import sys
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_database_url():
    """
    Get database URL from environment, handling postgres:// vs postgresql:// prefix.
    
    Render and some other services use postgres:// but SQLAlchemy 2.0+ requires postgresql://
    """
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        logger.error("DATABASE_URL environment variable not set")
        sys.exit(1)
    
    # Fix postgres:// to postgresql:// for SQLAlchemy 2.0+
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
        logger.info("Converted postgres:// to postgresql:// for SQLAlchemy compatibility")
    
    return database_url


def check_column_exists(conn, table_name: str, column_name: str) -> bool:
    """
    Check if a column exists in a table using direct SQL query.
    
    This is more reliable than using SQLAlchemy inspector which may have stale cache.
    """
    try:
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_schema = 'public' 
            AND table_name = :table_name 
            AND column_name = :column_name
        """), {"table_name": table_name, "column_name": column_name})
        return result.fetchone() is not None
    except Exception as e:
        logger.warning(f"Error checking column {table_name}.{column_name}: {e}")
        return False


def migrate_timesheets_table(conn) -> bool:
    """
    Migrate timesheets table to match Timesheet model exactly.
    
    Expected columns from models.py:
    - id (INTEGER PRIMARY KEY) - should already exist
    - client_id (INTEGER NOT NULL) - should already exist
    - staff_member (VARCHAR NOT NULL) - MISSING - needs default 'Unknown'
    - entry_date (DATE NOT NULL) - MISSING - needs default CURRENT_DATE
    - start_time (VARCHAR) - optional
    - end_time (VARCHAR) - optional
    - hours (DOUBLE PRECISION NOT NULL) - MISSING - needs default 0
    - project_task (VARCHAR) - optional
    - description (TEXT) - optional
    - billable (BOOLEAN) - MISSING - needs default TRUE
    - created_at (TIMESTAMP WITH TIME ZONE) - MISSING
    - updated_at (TIMESTAMP WITH TIME ZONE) - MISSING
    
    Returns:
        True if migration succeeded, False otherwise
    """
    logger.info("=" * 70)
    logger.info("MIGRATING TIMESHEETS TABLE")
    logger.info("=" * 70)
    
    # Define all required columns with their SQL definitions
    # Based on Timesheet model in models.py
    required_columns = {
        'staff_member': {
            'type': 'VARCHAR NOT NULL DEFAULT \'Unknown\'',
            'description': 'Name of staff member who logged time'
        },
        'entry_date': {
            'type': 'DATE NOT NULL DEFAULT CURRENT_DATE',
            'description': 'Date when work was performed'
        },
        'start_time': {
            'type': 'VARCHAR',
            'description': 'Start time (HH:MM format)'
        },
        'end_time': {
            'type': 'VARCHAR',
            'description': 'End time (HH:MM format)'
        },
        'hours': {
            'type': 'DOUBLE PRECISION NOT NULL DEFAULT 0',
            'description': 'Total hours (decimal, e.g., 1.5)'
        },
        'project_task': {
            'type': 'VARCHAR',
            'description': 'Project or task name'
        },
        'description': {
            'type': 'TEXT',
            'description': 'Notes/description of work performed'
        },
        'billable': {
            'type': 'BOOLEAN DEFAULT TRUE',
            'description': 'Whether this time is billable to client'
        },
        'created_at': {
            'type': 'TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP',
            'description': 'Creation timestamp'
        },
        'updated_at': {
            'type': 'TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP',
            'description': 'Last update timestamp'
        }
    }
    
    success_count = 0
    error_count = 0
    
    for col_name, col_def in required_columns.items():
        # Check if column already exists
        if check_column_exists(conn, 'timesheets', col_name):
            logger.info(f"✓ Column 'timesheets.{col_name}' already exists - skipping")
            success_count += 1
            continue
        
        try:
            # PostgreSQL doesn't support IF NOT EXISTS for ALTER TABLE ADD COLUMN
            # So we check first, then add if missing
            sql = f"ALTER TABLE timesheets ADD COLUMN {col_name} {col_def['type']}"
            logger.info(f"Adding column 'timesheets.{col_name}' ({col_def['description']})...")
            conn.execute(text(sql))
            conn.commit()
            
            # Verify the column was actually added
            if check_column_exists(conn, 'timesheets', col_name):
                logger.info(f"✓ Successfully added column 'timesheets.{col_name}'")
                success_count += 1
            else:
                logger.error(f"✗ Column 'timesheets.{col_name}' was not added successfully")
                error_count += 1
                
        except Exception as e:
            error_msg = str(e).lower()
            # PostgreSQL error codes: 42701 = duplicate_column
            if 'duplicate' in error_msg or 'already exists' in error_msg or '42701' in error_msg:
                logger.info(f"✓ Column 'timesheets.{col_name}' already exists (detected via error)")
                success_count += 1
            else:
                logger.error(f"✗ Failed to add column 'timesheets.{col_name}': {e}")
                conn.rollback()
                error_count += 1
    
    # Final verification
    logger.info("")
    logger.info("Verifying all columns exist...")
    missing_columns = []
    for col_name in required_columns.keys():
        if not check_column_exists(conn, 'timesheets', col_name):
            missing_columns.append(col_name)
    
    if missing_columns:
        logger.error(f"✗ Missing columns after migration: {missing_columns}")
        return False
    
    logger.info("=" * 70)
    logger.info(f"TIMESHEETS MIGRATION COMPLETE")
    logger.info(f"  ✓ Successfully processed: {success_count} columns")
    if error_count > 0:
        logger.warning(f"  ⚠ Errors encountered: {error_count} columns")
    logger.info("=" * 70)
    
    return error_count == 0


def migrate_all_tables(conn):
    """
    Migrate all tables that may have missing columns.
    
    This is a comprehensive migration that ensures all tables match their models.
    """
    logger.info("")
    logger.info("=" * 70)
    logger.info("COMPREHENSIVE DATABASE MIGRATION")
    logger.info("=" * 70)
    logger.info("")
    
    inspector = inspect(conn)
    all_tables = inspector.get_table_names()
    
    # Check if timesheets table exists
    if 'timesheets' not in all_tables:
        logger.warning("⚠ Table 'timesheets' does not exist - will be created by SQLAlchemy models")
        logger.info("  Run Base.metadata.create_all(engine) to create the table first")
        return False
    
    # Migrate timesheets table
    timesheets_success = migrate_timesheets_table(conn)
    
    # Add other table migrations here as needed
    # services_success = migrate_services_table(conn)
    # clients_success = migrate_clients_table(conn)
    
    return timesheets_success


def main():
    """
    Main migration function.
    
    This script is idempotent - it can be run multiple times safely.
    """
    logger.info("=" * 70)
    logger.info("DATABASE MIGRATION SCRIPT")
    logger.info("=" * 70)
    logger.info("")
    
    # Get database URL
    database_url = get_database_url()
    logger.info(f"Connecting to database...")
    
    try:
        # Create engine
        engine = create_engine(
            database_url,
            pool_pre_ping=True,
            pool_recycle=300,
            echo=False  # Set to True for SQL debugging
        )
        
        # Test connection
        with engine.connect() as test_conn:
            test_conn.execute(text("SELECT 1"))
        logger.info("✓ Database connection successful")
        
        # Run migrations
        logger.info("")
        with engine.begin() as conn:
            # Use begin() for proper transaction handling
            success = migrate_all_tables(conn)
        
        if success:
            logger.info("")
            logger.info("=" * 70)
            logger.info("✓ MIGRATION COMPLETED SUCCESSFULLY")
            logger.info("=" * 70)
            return 0
        else:
            logger.error("")
            logger.error("=" * 70)
            logger.error("✗ MIGRATION COMPLETED WITH ERRORS")
            logger.error("=" * 70)
            return 1
            
    except SQLAlchemyError as e:
        logger.error(f"✗ Database error: {e}", exc_info=True)
        return 1
    except Exception as e:
        logger.error(f"✗ Unexpected error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

