# Fix: Database Not Saving on Render

## Problem
SQLite database files are **ephemeral** on Render's free tier - they get deleted when the service restarts or spins down. This is why your data disappears.

## Solution: Use PostgreSQL (Persistent Database)

Render offers **free PostgreSQL databases** that persist your data. Let's set it up!

---

## Step 1: Create PostgreSQL Database on Render (5 minutes)

1. **Go to your Render dashboard:** https://dashboard.render.com
2. **Click "New +"** (top right)
3. **Click "PostgreSQL"**
4. **Fill in:**
   - **Name:** `tierney-ohlms-crm-db` (or any name)
   - **Database:** `crm` (or leave default)
   - **User:** Leave default (auto-generated)
   - **Region:** Same region as your web service
   - **PostgreSQL Version:** Latest (default)
   - **Plan:** **Free** (for now)
5. **Click "Create Database"**
6. **Wait 2-3 minutes** for database to be created

---

## Step 2: Get Database Connection String (2 minutes)

1. **Click on your new PostgreSQL database** in Render dashboard
2. **Look for "Connection String"** or "Internal Database URL"
3. **Copy the connection string** - it looks like:
   ```
   postgresql://username:password@dpg-xxxxx-a.oregon-postgres.render.com/crm
   ```
4. **Save this somewhere safe!** You'll need it in the next step.

**Note:** There are two connection strings:
- **Internal Database URL** - Use this one (for services on Render)
- **External Database URL** - For connecting from outside Render

---

## Step 3: Update Your Code to Use PostgreSQL

We need to modify the code to support PostgreSQL. Here's what to change:

### Option A: Quick Fix (Use Environment Variable)

Update `database.py` to use PostgreSQL when available:

```python
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use PostgreSQL if DATABASE_URL is set, otherwise use SQLite
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # PostgreSQL (for production/hosting)
    # Render provides DATABASE_URL automatically
    if DATABASE_URL.startswith("postgres://"):
        # Render uses postgres:// but SQLAlchemy needs postgresql://
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    engine = create_engine(DATABASE_URL)
else:
    # SQLite (for local development)
    SQLALCHEMY_DATABASE_URL = "sqlite:///./crm.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Option B: Install PostgreSQL Driver

Add to `requirements.txt`:
```
psycopg2-binary==2.9.9
```

---

## Step 4: Connect Database to Your Web Service (3 minutes)

### Method 1: Automatic (Recommended)

1. **Go to your Web Service** in Render dashboard
2. **Click on your service** (tierney-ohlms-crm)
3. **Go to "Environment"** tab
4. **Scroll down to "Environment Variables"**
5. **Look for "DATABASE_URL"** - Render should auto-add it if both services are in the same account
6. **If you don't see it:**
   - Click "Add Environment Variable"
   - **Key:** `DATABASE_URL`
   - **Value:** Paste your PostgreSQL connection string from Step 2
   - Click "Save Changes"

### Method 2: Manual Connection

1. **In your PostgreSQL database page**, find the **"Internal Database URL"**
2. **Copy it**
3. **Go to your Web Service** → "Environment" tab
4. **Add Environment Variable:**
   - **Key:** `DATABASE_URL`
   - **Value:** Paste the connection string
5. **Click "Save Changes"**

---

## Step 5: Update requirements.txt

Make sure `requirements.txt` includes PostgreSQL driver:

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy>=2.0.27
jinja2==3.1.2
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
itsdangerous==2.1.2
psycopg2-binary==2.9.9
```

---

## Step 6: Deploy Updated Code

1. **Update your code** (database.py and requirements.txt)
2. **Commit and push to GitHub:**
   ```powershell
   cd "C:\Users\PaulOhlms\Desktop\CRM Tool"
   git add .
   git commit -m "Add PostgreSQL support for persistent database"
   git push
   ```
3. **Render will auto-deploy** (wait 3-5 minutes)
4. **Database will be created automatically** on first startup

---

## Step 7: Initialize Database (First Time)

After deployment, the database tables will be created automatically when the app starts (because of `Base.metadata.create_all(bind=engine)` in main.py).

**To verify:**
1. Go to your live site
2. Try to log in
3. If login works, database is set up!

**If you need to manually initialize:**
- The bootstrap function in main.py will create admin users automatically
- Or you can add data through the web interface

---

## Alternative: Use Persistent Disk (If Available)

If Render offers persistent disks on your plan:

1. **Go to your Web Service** → "Settings"
2. **Look for "Persistent Disk"** or "Disk" option
3. **Add a disk** (usually 1GB free)
4. **Mount it** to `/opt/render/project/src/data` or similar
5. **Update database path** to use the mounted disk

**But PostgreSQL is better** - it's designed for production and handles multiple users better.

---

## Troubleshooting

### "Module psycopg2 not found"
**Solution:** Make sure `psycopg2-binary==2.9.9` is in `requirements.txt` and you've pushed the update.

### "Connection refused" or "Database not found"
**Solution:** 
- Check that DATABASE_URL environment variable is set correctly
- Make sure you're using the **Internal Database URL** (not External)
- Verify database is running (green status in Render dashboard)

### "Table doesn't exist" errors
**Solution:**
- Database tables are created automatically on first startup
- Check Render logs to see if there are any errors
- You can manually trigger table creation by restarting the service

### Data still not saving
**Solution:**
- Make sure DATABASE_URL is set in environment variables
- Check Render logs for database connection errors
- Verify PostgreSQL database is running (green status)

---

## Summary

**The Problem:** SQLite files are temporary on Render  
**The Solution:** Use PostgreSQL (persistent, free on Render)  
**Steps:** 
1. Create PostgreSQL database on Render
2. Get connection string
3. Update code to use PostgreSQL
4. Add DATABASE_URL environment variable
5. Deploy updated code

**Your data will now persist!** 🎉

