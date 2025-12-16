"""
Database migration script to update existing database schema.

This script safely migrates the database by:
1. Removing the ein_last4 column (if it exists)
2. Adding next_follow_up_date column (if it doesn't exist)

Run this once after updating the models.
"""
import sqlite3
import os
from datetime import datetime

DB_PATH = "crm.db"

def migrate_database():
    """Migrate the database schema."""
    if not os.path.exists(DB_PATH):
        print("Database file not found. It will be created automatically on first run.")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if ein_last4 column exists
        cursor.execute("PRAGMA table_info(clients)")
        columns = [row[1] for row in cursor.fetchall()]
        
        # Remove ein_last4 column if it exists
        if "ein_last4" in columns:
            print("Removing ein_last4 column...")
            # SQLite doesn't support DROP COLUMN directly, so we need to recreate the table
            cursor.execute("""
                CREATE TABLE clients_new (
                    id INTEGER PRIMARY KEY,
                    legal_name VARCHAR NOT NULL,
                    entity_type VARCHAR,
                    fiscal_year_end VARCHAR,
                    status VARCHAR NOT NULL DEFAULT 'Prospect',
                    next_follow_up_date DATE,
                    created_at DATETIME
                )
            """)
            
            # Copy data (excluding ein_last4)
            cursor.execute("""
                INSERT INTO clients_new (id, legal_name, entity_type, fiscal_year_end, status, created_at)
                SELECT id, legal_name, entity_type, fiscal_year_end, status, created_at
                FROM clients
            """)
            
            # Drop old table and rename new one
            cursor.execute("DROP TABLE clients")
            cursor.execute("ALTER TABLE clients_new RENAME TO clients")
            
            # Recreate indexes
            cursor.execute("CREATE INDEX IF NOT EXISTS ix_clients_id ON clients(id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS ix_clients_legal_name ON clients(legal_name)")
            
            print("✓ Removed ein_last4 column")
        else:
            print("✓ ein_last4 column already removed")
        
        # Check if next_follow_up_date column exists
        cursor.execute("PRAGMA table_info(clients)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if "next_follow_up_date" not in columns:
            print("Adding next_follow_up_date column...")
            cursor.execute("ALTER TABLE clients ADD COLUMN next_follow_up_date DATE")
            print("✓ Added next_follow_up_date column")
        else:
            print("✓ next_follow_up_date column already exists")
        
        conn.commit()
        print("\n✓ Database migration completed successfully!")
        
    except Exception as e:
        conn.rollback()
        print(f"\n✗ Error during migration: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    print("Starting database migration...")
    print("=" * 50)
    migrate_database()

