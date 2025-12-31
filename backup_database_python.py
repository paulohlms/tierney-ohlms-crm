#!/usr/bin/env python3
"""
Database Backup Script for Render (Python-only version)
Uses psycopg to backup PostgreSQL database without requiring pg_dump
Runs hourly to backup PostgreSQL database
"""

import os
import sys
from datetime import datetime
import json

try:
    import psycopg
    from psycopg import sql
except ImportError:
    print("ERROR: psycopg not installed. Install with: pip install psycopg[binary]")
    sys.exit(1)

# Configuration
DATABASE_URL = os.getenv("DATABASE_URL")
BACKUP_TOKEN = os.getenv("BACKUP_TOKEN", "change-me-in-production")

def log(message):
    """Print timestamped log message"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def get_table_names(conn):
    """Get list of all tables in the database"""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
        return [row[0] for row in cur.fetchall()]

def backup_table(conn, table_name):
    """Backup a single table's data"""
    with conn.cursor() as cur:
        # Get table structure
        cur.execute(f"""
            SELECT column_name, data_type, character_maximum_length
            FROM information_schema.columns
            WHERE table_name = %s
            ORDER BY ordinal_position;
        """, (table_name,))
        columns = cur.fetchall()
        
        # Get all data
        cur.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name)))
        rows = cur.fetchall()
        
        return {
            "table_name": table_name,
            "columns": [col[0] for col in columns],
            "column_types": {col[0]: col[1] for col in columns},
            "row_count": len(rows),
            "data": [[str(val) if val is not None else None for val in row] for row in rows]
        }

def backup_database():
    """Create a backup of the PostgreSQL database"""
    
    if not DATABASE_URL:
        log("ERROR: DATABASE_URL environment variable not set")
        return False
    
    try:
        log(f"Connecting to database...")
        
        # Connect to database
        conn = psycopg.connect(DATABASE_URL)
        
        try:
            # Get all tables
            tables = get_table_names(conn)
            log(f"Found {len(tables)} tables: {', '.join(tables)}")
            
            if not tables:
                log("⚠️  No tables found in database")
                return True
            
            # Backup each table
            backup_data = {
                "backup_timestamp": datetime.now().isoformat(),
                "database_url": DATABASE_URL.split("@")[-1] if "@" in DATABASE_URL else "hidden",
                "tables": {}
            }
            
            for table in tables:
                log(f"Backing up table: {table}")
                try:
                    table_data = backup_table(conn, table)
                    backup_data["tables"][table] = table_data
                    log(f"  ✅ {table}: {table_data['row_count']} rows")
                except Exception as e:
                    log(f"  ❌ Error backing up {table}: {e}")
                    backup_data["tables"][table] = {"error": str(e)}
            
            # Save backup to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"backup_{timestamp}.json"
            
            with open(backup_filename, "w", encoding="utf-8") as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
            
            # Get file size
            size = os.path.getsize(backup_filename)
            size_mb = size / (1024 * 1024)
            
            log(f"✅ Backup created: {backup_filename} ({size_mb:.2f} MB)")
            
            # Also create a compressed version if data is large
            if size > 1024 * 1024:  # If larger than 1MB
                try:
                    import gzip
                    compressed_filename = f"{backup_filename}.gz"
                    with open(backup_filename, "rb") as f_in:
                        with gzip.open(compressed_filename, "wb") as f_out:
                            f_out.writelines(f_in)
                    compressed_size = os.path.getsize(compressed_filename) / (1024 * 1024)
                    log(f"✅ Compressed backup: {compressed_filename} ({compressed_size:.2f} MB)")
                    # Optionally remove uncompressed version to save space
                    # os.remove(backup_filename)
                except ImportError:
                    log("⚠️  gzip not available, skipping compression")
            
            return True
            
        finally:
            conn.close()
            
    except Exception as e:
        log(f"❌ Error during backup: {str(e)}")
        import traceback
        log(traceback.format_exc())
        return False

def cleanup_old_backups(days_to_keep=7):
    """Remove backup files older than specified days"""
    try:
        import glob
        from pathlib import Path
        
        backup_dir = Path(".")
        backup_files = list(backup_dir.glob("backup_*.json*"))
        
        cutoff_date = datetime.now().timestamp() - (days_to_keep * 24 * 60 * 60)
        
        deleted_count = 0
        total_size_freed = 0
        for backup_file in backup_files:
            if backup_file.stat().st_mtime < cutoff_date:
                size = backup_file.stat().st_size
                backup_file.unlink()
                deleted_count += 1
                total_size_freed += size
                log(f"Deleted old backup: {backup_file.name}")
        
        if deleted_count > 0:
            size_mb = total_size_freed / (1024 * 1024)
            log(f"Cleaned up {deleted_count} old backup(s), freed {size_mb:.2f} MB")
        
    except Exception as e:
        log(f"⚠️  Error during cleanup: {e}")

if __name__ == "__main__":
    log("=" * 50)
    log("Starting database backup (Python version)...")
    log("=" * 50)
    
    success = backup_database()
    
    # Cleanup old backups (keep last 7 days)
    cleanup_old_backups(days_to_keep=7)
    
    if success:
        log("=" * 50)
        log("✅ Backup process completed successfully")
        log("=" * 50)
        sys.exit(0)
    else:
        log("=" * 50)
        log("❌ Backup process failed")
        log("=" * 50)
        sys.exit(1)


