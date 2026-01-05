"""
Comprehensive Schema Fix and Reconciliation System

This module provides:
1. Deep schema inspection comparing models vs actual database
2. Automatic migration generation and application
3. Defensive query helpers that work with incomplete schema
4. Schema validation and reporting

CRITICAL: This ensures the application works even when schema is partially migrated.
"""
import logging
from typing import Dict, List, Set, Tuple, Optional
from sqlalchemy import inspect, text, MetaData
from sqlalchemy.exc import SQLAlchemyError, ProgrammingError
from psycopg.errors import UndefinedColumn
from database import engine
from models import Client, Contact, Service, Task, Note, Timesheet, User

logger = logging.getLogger(__name__)

# Map of table names to model classes
TABLE_MODEL_MAP = {
    'clients': Client,
    'contacts': Contact,
    'services': Service,
    'tasks': Task,
    'notes': Note,
    'timesheets': Timesheet,
    'users': User
}

# Expected columns per table (from models.py)
EXPECTED_COLUMNS = {
    'clients': {
        'id': 'INTEGER PRIMARY KEY',
        'legal_name': 'VARCHAR NOT NULL',
        'entity_type': 'VARCHAR',
        'fiscal_year_end': 'VARCHAR',
        'status': 'VARCHAR NOT NULL',
        'owner_name': 'VARCHAR',
        'owner_email': 'VARCHAR',
        'next_follow_up_date': 'DATE',
        'last_reminder_sent': 'DATE',
        'created_at': 'TIMESTAMP WITH TIME ZONE'
    },
    'contacts': {
        'id': 'INTEGER PRIMARY KEY',
        'client_id': 'INTEGER NOT NULL',
        'name': 'VARCHAR NOT NULL',
        'role': 'VARCHAR',
        'email': 'VARCHAR',
        'phone': 'VARCHAR'
    },
    'services': {
        'id': 'INTEGER PRIMARY KEY',
        'client_id': 'INTEGER NOT NULL',
        'service_type': 'VARCHAR NOT NULL',
        'billing_frequency': 'VARCHAR',
        'monthly_fee': 'DOUBLE PRECISION',
        'active': 'BOOLEAN'
    },
    'tasks': {
        'id': 'INTEGER PRIMARY KEY',
        'client_id': 'INTEGER NOT NULL',
        'title': 'VARCHAR NOT NULL',
        'due_date': 'DATE',
        'status': 'VARCHAR NOT NULL',
        'notes': 'TEXT'
    },
    'notes': {
        'id': 'INTEGER PRIMARY KEY',
        'client_id': 'INTEGER NOT NULL',
        'content': 'TEXT NOT NULL',
        'created_at': 'TIMESTAMP WITH TIME ZONE'
    },
    'timesheets': {
        'id': 'INTEGER PRIMARY KEY',
        'client_id': 'INTEGER NOT NULL',
        'staff_member': 'VARCHAR NOT NULL',
        'entry_date': 'DATE NOT NULL',
        'start_time': 'VARCHAR',
        'end_time': 'VARCHAR',
        'hours': 'DOUBLE PRECISION NOT NULL',
        'project_task': 'VARCHAR',
        'description': 'TEXT',
        'billable': 'BOOLEAN',
        'created_at': 'TIMESTAMP WITH TIME ZONE',
        'updated_at': 'TIMESTAMP WITH TIME ZONE'
    },
    'users': {
        'id': 'INTEGER PRIMARY KEY',
        'email': 'VARCHAR NOT NULL',
        'name': 'VARCHAR NOT NULL',
        'hashed_password': 'VARCHAR NOT NULL',
        'role': 'VARCHAR NOT NULL',
        'permissions': 'TEXT',
        'active': 'BOOLEAN',
        'created_at': 'TIMESTAMP WITH TIME ZONE',
        'updated_at': 'TIMESTAMP WITH TIME ZONE'
    }
}

# Column defaults for safe migration
COLUMN_DEFAULTS = {
    'clients': {
        'status': "'Prospect'",
        'created_at': 'CURRENT_TIMESTAMP'
    },
    'services': {
        'service_type': "'Other'",
        'active': 'TRUE'
    },
    'tasks': {
        'title': "'Untitled Task'",
        'status': "'Open'"
    },
    'notes': {
        'content': "''"
    },
    'timesheets': {
        'staff_member': "'Unknown'",
        'entry_date': 'CURRENT_DATE',
        'hours': '0',
        'billable': 'TRUE',
        'created_at': 'CURRENT_TIMESTAMP',
        'updated_at': 'CURRENT_TIMESTAMP'
    },
    'users': {
        'role': "'Staff'",
        'active': 'TRUE',
        'created_at': 'CURRENT_TIMESTAMP',
        'updated_at': 'CURRENT_TIMESTAMP'
    }
}


def check_column_exists(conn, table_name: str, column_name: str) -> bool:
    """
    Check if a column exists in a table using direct SQL query.
    
    This is more reliable than using SQLAlchemy inspector which may have stale cache.
    """
    try:
        result = conn.execute(text(f"""
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


def get_existing_columns(conn, table_name: str) -> Set[str]:
    """Get all existing columns for a table."""
    try:
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_schema = 'public' AND table_name = :table_name
        """), {"table_name": table_name})
        return {row[0] for row in result}
    except Exception as e:
        logger.error(f"Error getting columns for {table_name}: {e}")
        return set()


def generate_column_sql(table_name: str, column_name: str) -> str:
    """
    Generate SQL ALTER TABLE statement for adding a column.
    
    Includes proper defaults for NOT NULL columns to handle existing data.
    """
    expected = EXPECTED_COLUMNS.get(table_name, {}).get(column_name, 'VARCHAR')
    defaults = COLUMN_DEFAULTS.get(table_name, {}).get(column_name)
    
    # Parse the expected type
    sql_type = expected.replace('PRIMARY KEY', '').strip()
    
    # Add default if column is NOT NULL and we have a default
    if 'NOT NULL' in sql_type and defaults:
        sql_type = sql_type.replace('NOT NULL', f'NOT NULL DEFAULT {defaults}')
    
    return f"ALTER TABLE {table_name} ADD COLUMN {column_name} {sql_type}"


def migrate_table_comprehensive(conn, table_name: str) -> Tuple[bool, List[str]]:
    """
    Comprehensively migrate a table by adding all missing columns.
    
    Returns:
        (success, list of added columns)
    """
    if table_name not in EXPECTED_COLUMNS:
        logger.warning(f"Table {table_name} not in expected columns map")
        return False, []
    
    expected_cols = set(EXPECTED_COLUMNS[table_name].keys())
    existing_cols = get_existing_columns(conn, table_name)
    missing_cols = expected_cols - existing_cols
    
    if not missing_cols:
        logger.info(f"[SCHEMA] Table {table_name} is up to date")
        return True, []
    
    added_cols = []
    for col_name in sorted(missing_cols):
        try:
            # Double-check column doesn't exist (race condition protection)
            if check_column_exists(conn, table_name, col_name):
                logger.info(f"[SCHEMA] Column {table_name}.{col_name} already exists (race condition)")
                continue
            
            # Generate and execute ALTER TABLE
            sql = generate_column_sql(table_name, col_name)
            conn.execute(text(sql))
            conn.commit()
            
            # Verify it was added
            if check_column_exists(conn, table_name, col_name):
                logger.info(f"[SCHEMA] Added column {table_name}.{col_name}")
                added_cols.append(col_name)
            else:
                logger.error(f"[SCHEMA] Column {table_name}.{col_name} was not added successfully")
                return False, added_cols
                
        except Exception as e:
            error_msg = str(e).lower()
            if 'duplicate' in error_msg or 'already exists' in error_msg or '42701' in error_msg:
                logger.info(f"[SCHEMA] Column {table_name}.{col_name} already exists (detected via error)")
            else:
                logger.error(f"[SCHEMA] Failed to add column {table_name}.{col_name}: {e}")
                conn.rollback()
                return False, added_cols
    
    return True, added_cols


def fix_all_schema_drift() -> Tuple[bool, str]:
    """
    Comprehensive schema fix - migrates all tables to match models.
    
    Returns:
        (success, report_message)
    """
    logger.info("[SCHEMA FIX] Starting comprehensive schema reconciliation...")
    
    report_lines = []
    report_lines.append("=" * 70)
    report_lines.append("COMPREHENSIVE SCHEMA FIX")
    report_lines.append("=" * 70)
    report_lines.append("")
    
    try:
        with engine.begin() as conn:
            inspector = inspect(engine)
            all_tables = inspector.get_table_names()
            
            all_success = True
            total_added = 0
            
            for table_name in TABLE_MODEL_MAP.keys():
                report_lines.append(f"Table: {table_name}")
                report_lines.append("-" * 70)
                
                if table_name not in all_tables:
                    report_lines.append(f"  ⚠ Table does not exist - will be created by Base.metadata.create_all")
                    report_lines.append("")
                    continue
                
                success, added = migrate_table_comprehensive(conn, table_name)
                total_added += len(added)
                
                if success:
                    if added:
                        report_lines.append(f"  ✓ Added {len(added)} column(s): {', '.join(added)}")
                    else:
                        report_lines.append(f"  ✓ Table is up to date")
                else:
                    report_lines.append(f"  ✗ Migration failed")
                    all_success = False
                
                report_lines.append("")
            
            report_lines.append("=" * 70)
            report_lines.append(f"Summary: Added {total_added} column(s) across all tables")
            
            if all_success:
                report_lines.append("✓ All migrations completed successfully")
            else:
                report_lines.append("✗ Some migrations failed")
            
            report = "\n".join(report_lines)
            
            if all_success:
                logger.info("[SCHEMA FIX] Comprehensive schema fix completed successfully")
            else:
                logger.warning("[SCHEMA FIX] Some schema fixes failed")
            
            return all_success, report
            
    except Exception as e:
        error_msg = f"[SCHEMA FIX] Fatal error during schema fix: {e}"
        logger.error(error_msg, exc_info=True)
        report = "\n".join(report_lines) + f"\n\nERROR: {error_msg}"
        return False, report


def validate_schema_complete() -> Tuple[bool, Dict[str, Dict[str, List[str]]]]:
    """
    Complete schema validation - returns detailed drift report.
    
    Returns:
        (is_valid, drift_report)
        drift_report: {table_name: {missing_in_db: [...], extra_in_db: [...]}}
    """
    inspector = inspect(engine)
    drift_report = {}
    is_valid = True
    
    for table_name, model_class in TABLE_MODEL_MAP.items():
        if table_name not in inspector.get_table_names():
            drift_report[table_name] = {
                'missing_in_db': list(EXPECTED_COLUMNS.get(table_name, {}).keys()),
                'extra_in_db': [],
                'table_missing': True
            }
            is_valid = False
            continue
        
        expected = set(EXPECTED_COLUMNS.get(table_name, {}).keys())
        existing = get_existing_columns(engine.connect(), table_name)
        
        missing = expected - existing
        extra = existing - expected
        
        if missing or extra:
            is_valid = False
            drift_report[table_name] = {
                'missing_in_db': sorted(missing),
                'extra_in_db': sorted(extra),
                'table_missing': False
            }
    
    return is_valid, drift_report

