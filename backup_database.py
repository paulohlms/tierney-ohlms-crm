#!/usr/bin/env python3
"""
Database Backup Script for Render
Runs hourly to backup PostgreSQL database
"""

import os
import subprocess
import sys
from datetime import datetime
import requests

# Configuration
DATABASE_URL = os.getenv("DATABASE_URL")
BACKUP_TOKEN = os.getenv("BACKUP_TOKEN", "change-me-in-production")
BACKUP_WEBHOOK = os.getenv("BACKUP_WEBHOOK", "")  # Optional: webhook for notifications

def log(message):
    """Print timestamped log message"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def backup_database():
    """Create a backup of the PostgreSQL database"""
    
    if not DATABASE_URL:
        log("ERROR: DATABASE_URL environment variable not set")
        return False
    
    # Parse DATABASE_URL
    # Format: postgresql://user:password@host:port/database
    try:
        # Remove postgresql:// prefix
        url = DATABASE_URL.replace("postgresql://", "").replace("postgres://", "")
        
        # Split into parts
        if "@" in url:
            auth_part, host_part = url.split("@", 1)
            if ":" in auth_part:
                user, password = auth_part.split(":", 1)
            else:
                user = auth_part
                password = ""
        else:
            log("ERROR: Invalid DATABASE_URL format")
            return False
        
        if "/" in host_part:
            host_port, database = host_part.rsplit("/", 1)
        else:
            log("ERROR: Invalid DATABASE_URL format")
            return False
        
        if ":" in host_port:
            host, port = host_port.split(":", 1)
        else:
            host = host_port
            port = "5432"
        
        log(f"Connecting to database: {host}:{port}/{database}")
        
        # Create backup filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"backup_{database}_{timestamp}.sql"
        
        # Set PGPASSWORD environment variable for pg_dump
        env = os.environ.copy()
        env["PGPASSWORD"] = password
        
        # Run pg_dump command
        # Note: pg_dump needs to be installed on the system
        cmd = [
            "pg_dump",
            "-h", host,
            "-p", port,
            "-U", user,
            "-d", database,
            "-F", "c",  # Custom format (compressed)
            "-f", backup_filename
        ]
        
        log(f"Running backup command...")
        result = subprocess.run(
            cmd,
            env=env,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            log(f"✅ Backup created successfully: {backup_filename}")
            
            # Get file size
            if os.path.exists(backup_filename):
                size = os.path.getsize(backup_filename)
                size_mb = size / (1024 * 1024)
                log(f"Backup size: {size_mb:.2f} MB")
            
            # Optional: Upload to cloud storage or send webhook
            if BACKUP_WEBHOOK:
                try:
                    with open(backup_filename, "rb") as f:
                        files = {"file": (backup_filename, f)}
                        data = {"message": f"Database backup completed: {backup_filename}"}
                        requests.post(BACKUP_WEBHOOK, files=files, data=data, timeout=30)
                    log("✅ Backup notification sent")
                except Exception as e:
                    log(f"⚠️  Failed to send notification: {e}")
            
            return True
        else:
            log(f"❌ Backup failed: {result.stderr}")
            return False
            
    except Exception as e:
        log(f"❌ Error during backup: {str(e)}")
        return False

def cleanup_old_backups(days_to_keep=7):
    """Remove backup files older than specified days"""
    try:
        import glob
        from pathlib import Path
        
        backup_dir = Path(".")
        backup_files = list(backup_dir.glob("backup_*.sql"))
        
        cutoff_date = datetime.now().timestamp() - (days_to_keep * 24 * 60 * 60)
        
        deleted_count = 0
        for backup_file in backup_files:
            if backup_file.stat().st_mtime < cutoff_date:
                backup_file.unlink()
                deleted_count += 1
                log(f"Deleted old backup: {backup_file.name}")
        
        if deleted_count > 0:
            log(f"Cleaned up {deleted_count} old backup(s)")
        
    except Exception as e:
        log(f"⚠️  Error during cleanup: {e}")

if __name__ == "__main__":
    log("=" * 50)
    log("Starting database backup...")
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


