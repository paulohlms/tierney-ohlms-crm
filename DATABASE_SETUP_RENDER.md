# Database Setup & Hourly Backups on Render

## Overview
This guide will help you:
1. ✅ Set up PostgreSQL database on Render
2. ✅ Connect your app to the database
3. ✅ Set up hourly automated backups

---

## Step 1: Create PostgreSQL Database on Render

### A. Create New Database

1. **Go to Render Dashboard**: https://dashboard.render.com
2. **Click "New +"** button (top right)
3. **Select "PostgreSQL"**
4. **Fill in the form:**
   - **Name**: `tierney-ohlms-crm-db` (or any name you prefer)
   - **Database**: `crm_db` (or leave default)
   - **User**: `crm_user` (or leave default)
   - **Region**: Choose closest to you (e.g., `Oregon (US West)`)
   - **PostgreSQL Version**: `16` (or latest)
   - **Plan**: 
     - **Free tier** for testing (⚠️ spins down after inactivity)
     - **Starter ($7/month)** for production (always on)
5. **Click "Create Database"**
6. **Wait 2-3 minutes** for database to be created

### B. Get Your Database Connection String

1. **Click on your new database** in the dashboard
2. **Look for "Connection String"** section
3. **Copy the "Internal Database URL"** (for Render services)
   - Looks like: `postgresql://crm_user:password@dpg-xxxxx-a.oregon-postgres.render.com/crm_db`
4. **Also copy the "External Connection String"** (for backups)
   - Looks like: `postgresql://crm_user:password@dpg-xxxxx-a.oregon-postgres.render.com:5432/crm_db`

**⚠️ IMPORTANT**: Save these somewhere safe! You'll need them.

---

## Step 2: Connect Your Web Service to Database

### A. Add Environment Variable to Web Service

1. **Go to your Web Service** (your CRM app) in Render dashboard
2. **Click "Environment"** tab
3. **Click "Add Environment Variable"**
4. **Add this variable:**
   - **Key**: `DATABASE_URL`
   - **Value**: Paste the **Internal Database URL** you copied in Step 1B
5. **Click "Save Changes"**

### B. Verify Your Code Uses DATABASE_URL

Your `database.py` should already be set up to use `DATABASE_URL` if it exists. It should look like this:

```python
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # PostgreSQL (for production)
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    engine = create_engine(DATABASE_URL)
else:
    # SQLite (for local development)
    SQLALCHEMY_DATABASE_URL = "sqlite:///./crm.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### C. Redeploy Your Service

1. **After adding the environment variable**, Render will automatically redeploy
2. **Wait 3-5 minutes** for deployment to complete
3. **Check the logs** to make sure there are no errors

---

## Step 3: Initialize Database Tables

### A. Create Migration Script (if needed)

If your tables don't exist yet, you'll need to create them. Your app should create them automatically on first run, but if not:

1. **Check your `main.py`** - it should have code like:
   ```python
   from database import Base, engine
   Base.metadata.create_all(bind=engine)
   ```

2. **If tables don't exist**, the app will create them on first request

### B. Test Database Connection

1. **Visit your website**
2. **Try creating a user or timesheet entry**
3. **Check if it saves** (refresh the page - data should persist)

---

## Step 4: Set Up Hourly Backups

### A. Create Backup Script

I'll create a backup script for you (see `backup_database.py`)

### B. Create Cron Job on Render

Render doesn't have built-in cron jobs, so we'll use one of these options:

#### **Option 1: Render Cron Job (Recommended)**

1. **Go to Render Dashboard**
2. **Click "New +"** → **"Cron Job"**
3. **Fill in:**
   - **Name**: `crm-hourly-backup`
   - **Schedule**: `0 * * * *` (runs every hour at minute 0)
   - **Command**: `python backup_database.py`
   - **Environment**: Same as your web service
   - **Plan**: Free tier is fine
4. **Add Environment Variables:**
   - `DATABASE_URL`: Your **External Connection String** from Step 1B
   - `BACKUP_TOKEN`: A random secret token (for security)
5. **Click "Create Cron Job"**

#### **Option 2: Background Worker (Alternative)**

If cron jobs aren't available, we can create a background worker service that runs the backup script.

---

## Step 5: Verify Everything Works

### A. Test Database Persistence

1. **Go to your website**
2. **Create a test entry** (user, client, timesheet, etc.)
3. **Refresh the page** - data should still be there
4. **Close browser and come back later** - data should persist

### B. Test Backup

1. **Wait for the next hour** (or manually trigger backup)
2. **Check Render logs** for the cron job
3. **Verify backup file was created** (if stored in Render storage)

---

## Troubleshooting

### Problem: Data still not saving

**Solutions:**
- ✅ Check `DATABASE_URL` environment variable is set correctly
- ✅ Check database is running (not spun down on free tier)
- ✅ Check app logs for database connection errors
- ✅ Verify `database.py` uses `DATABASE_URL` when available

### Problem: Backup not working

**Solutions:**
- ✅ Check cron job is running (check logs)
- ✅ Verify `DATABASE_URL` is set in cron job environment
- ✅ Check backup script has correct permissions
- ✅ Verify external connection string works

### Problem: Database connection errors

**Solutions:**
- ✅ Make sure you're using **Internal Database URL** for web service
- ✅ Make sure database is not paused (free tier spins down)
- ✅ Check database is in same region as web service
- ✅ Verify connection string format is correct

---

## Next Steps

1. ✅ Follow Step 1 to create PostgreSQL database
2. ✅ Follow Step 2 to connect your app
3. ✅ Test that data saves (Step 3)
4. ✅ Set up hourly backups (Step 4)
5. ✅ Verify everything works (Step 5)

**Once you complete these steps, your data will persist and be backed up every hour!** 🎉


