"""
Database migration utilities.

Rebuilt with:
- Explicit autocommit mode for DDL operations
- Verification that columns were actually added
- Clear error reporting
- No silent failures
"""
import os
from sqlalchemy import inspect, text
from database import engine


def migrate_database_schema():
    """
    Migrate database schema by adding missing columns to existing tables.
    
    Uses autocommit mode for DDL operations to prevent transaction state issues.
    Verifies that columns were actually added.
    
    Returns:
        True if migration succeeded, False otherwise
    """
    if not os.getenv("DATABASE_URL"):
        # SQLite - tables are created fresh, no migration needed
        return True
    
    try:
        # Use isolated connection with autocommit for DDL operations
        # This prevents transaction state from affecting the main session pool
        with engine.connect() as conn:
            # Set autocommit mode for DDL operations
            conn = conn.execution_options(autocommit=True)
            inspector = inspect(engine)
            
            # Migrate users table
            users_success = False
            if 'users' in inspector.get_table_names():
                users_success = _migrate_users_table(conn, inspector)
            else:
                print("[MIGRATION] Users table does not exist - will be created by Base.metadata.create_all")
                users_success = True  # Table will be created fresh
            
            # Migrate clients table
            clients_success = False
            if 'clients' in inspector.get_table_names():
                clients_success = _migrate_clients_table(conn, inspector)
            else:
                print("[MIGRATION] Clients table does not exist - will be created by Base.metadata.create_all")
                clients_success = True  # Table will be created fresh
            
            if users_success and clients_success:
                print("[MIGRATION] Migration completed successfully")
                return True
            else:
                print(f"[MIGRATION] Migration completed with errors (users: {users_success}, clients: {clients_success})")
                return False
                
    except Exception as e:
        print(f"[MIGRATION ERROR] Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def _migrate_users_table(conn, inspector) -> bool:
    """
    Add missing columns to users table.
    
    Returns:
        True if all required columns exist or were added, False otherwise
    """
    try:
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
                conn.execute(text(f"ALTER TABLE users ADD COLUMN {col_name} {col_def}"))
                print(f"[MIGRATION] Added column 'users.{col_name}'")
            except Exception as e:
                # Check if column was actually added (might have been added concurrently)
                inspector = inspect(engine)
                current_columns = {col['name'] for col in inspector.get_columns('users')}
                if col_name in current_columns:
                    print(f"[MIGRATION] Column 'users.{col_name}' already exists")
                else:
                    print(f"[MIGRATION ERROR] Could not add column 'users.{col_name}': {e}")
                    return False
        
        # Verify all columns exist
        inspector = inspect(engine)
        final_columns = {col['name'] for col in inspector.get_columns('users')}
        for col_name in required_columns.keys():
            if col_name not in final_columns:
                print(f"[MIGRATION ERROR] Column 'users.{col_name}' is missing after migration")
                return False
        
        # Update existing users with default values
        _update_user_defaults(conn)
        
        return True
    except Exception as e:
        print(f"[MIGRATION ERROR] Error migrating users table: {e}")
        import traceback
        traceback.print_exc()
        return False


def _migrate_clients_table(conn, inspector) -> bool:
    """
    Add missing columns to clients table.
    
    Returns:
        True if all required columns exist or were added, False otherwise
    """
    try:
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
                conn.execute(text(f"ALTER TABLE clients ADD COLUMN {col_name} {col_def}"))
                print(f"[MIGRATION] Added column 'clients.{col_name}'")
            except Exception as e:
                # Check if column was actually added (might have been added concurrently)
                inspector = inspect(engine)
                current_columns = {col['name'] for col in inspector.get_columns('clients')}
                if col_name in current_columns:
                    print(f"[MIGRATION] Column 'clients.{col_name}' already exists")
                else:
                    print(f"[MIGRATION ERROR] Could not add column 'clients.{col_name}': {e}")
                    return False
        
        # Verify all columns exist
        inspector = inspect(engine)
        final_columns = {col['name'] for col in inspector.get_columns('clients')}
        for col_name in required_columns.keys():
            if col_name not in final_columns:
                print(f"[MIGRATION ERROR] Column 'clients.{col_name}' is missing after migration")
                return False
        
        return True
    except Exception as e:
        print(f"[MIGRATION ERROR] Error migrating clients table: {e}")
        import traceback
        traceback.print_exc()
        return False


def _update_user_defaults(conn):
    """Update existing users with default values if missing."""
    try:
        # Set names from emails
        result = conn.execute(text("""
            UPDATE users 
            SET name = SPLIT_PART(email, '@', 1)
            WHERE name IS NULL OR name = ''
        """))
        if result.rowcount > 0:
            print(f"[MIGRATION] Updated {result.rowcount} user(s) with names from email")
    except Exception as e:
        print(f"[MIGRATION WARNING] Could not update user names: {e}")
    
    try:
        # Set default role
        result = conn.execute(text("""
            UPDATE users 
            SET role = 'Staff' 
            WHERE role IS NULL OR role = ''
        """))
        if result.rowcount > 0:
            print(f"[MIGRATION] Set default role for {result.rowcount} user(s)")
    except Exception as e:
        print(f"[MIGRATION WARNING] Could not update user roles: {e}")
    
    try:
        # Set default active status
        result = conn.execute(text("""
            UPDATE users 
            SET active = TRUE 
            WHERE active IS NULL
        """))
        if result.rowcount > 0:
            print(f"[MIGRATION] Set default active status for {result.rowcount} user(s)")
    except Exception as e:
        print(f"[MIGRATION WARNING] Could not update user active status: {e}")
