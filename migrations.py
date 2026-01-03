"""
Database migration utilities.

Handles schema migrations for existing databases by adding missing columns.
Uses isolated connections to prevent transaction state issues.
"""
import os
from sqlalchemy import inspect, text
from database import engine


def migrate_database_schema():
    """
    Migrate database schema by adding missing columns to existing tables.
    
    This function:
    - Only runs for PostgreSQL (production)
    - Uses isolated connections to avoid transaction issues
    - Adds missing columns based on model definitions
    - Fails gracefully if columns already exist
    """
    if not os.getenv("DATABASE_URL"):
        # SQLite - tables are created fresh, no migration needed
        return
    
    try:
        # Use isolated connection for DDL operations
        # This prevents transaction state from affecting the main session pool
        with engine.connect() as conn:
            inspector = inspect(engine)
            
            # Migrate users table
            if 'users' in inspector.get_table_names():
                _migrate_users_table(conn, inspector)
            
            # Migrate clients table
            if 'clients' in inspector.get_table_names():
                _migrate_clients_table(conn, inspector)
                
    except Exception as e:
        print(f"[WARNING] Migration error: {e}")
        import traceback
        traceback.print_exc()
        # Don't fail startup - application should still work


def _migrate_users_table(conn, inspector):
    """Add missing columns to users table."""
    columns = {col['name'] for col in inspector.get_columns('users')}
    columns_to_add = []
    
    # Define required columns with their SQL definitions
    required_columns = {
        'name': 'VARCHAR',
        'role': "VARCHAR DEFAULT 'Staff'",
        'permissions': 'TEXT',
        'active': 'BOOLEAN DEFAULT TRUE',
        'created_at': 'TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP',
        'updated_at': 'TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP'
    }
    
    for col_name, col_def in required_columns.items():
        if col_name not in columns:
            columns_to_add.append((col_name, col_def))
    
    # Add missing columns
    for col_name, col_def in columns_to_add:
        try:
            # Each ALTER TABLE in its own transaction
            with conn.begin():
                conn.execute(text(f"ALTER TABLE users ADD COLUMN {col_name} {col_def}"))
            print(f"[OK] Added column 'users.{col_name}'")
        except Exception as e:
            # Column might already exist or other error
            print(f"[WARNING] Could not add column 'users.{col_name}': {e}")
    
    # Update existing users with default values
    _update_user_defaults(conn)


def _migrate_clients_table(conn, inspector):
    """Add missing columns to clients table."""
    columns = {col['name'] for col in inspector.get_columns('clients')}
    columns_to_add = []
    
    # Define required columns with their SQL definitions
    required_columns = {
        'owner_name': 'VARCHAR',
        'owner_email': 'VARCHAR',
        'next_follow_up_date': 'DATE',
        'last_reminder_sent': 'DATE',
        'created_at': 'TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP'
    }
    
    for col_name, col_def in required_columns.items():
        if col_name not in columns:
            columns_to_add.append((col_name, col_def))
    
    # Add missing columns
    for col_name, col_def in columns_to_add:
        try:
            # Each ALTER TABLE in its own transaction
            with conn.begin():
                conn.execute(text(f"ALTER TABLE clients ADD COLUMN {col_name} {col_def}"))
            print(f"[OK] Added column 'clients.{col_name}'")
        except Exception as e:
            # Column might already exist or other error
            print(f"[WARNING] Could not add column 'clients.{col_name}': {e}")


def _update_user_defaults(conn):
    """Update existing users with default values if missing."""
    try:
        # Set names from emails
        with conn.begin():
            result = conn.execute(text("""
                UPDATE users 
                SET name = SPLIT_PART(email, '@', 1)
                WHERE name IS NULL OR name = ''
            """))
            if result.rowcount > 0:
                print(f"[OK] Updated {result.rowcount} user(s) with names from email")
    except Exception as e:
        print(f"[WARNING] Could not update user names: {e}")
    
    try:
        # Set default role
        with conn.begin():
            result = conn.execute(text("""
                UPDATE users 
                SET role = 'Staff' 
                WHERE role IS NULL OR role = ''
            """))
            if result.rowcount > 0:
                print(f"[OK] Set default role for {result.rowcount} user(s)")
    except Exception as e:
        print(f"[WARNING] Could not update user roles: {e}")
    
    try:
        # Set default active status
        with conn.begin():
            result = conn.execute(text("""
                UPDATE users 
                SET active = TRUE 
                WHERE active IS NULL
            """))
            if result.rowcount > 0:
                print(f"[OK] Set default active status for {result.rowcount} user(s)")
    except Exception as e:
        print(f"[WARNING] Could not update user active status: {e}")

