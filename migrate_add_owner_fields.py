"""
Migration script to add owner_name, owner_email, and last_reminder_sent fields to clients table.
Run this after updating models.py to add the new columns to existing databases.
"""
import sqlite3
from pathlib import Path

DB_PATH = Path("crm.db")

def migrate():
    """Add new columns to clients table if they don't exist."""
    if not DB_PATH.exists():
        print("Database not found. Run seed.py first to create the database.")
        return
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    try:
        # Check if columns exist
        cursor.execute("PRAGMA table_info(clients)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if "owner_name" not in columns:
            print("Adding owner_name column...")
            cursor.execute("ALTER TABLE clients ADD COLUMN owner_name VARCHAR")
        
        if "owner_email" not in columns:
            print("Adding owner_email column...")
            cursor.execute("ALTER TABLE clients ADD COLUMN owner_email VARCHAR")
        
        if "last_reminder_sent" not in columns:
            print("Adding last_reminder_sent column...")
            cursor.execute("ALTER TABLE clients ADD COLUMN last_reminder_sent DATE")
        
        conn.commit()
        print("Migration completed successfully!")
        
        # Update existing prospects with placeholder owner info if missing
        cursor.execute("""
            UPDATE clients 
            SET owner_name = 'Account Manager', 
                owner_email = 'admin@firm.com'
            WHERE status = 'Prospect' 
            AND (owner_name IS NULL OR owner_email IS NULL)
        """)
        conn.commit()
        print("Updated existing prospects with default owner information.")
        
    except Exception as e:
        conn.rollback()
        print(f"Error during migration: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()

