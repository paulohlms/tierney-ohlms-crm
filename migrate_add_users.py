"""
Migration script to create users table and add initial admin users.
Run this to set up the user management system.
"""
import sqlite3
from pathlib import Path
import json
from auth import hash_password, get_default_permissions

DB_PATH = Path("crm.db")

def migrate():
    """Create users table and add initial admin users."""
    if not DB_PATH.exists():
        print("Database not found. Run seed.py first to create the database.")
        return
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    try:
        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if cursor.fetchone():
            print("Users table already exists.")
            # Check if admins exist
            cursor.execute("SELECT COUNT(*) FROM users WHERE email IN ('Paul@tierneyohlms.com', 'Dan@tierneyohlms.com')")
            if cursor.fetchone()[0] > 0:
                print("Admin users already exist. Skipping user creation.")
                return
        else:
            # Create users table
            print("Creating users table...")
            cursor.execute("""
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email VARCHAR NOT NULL UNIQUE,
                    name VARCHAR NOT NULL,
                    hashed_password VARCHAR NOT NULL,
                    role VARCHAR NOT NULL DEFAULT 'Staff',
                    permissions TEXT,
                    active BOOLEAN DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create index
            cursor.execute("CREATE INDEX idx_users_email ON users(email)")
            print("Users table created successfully!")
        
        # Add admin users
        print("Creating admin users...")
        
        # Paul - Admin
        paul_permissions = get_default_permissions("Admin")
        paul_password_hash = hash_password("ChangeMe123!")  # Default password - CHANGE THIS!
        
        cursor.execute("""
            INSERT OR IGNORE INTO users (email, name, hashed_password, role, permissions, active)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            "Paul@tierneyohlms.com",
            "Paul Ohlms",
            paul_password_hash,
            "Admin",
            json.dumps(paul_permissions),
            1
        ))
        
        # Dan - Admin
        dan_permissions = get_default_permissions("Admin")
        dan_password_hash = hash_password("ChangeMe123!")  # Default password - CHANGE THIS!
        
        cursor.execute("""
            INSERT OR IGNORE INTO users (email, name, hashed_password, role, permissions, active)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            "Dan@tierneyohlms.com",
            "Dan Tierney",
            dan_password_hash,
            "Admin",
            json.dumps(dan_permissions),
            1
        ))
        
        conn.commit()
        print("Admin users created successfully!")
        print("\nIMPORTANT: Default passwords are 'ChangeMe123!' - Please change these immediately!")
        print("Admin users:")
        print("  - Paul@tierneyohlms.com")
        print("  - Dan@tierneyohlms.com")
        
    except Exception as e:
        conn.rollback()
        print(f"Error during migration: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()

