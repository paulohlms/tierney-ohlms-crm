"""
Migration script to create timesheets table.
Run this after updating models.py to add the new table to existing databases.
"""
import sqlite3
from pathlib import Path

DB_PATH = Path("crm.db")

def migrate():
    """Create timesheets table if it doesn't exist."""
    if not DB_PATH.exists():
        print("Database not found. Run seed.py first to create the database.")
        return
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    try:
        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='timesheets'")
        if cursor.fetchone():
            print("Timesheets table already exists. Skipping...")
            return
        
        # Create timesheets table
        print("Creating timesheets table...")
        cursor.execute("""
            CREATE TABLE timesheets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER NOT NULL,
                staff_member VARCHAR NOT NULL,
                entry_date DATE NOT NULL,
                start_time VARCHAR,
                end_time VARCHAR,
                hours FLOAT NOT NULL,
                project_task VARCHAR,
                description TEXT,
                billable BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (client_id) REFERENCES clients (id)
            )
        """)
        
        # Create indexes
        cursor.execute("CREATE INDEX idx_timesheets_entry_date ON timesheets(entry_date)")
        cursor.execute("CREATE INDEX idx_timesheets_client_id ON timesheets(client_id)")
        
        conn.commit()
        print("Timesheets table created successfully!")
        
    except Exception as e:
        conn.rollback()
        print(f"Error during migration: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()

