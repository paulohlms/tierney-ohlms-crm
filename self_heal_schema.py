"""
Self-Healing Schema Migration

This module provides a function that automatically fixes missing columns
in the timesheets table on application startup.

It is idempotent and can be run multiple times safely.
"""
import logging
from typing import Tuple, List
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from database import engine

logger = logging.getLogger(__name__)

# Required columns for timesheets table (from models.py)
REQUIRED_TIMESHEET_COLUMNS = {
    'staff_member': "VARCHAR NOT NULL DEFAULT 'Unknown'",
    'entry_date': "DATE NOT NULL DEFAULT CURRENT_DATE",
    'start_time': 'VARCHAR',
    'end_time': 'VARCHAR',
    'hours': 'DOUBLE PRECISION NOT NULL DEFAULT 0',
    'project_task': 'VARCHAR',
    'description': 'TEXT',
    'billable': 'BOOLEAN DEFAULT TRUE',
    'created_at': 'TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP',
    'updated_at': 'TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP'
}


def check_column_exists(conn, table_name: str, column_name: str) -> bool:
    """Check if a column exists using direct SQL query."""
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


def self_heal_timesheets_schema() -> Tuple[bool, List[str]]:
    """
    Self-healing migration for timesheets table.
    
    Automatically adds any missing columns to match the Timesheet model.
    This function is idempotent - can be run multiple times safely.
    
    Returns:
        (success, list of added columns)
    """
    logger.info("[SELF-HEAL] Starting self-healing schema migration for timesheets...")
    
    added_columns = []
    
    try:
        with engine.begin() as conn:
            # Check if timesheets table exists
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_name = 'timesheets'
            """))
            if not result.fetchone():
                logger.warning("[SELF-HEAL] Table 'timesheets' does not exist - will be created by Base.metadata.create_all")
                return True, []
            
            # Check and add missing columns
            for col_name, col_def in REQUIRED_TIMESHEET_COLUMNS.items():
                if check_column_exists(conn, 'timesheets', col_name):
                    logger.debug(f"[SELF-HEAL] Column 'timesheets.{col_name}' already exists")
                    continue
                
                try:
                    sql = f"ALTER TABLE timesheets ADD COLUMN {col_name} {col_def}"
                    logger.info(f"[SELF-HEAL] Adding column 'timesheets.{col_name}'...")
                    conn.execute(text(sql))
                    
                    # Verify it was added
                    if check_column_exists(conn, 'timesheets', col_name):
                        logger.info(f"[SELF-HEAL] ✓ Successfully added column 'timesheets.{col_name}'")
                        added_columns.append(col_name)
                    else:
                        logger.error(f"[SELF-HEAL] ✗ Column 'timesheets.{col_name}' was not added")
                        return False, added_columns
                        
                except Exception as e:
                    error_msg = str(e).lower()
                    if 'duplicate' in error_msg or 'already exists' in error_msg or '42701' in error_msg:
                        logger.info(f"[SELF-HEAL] Column 'timesheets.{col_name}' already exists (race condition)")
                    else:
                        logger.error(f"[SELF-HEAL] Failed to add column 'timesheets.{col_name}': {e}")
                        return False, added_columns
            
            # Final verification
            missing = []
            for col_name in REQUIRED_TIMESHEET_COLUMNS.keys():
                if not check_column_exists(conn, 'timesheets', col_name):
                    missing.append(col_name)
            
            if missing:
                logger.error(f"[SELF-HEAL] ✗ Missing columns after migration: {missing}")
                return False, added_columns
            
            if added_columns:
                logger.info(f"[SELF-HEAL] ✓ Self-healing complete: Added {len(added_columns)} column(s): {', '.join(added_columns)}")
            else:
                logger.info("[SELF-HEAL] ✓ All columns already exist - no migration needed")
            
            return True, added_columns
            
    except SQLAlchemyError as e:
        logger.error(f"[SELF-HEAL] Database error during self-healing: {e}", exc_info=True)
        return False, added_columns
    except Exception as e:
        logger.error(f"[SELF-HEAL] Unexpected error during self-healing: {e}", exc_info=True)
        return False, added_columns


def self_heal_all_schema() -> bool:
    """
    Self-healing migration for all tables.
    
    Currently focuses on timesheets, but can be extended for other tables.
    """
    success, added = self_heal_timesheets_schema()
    return success

