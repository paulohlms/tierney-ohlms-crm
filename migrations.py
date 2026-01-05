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
            
            # Migrate services table
            services_success = False
            if 'services' in inspector.get_table_names():
                services_success = _migrate_services_table(conn, inspector)
            else:
                print("[MIGRATION] Services table does not exist - will be created by Base.metadata.create_all")
                services_success = True  # Table will be created fresh
            
            # Migrate contacts table
            contacts_success = False
            if 'contacts' in inspector.get_table_names():
                contacts_success = _migrate_contacts_table(conn, inspector)
            else:
                print("[MIGRATION] Contacts table does not exist - will be created by Base.metadata.create_all")
                contacts_success = True  # Table will be created fresh
            
            # Migrate timesheets table
            timesheets_success = False
            if 'timesheets' in inspector.get_table_names():
                timesheets_success = _migrate_timesheets_table(conn, inspector)
            else:
                print("[MIGRATION] Timesheets table does not exist - will be created by Base.metadata.create_all")
                timesheets_success = True  # Table will be created fresh
            
            # Migrate tasks table
            tasks_success = False
            if 'tasks' in inspector.get_table_names():
                tasks_success = _migrate_tasks_table(conn, inspector)
            else:
                print("[MIGRATION] Tasks table does not exist - will be created by Base.metadata.create_all")
                tasks_success = True  # Table will be created fresh
            
            # Migrate notes table
            notes_success = False
            if 'notes' in inspector.get_table_names():
                notes_success = _migrate_notes_table(conn, inspector)
            else:
                print("[MIGRATION] Notes table does not exist - will be created by Base.metadata.create_all")
                notes_success = True  # Table will be created fresh
            
            if users_success and clients_success and services_success and contacts_success and timesheets_success and tasks_success and notes_success:
                print("[MIGRATION] Migration completed successfully")
                return True
            else:
                print(f"[MIGRATION] Migration completed with errors (users: {users_success}, clients: {clients_success}, services: {services_success}, contacts: {contacts_success}, timesheets: {timesheets_success}, tasks: {tasks_success}, notes: {notes_success})")
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


def _migrate_services_table(conn, inspector) -> bool:
    """
    Add missing columns to services table.
    
    This function is idempotent - it can be run multiple times safely.
    It checks for column existence using direct SQL queries to avoid
    stale inspector cache issues.
    
    Returns:
        True if all required columns exist or were added, False otherwise
    """
    try:
        # Use direct SQL query to check column existence - more reliable than inspector cache
        # This prevents duplicate column additions when migration runs multiple times
        def column_exists(table_name: str, column_name: str) -> bool:
            """Check if a column exists using direct SQL query."""
            try:
                result = conn.execute(text(f"""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = '{table_name}' AND column_name = '{column_name}'
                """))
                return result.fetchone() is not None
            except Exception:
                return False
        
        # Define required columns with their SQL definitions
        # Based on the Service model in models.py
        required_columns = {
            'service_type': "VARCHAR NOT NULL DEFAULT 'Other'",  # Required field, add default for existing rows
            'billing_frequency': 'VARCHAR',
            'monthly_fee': 'DOUBLE PRECISION',
            'active': 'BOOLEAN DEFAULT TRUE'
        }
        
        # Check each column and add only if missing
        for col_name, col_def in required_columns.items():
            # Use direct SQL query instead of inspector to avoid cache issues
            if column_exists('services', col_name):
                print(f"[MIGRATION] Column 'services.{col_name}' already exists - skipping")
                continue
            
            try:
                # PostgreSQL allows adding NOT NULL columns with DEFAULT in one statement
                # This automatically populates existing rows with the default value
                conn.execute(text(f"ALTER TABLE services ADD COLUMN {col_name} {col_def}"))
                print(f"[MIGRATION] Added column 'services.{col_name}'")
                
                # Verify the column was actually added
                if not column_exists('services', col_name):
                    print(f"[MIGRATION ERROR] Column 'services.{col_name}' was not added successfully")
                    return False
                    
            except Exception as e:
                error_msg = str(e).lower()
                # PostgreSQL error codes: 42701 = duplicate_column
                if 'duplicate' in error_msg or 'already exists' in error_msg or '42701' in error_msg:
                    # Column exists - this is OK, might have been added concurrently
                    print(f"[MIGRATION] Column 'services.{col_name}' already exists (detected via error)")
                else:
                    print(f"[MIGRATION ERROR] Could not add column 'services.{col_name}': {e}")
                    return False
        
        # Final verification: ensure all required columns exist
        missing_columns = []
        for col_name in required_columns.keys():
            if not column_exists('services', col_name):
                missing_columns.append(col_name)
        
        if missing_columns:
            print(f"[MIGRATION ERROR] Missing columns after migration: {missing_columns}")
            return False
        
        print(f"[MIGRATION] Services table migration completed successfully")
        return True
        
    except Exception as e:
        print(f"[MIGRATION ERROR] Error migrating services table: {e}")
        import traceback
        traceback.print_exc()
        return False


def _migrate_contacts_table(conn, inspector) -> bool:
    """
    Add missing columns to contacts table.
    
    Returns:
        True if all required columns exist or were added, False otherwise
    """
    try:
        columns = {col['name'] for col in inspector.get_columns('contacts')}
        columns_to_add = []
        
        # Define required columns with their SQL definitions
        # Based on the Contact model in models.py
        required_columns = {
            'role': 'VARCHAR',  # Owner, Controller, Bookkeeper, Tax, Other
            'email': 'VARCHAR',
            'phone': 'VARCHAR'
        }
        
        for col_name, col_def in required_columns.items():
            if col_name not in columns:
                columns_to_add.append((col_name, col_def))
        
        # Add missing columns
        for col_name, col_def in columns_to_add:
            try:
                conn.execute(text(f"ALTER TABLE contacts ADD COLUMN {col_name} {col_def}"))
                print(f"[MIGRATION] Added column 'contacts.{col_name}'")
            except Exception as e:
                # Check if column was actually added (might have been added concurrently)
                inspector = inspect(engine)
                current_columns = {col['name'] for col in inspector.get_columns('contacts')}
                if col_name in current_columns:
                    print(f"[MIGRATION] Column 'contacts.{col_name}' already exists")
                else:
                    print(f"[MIGRATION ERROR] Could not add column 'contacts.{col_name}': {e}")
                    return False
        
        # Verify all columns exist
        inspector = inspect(engine)
        final_columns = {col['name'] for col in inspector.get_columns('contacts')}
        for col_name in required_columns.keys():
            if col_name not in final_columns:
                print(f"[MIGRATION ERROR] Column 'contacts.{col_name}' is missing after migration")
                return False
        
        return True
    except Exception as e:
        print(f"[MIGRATION ERROR] Error migrating contacts table: {e}")
        import traceback
        traceback.print_exc()
        return False


def _migrate_timesheets_table(conn, inspector) -> bool:
    """
    Add missing columns to timesheets table.
    
    Returns:
        True if all required columns exist or were added, False otherwise
    """
    try:
        columns = {col['name'] for col in inspector.get_columns('timesheets')}
        columns_to_add = []
        
        # Define required columns with their SQL definitions
        # Based on the Timesheet model in models.py
        required_columns = {
            'entry_date': "DATE NOT NULL DEFAULT CURRENT_DATE",  # Required field, add default for existing rows
            'staff_member': "VARCHAR NOT NULL DEFAULT 'Unknown'",  # Required field
            'start_time': 'VARCHAR',
            'end_time': 'VARCHAR',
            'hours': 'DOUBLE PRECISION NOT NULL DEFAULT 0',  # Required field
            'project_task': 'VARCHAR',
            'description': 'TEXT',
            'billable': 'BOOLEAN DEFAULT TRUE',
            'created_at': 'TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP',
            'updated_at': 'TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP'
        }
        
        for col_name, col_def in required_columns.items():
            if col_name not in columns:
                columns_to_add.append((col_name, col_def))
        
        # Add missing columns
        for col_name, col_def in columns_to_add:
            try:
                # PostgreSQL allows adding NOT NULL columns with DEFAULT in one statement
                # This automatically populates existing rows with the default value
                conn.execute(text(f"ALTER TABLE timesheets ADD COLUMN {col_name} {col_def}"))
                print(f"[MIGRATION] Added column 'timesheets.{col_name}'")
            except Exception as e:
                # Check if column was actually added (might have been added concurrently)
                inspector = inspect(engine)
                current_columns = {col['name'] for col in inspector.get_columns('timesheets')}
                if col_name in current_columns:
                    print(f"[MIGRATION] Column 'timesheets.{col_name}' already exists")
                else:
                    print(f"[MIGRATION ERROR] Could not add column 'timesheets.{col_name}': {e}")
                    return False
        
        # Verify all columns exist
        inspector = inspect(engine)
        final_columns = {col['name'] for col in inspector.get_columns('timesheets')}
        for col_name in required_columns.keys():
            if col_name not in final_columns:
                print(f"[MIGRATION ERROR] Column 'timesheets.{col_name}' is missing after migration")
                return False
        
        return True
    except Exception as e:
        print(f"[MIGRATION ERROR] Error migrating timesheets table: {e}")
        import traceback
        traceback.print_exc()
        return False


def _migrate_tasks_table(conn, inspector) -> bool:
    """
    Add missing columns to tasks table.
    
    Returns:
        True if all required columns exist or were added, False otherwise
    """
    try:
        columns = {col['name'] for col in inspector.get_columns('tasks')}
        columns_to_add = []
        
        # Define required columns with their SQL definitions
        # Based on the Task model in models.py
        required_columns = {
            'title': "VARCHAR NOT NULL DEFAULT 'Untitled Task'",  # Required field
            'due_date': 'DATE',
            'status': "VARCHAR NOT NULL DEFAULT 'Open'",  # Required field
            'notes': 'TEXT'
        }
        
        for col_name, col_def in required_columns.items():
            if col_name not in columns:
                columns_to_add.append((col_name, col_def))
        
        # Add missing columns
        for col_name, col_def in columns_to_add:
            try:
                conn.execute(text(f"ALTER TABLE tasks ADD COLUMN {col_name} {col_def}"))
                print(f"[MIGRATION] Added column 'tasks.{col_name}'")
            except Exception as e:
                # Check if column was actually added (might have been added concurrently)
                inspector = inspect(engine)
                current_columns = {col['name'] for col in inspector.get_columns('tasks')}
                if col_name in current_columns:
                    print(f"[MIGRATION] Column 'tasks.{col_name}' already exists")
                else:
                    print(f"[MIGRATION ERROR] Could not add column 'tasks.{col_name}': {e}")
                    return False
        
        # Verify all columns exist
        inspector = inspect(engine)
        final_columns = {col['name'] for col in inspector.get_columns('tasks')}
        for col_name in required_columns.keys():
            if col_name not in final_columns:
                print(f"[MIGRATION ERROR] Column 'tasks.{col_name}' is missing after migration")
                return False
        
        return True
    except Exception as e:
        print(f"[MIGRATION ERROR] Error migrating tasks table: {e}")
        import traceback
        traceback.print_exc()
        return False


def _migrate_notes_table(conn, inspector) -> bool:
    """
    Add missing columns to notes table.
    
    Returns:
        True if all required columns exist or were added, False otherwise
    """
    try:
        columns = {col['name'] for col in inspector.get_columns('notes')}
        columns_to_add = []
        
        # Define required columns with their SQL definitions
        # Based on the Note model in models.py
        required_columns = {
            'content': "TEXT NOT NULL DEFAULT ''",  # Required field
            'created_at': 'TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP'
        }
        
        for col_name, col_def in required_columns.items():
            if col_name not in columns:
                columns_to_add.append((col_name, col_def))
        
        # Add missing columns
        for col_name, col_def in columns_to_add:
            try:
                conn.execute(text(f"ALTER TABLE notes ADD COLUMN {col_name} {col_def}"))
                print(f"[MIGRATION] Added column 'notes.{col_name}'")
            except Exception as e:
                # Check if column was actually added (might have been added concurrently)
                inspector = inspect(engine)
                current_columns = {col['name'] for col in inspector.get_columns('notes')}
                if col_name in current_columns:
                    print(f"[MIGRATION] Column 'notes.{col_name}' already exists")
                else:
                    print(f"[MIGRATION ERROR] Could not add column 'notes.{col_name}': {e}")
                    return False
        
        # Verify all columns exist
        inspector = inspect(engine)
        final_columns = {col['name'] for col in inspector.get_columns('notes')}
        for col_name in required_columns.keys():
            if col_name not in final_columns:
                print(f"[MIGRATION ERROR] Column 'notes.{col_name}' is missing after migration")
                return False
        
        return True
    except Exception as e:
        print(f"[MIGRATION ERROR] Error migrating notes table: {e}")
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
