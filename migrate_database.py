"""
Database migration script to add missing columns to existing tables.

Run this script once to update your PostgreSQL database schema.
"""
import os
from sqlalchemy import create_engine, text, inspect
from database import DATABASE_URL, engine

def migrate_database():
    """Add missing columns to existing tables."""
    
    if not DATABASE_URL:
        print("⚠️  DATABASE_URL not set. This script is for PostgreSQL databases.")
        print("   SQLite databases will be auto-created with the correct schema.")
        return
    
    print("🔄 Starting database migration...")
    
    with engine.connect() as conn:
        inspector = inspect(engine)
        
        # Check users table
        if 'users' in inspector.get_table_names():
            print("📋 Checking users table...")
            columns = [col['name'] for col in inspector.get_columns('users')]
            
            # Add name column if missing
            if 'name' not in columns:
                print("  ➕ Adding 'name' column to users table...")
                conn.execute(text("ALTER TABLE users ADD COLUMN name VARCHAR"))
                conn.commit()
                print("  ✅ Added 'name' column")
            else:
                print("  ✓ 'name' column already exists")
            
            # Add created_at column if missing
            if 'created_at' not in columns:
                print("  ➕ Adding 'created_at' column to users table...")
                conn.execute(text("ALTER TABLE users ADD COLUMN created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP"))
                conn.commit()
                print("  ✅ Added 'created_at' column")
            else:
                print("  ✓ 'created_at' column already exists")
            
            # Add updated_at column if missing
            if 'updated_at' not in columns:
                print("  ➕ Adding 'updated_at' column to users table...")
                conn.execute(text("ALTER TABLE users ADD COLUMN updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP"))
                conn.commit()
                print("  ✅ Added 'updated_at' column")
            else:
                print("  ✓ 'updated_at' column already exists")
            
            # Update existing users to have a name if they don't
            print("  🔍 Checking for users without names...")
            result = conn.execute(text("SELECT id, email FROM users WHERE name IS NULL OR name = ''"))
            users_without_names = result.fetchall()
            
            if users_without_names:
                print(f"  ⚠️  Found {len(users_without_names)} user(s) without names. Updating...")
                for user_id, email in users_without_names:
                    # Extract name from email (e.g., "Paul@tierneyohlms.com" -> "Paul")
                    name = email.split('@')[0].title()
                    conn.execute(text("UPDATE users SET name = :name WHERE id = :id"), {"name": name, "id": user_id})
                conn.commit()
                print("  ✅ Updated user names")
            else:
                print("  ✓ All users have names")
        
        else:
            print("⚠️  'users' table does not exist. It will be created automatically on first run.")
    
    print("✅ Migration complete!")

if __name__ == "__main__":
    migrate_database()

