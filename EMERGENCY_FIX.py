"""
EMERGENCY FIX: Create admin users directly in database.
This bypasses all the normal checks and just creates the users.
Run this if nothing else works.
"""
import sqlite3
import json
from pathlib import Path
import bcrypt

# Direct bcrypt hashing to avoid passlib issues
def hash_password_direct(password: str) -> str:
    """Hash password using bcrypt directly (Python 3.14 compatible)."""
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

# Get default permissions without importing auth (to avoid bcrypt issues)
def get_default_permissions_simple(role: str) -> dict:
    """Simple permissions for Admin role."""
    if role == "Admin":
        return {
            "view_dashboard": True, "view_clients": True, "create_clients": True,
            "edit_clients": True, "delete_clients": True, "export_clients": True,
            "create_contacts": True, "delete_contacts": True, "create_services": True,
            "edit_services": True, "delete_services": True, "create_tasks": True,
            "edit_tasks": True, "delete_tasks": True, "create_notes": True,
            "delete_notes": True, "view_all_timesheets": True, "create_timesheets": True,
            "edit_all_timesheets": True, "delete_all_timesheets": True, "view_settings": True,
            "manage_users": True
        }
    return {}

DB_PATH = Path("crm.db")

if not DB_PATH.exists():
    print("❌ Database file 'crm.db' not found!")
    print("Please run 'python seed.py' first to create the database.")
    exit(1)

print("Connecting to database...")
conn = sqlite3.connect(str(DB_PATH))
cursor = conn.cursor()

try:
    # Check if users table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    if not cursor.fetchone():
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
        cursor.execute("CREATE INDEX idx_users_email ON users(email)")
        print("✅ Users table created!")
    
    # Check if users already exist
    cursor.execute("SELECT COUNT(*) FROM users WHERE email IN ('Paul@tierneyohlms.com', 'Dan@tierneyohlms.com')")
    existing_count = cursor.fetchone()[0]
    
    if existing_count > 0:
        print(f"⚠️  Found {existing_count} existing admin user(s).")
        response = input("Do you want to delete and recreate them? (yes/no): ")
        if response.lower() == 'yes':
            cursor.execute("DELETE FROM users WHERE email IN ('Paul@tierneyohlms.com', 'Dan@tierneyohlms.com')")
            print("Deleted existing admin users.")
        else:
            print("Keeping existing users. Exiting.")
            conn.close()
            exit(0)
    
    # Create admin users
    print("\nCreating admin users...")
    
    # Get permissions and hash password (using direct methods to avoid import issues)
    admin_permissions = get_default_permissions_simple("Admin")
    password_hash = hash_password_direct("ChangeMe123!")
    
    # Create Paul
    try:
        cursor.execute("""
            INSERT INTO users (email, name, hashed_password, role, permissions, active)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            "Paul@tierneyohlms.com",
            "Paul Ohlms",
            password_hash,
            "Admin",
            json.dumps(admin_permissions),
            1
        ))
        print("✅ Created Paul@tierneyohlms.com")
    except sqlite3.IntegrityError:
        print("⚠️  Paul@tierneyohlms.com already exists (skipping)")
    
    # Create Dan
    try:
        cursor.execute("""
            INSERT INTO users (email, name, hashed_password, role, permissions, active)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            "Dan@tierneyohlms.com",
            "Dan Tierney",
            password_hash,
            "Admin",
            json.dumps(admin_permissions),
            1
        ))
        print("✅ Created Dan@tierneyohlms.com")
    except sqlite3.IntegrityError:
        print("⚠️  Dan@tierneyohlms.com already exists (skipping)")
    
    conn.commit()
    
    # Verify
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    
    print(f"\n✅ SUCCESS! Total users in database: {total_users}")
    print("\n" + "="*50)
    print("LOGIN CREDENTIALS:")
    print("="*50)
    print("Email: Paul@tierneyohlms.com")
    print("Password: ChangeMe123!")
    print("\nOR")
    print("\nEmail: Dan@tierneyohlms.com")
    print("Password: ChangeMe123!")
    print("="*50)
    print("\n⚠️  CHANGE THESE PASSWORDS IMMEDIATELY after logging in!")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    conn.rollback()
finally:
    conn.close()

