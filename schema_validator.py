"""
Schema validation and drift detection.

This module validates that SQLAlchemy models match the actual database schema.
It will detect and report any mismatches, and can optionally fix them.
"""
import logging
from typing import Dict, List, Tuple, Set
from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError
from database import engine
from models import (
    Client, Contact, Service, Task, Note, Timesheet, User
)

logger = logging.getLogger(__name__)


def get_model_columns(model_class) -> Dict[str, str]:
    """
    Get expected columns from a SQLAlchemy model.
    
    Returns:
        Dictionary mapping column name to SQL type
    """
    columns = {}
    for column in model_class.__table__.columns:
        col_type = str(column.type)
        # Normalize type names
        if 'VARCHAR' in col_type or 'String' in col_type:
            col_type = 'VARCHAR'
        elif 'INTEGER' in col_type or 'Integer' in col_type:
            col_type = 'INTEGER'
        elif 'BOOLEAN' in col_type or 'Boolean' in col_type:
            col_type = 'BOOLEAN'
        elif 'DATE' in col_type or 'Date' in col_type:
            col_type = 'DATE'
        elif 'TIMESTAMP' in col_type or 'DateTime' in col_type:
            col_type = 'TIMESTAMP'
        elif 'FLOAT' in col_type or 'Float' in col_type:
            col_type = 'DOUBLE PRECISION'
        elif 'TEXT' in col_type or 'Text' in col_type:
            col_type = 'TEXT'
        
        columns[column.name] = {
            'type': col_type,
            'nullable': column.nullable,
            'default': column.default
        }
    return columns


def get_database_columns(table_name: str, inspector) -> Set[str]:
    """
    Get actual columns from the database.
    
    Returns:
        Set of column names
    """
    try:
        columns = inspector.get_columns(table_name)
        return {col['name'] for col in columns}
    except Exception as e:
        logger.error(f"Error getting columns for table {table_name}: {e}")
        return set()


def validate_schema() -> Tuple[bool, Dict[str, Dict[str, List[str]]]]:
    """
    Validate that all models match the database schema.
    
    Returns:
        Tuple of (is_valid, drift_report)
        drift_report structure:
        {
            'table_name': {
                'missing_in_db': [col1, col2, ...],
                'missing_in_model': [col1, col2, ...],
                'extra_in_db': [col1, col2, ...]
            }
        }
    """
    inspector = inspect(engine)
    drift_report = {}
    is_valid = True
    
    # Map of model classes to table names
    models = {
        'clients': Client,
        'contacts': Contact,
        'services': Service,
        'tasks': Task,
        'notes': Note,
        'timesheets': Timesheet,
        'users': User
    }
    
    for table_name, model_class in models.items():
        # Check if table exists
        if table_name not in inspector.get_table_names():
            logger.error(f"[SCHEMA] Table '{table_name}' does not exist in database")
            drift_report[table_name] = {
                'missing_in_db': list(get_model_columns(model_class).keys()),
                'missing_in_model': [],
                'extra_in_db': [],
                'table_missing': True
            }
            is_valid = False
            continue
        
        # Get expected columns from model
        model_columns = get_model_columns(model_class)
        model_column_names = set(model_columns.keys())
        
        # Get actual columns from database
        db_columns = get_database_columns(table_name, inspector)
        
        # Find differences
        missing_in_db = model_column_names - db_columns
        extra_in_db = db_columns - model_column_names
        
        if missing_in_db or extra_in_db:
            is_valid = False
            drift_report[table_name] = {
                'missing_in_db': sorted(missing_in_db),
                'missing_in_model': sorted(extra_in_db),
                'extra_in_db': sorted(extra_in_db),
                'table_missing': False
            }
            logger.warning(f"[SCHEMA] Drift detected in table '{table_name}':")
            if missing_in_db:
                logger.warning(f"  Missing in DB: {sorted(missing_in_db)}")
            if extra_in_db:
                logger.warning(f"  Extra in DB: {sorted(extra_in_db)}")
        else:
            logger.info(f"[SCHEMA] Table '{table_name}' is valid")
    
    return is_valid, drift_report


def generate_diff_report(drift_report: Dict) -> str:
    """
    Generate a human-readable diff report.
    """
    report_lines = []
    report_lines.append("=" * 70)
    report_lines.append("SCHEMA DRIFT REPORT")
    report_lines.append("=" * 70)
    report_lines.append("")
    
    if not drift_report:
        report_lines.append("✓ All tables match their models - no drift detected.")
        return "\n".join(report_lines)
    
    for table_name, issues in drift_report.items():
        report_lines.append(f"Table: {table_name}")
        report_lines.append("-" * 70)
        
        if issues.get('table_missing'):
            report_lines.append("  ✗ TABLE MISSING - Table does not exist in database")
            report_lines.append(f"  Expected columns: {', '.join(issues['missing_in_db'])}")
        else:
            if issues['missing_in_db']:
                report_lines.append(f"  ✗ Missing columns in database ({len(issues['missing_in_db'])}):")
                for col in issues['missing_in_db']:
                    report_lines.append(f"    - {col}")
            
            if issues['extra_in_db']:
                report_lines.append(f"  ⚠ Extra columns in database ({len(issues['extra_in_db'])}):")
                for col in issues['extra_in_db']:
                    report_lines.append(f"    + {col}")
        
        report_lines.append("")
    
    report_lines.append("=" * 70)
    return "\n".join(report_lines)


def fix_schema_drift(drift_report: Dict) -> bool:
    """
    Attempt to fix schema drift by adding missing columns.
    
    Returns:
        True if all fixes succeeded, False otherwise
    """
    if not drift_report:
        return True
    
    try:
        with engine.connect() as conn:
            conn = conn.execution_options(autocommit=True)
            inspector = inspect(engine)
            
            all_success = True
            
            for table_name, issues in drift_report.items():
                if issues.get('table_missing'):
                    logger.error(f"[SCHEMA FIX] Cannot fix - table '{table_name}' is missing")
                    all_success = False
                    continue
                
                # Add missing columns
                for col_name in issues['missing_in_db']:
                    try:
                        # Get column definition from model
                        model_class = {
                            'clients': Client,
                            'contacts': Contact,
                            'services': Service,
                            'tasks': Task,
                            'notes': Note,
                            'timesheets': Timesheet,
                            'users': User
                        }[table_name]
                        
                        column = model_class.__table__.columns[col_name]
                        
                        # Generate SQL type
                        col_type = str(column.type)
                        sql_type = _convert_sqlalchemy_type(col_type, column.nullable)
                        
                        # Add column
                        conn.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {col_name} {sql_type}"))
                        logger.info(f"[SCHEMA FIX] Added column '{table_name}.{col_name}'")
                        
                    except Exception as e:
                        logger.error(f"[SCHEMA FIX] Failed to add column '{table_name}.{col_name}': {e}")
                        all_success = False
            
            return all_success
            
    except Exception as e:
        logger.error(f"[SCHEMA FIX] Error fixing schema drift: {e}", exc_info=True)
        return False


def _convert_sqlalchemy_type(sqlalchemy_type: str, nullable: bool) -> str:
    """
    Convert SQLAlchemy type to PostgreSQL type.
    """
    type_str = str(sqlalchemy_type).upper()
    
    if 'VARCHAR' in type_str or 'STRING' in type_str:
        pg_type = 'VARCHAR'
    elif 'INTEGER' in type_str or 'INT' in type_str:
        pg_type = 'INTEGER'
    elif 'BOOLEAN' in type_str or 'BOOL' in type_str:
        pg_type = 'BOOLEAN'
    elif 'DATE' in type_str:
        pg_type = 'DATE'
    elif 'TIMESTAMP' in type_str or 'DATETIME' in type_str:
        pg_type = 'TIMESTAMP WITH TIME ZONE'
    elif 'FLOAT' in type_str or 'DOUBLE' in type_str:
        pg_type = 'DOUBLE PRECISION'
    elif 'TEXT' in type_str:
        pg_type = 'TEXT'
    else:
        pg_type = 'VARCHAR'  # Default fallback
    
    if not nullable:
        pg_type += ' NOT NULL'
    
    return pg_type


def validate_and_fix() -> Tuple[bool, str]:
    """
    Validate schema and attempt to fix any drift.
    
    Returns:
        Tuple of (success, report_message)
    """
    logger.info("[SCHEMA] Starting schema validation...")
    
    is_valid, drift_report = validate_schema()
    
    if is_valid:
        report = generate_diff_report(drift_report)
        logger.info("[SCHEMA] Schema validation passed - no drift detected")
        return True, report
    
    # Generate report
    report = generate_diff_report(drift_report)
    logger.warning("[SCHEMA] Schema drift detected - attempting to fix...")
    
    # Attempt to fix
    fix_success = fix_schema_drift(drift_report)
    
    if fix_success:
        # Re-validate
        is_valid_after, drift_report_after = validate_schema()
        if is_valid_after:
            report += "\n\n[SCHEMA FIX] All schema drift has been fixed successfully."
            logger.info("[SCHEMA] Schema drift fixed successfully")
            return True, report
        else:
            report += "\n\n[SCHEMA FIX] Some drift remains after fix attempt."
            report += "\n" + generate_diff_report(drift_report_after)
            logger.warning("[SCHEMA] Some schema drift remains after fix")
            return False, report
    else:
        report += "\n\n[SCHEMA FIX] Failed to fix some schema drift issues."
        logger.error("[SCHEMA] Failed to fix schema drift")
        return False, report

