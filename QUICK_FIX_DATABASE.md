# Quick Fix: Make Database Save on Render

## The Problem
SQLite database files get deleted when Render restarts. Your data disappears.

## The Solution
Use PostgreSQL (persistent database) instead of SQLite.

---

## Step-by-Step Fix (15 minutes)

### Step 1: Create PostgreSQL Database on Render

1. **Go to:** https://dashboard.render.com
2. **Click "New +"** (top right)
3. **Click "PostgreSQL"**
4. **Fill in:**
   - **Name:** `tierney-ohlms-crm-db`
   - **Database:** `crm` (or leave default)
   - **Region:** Same as your web service
   - **Plan:** **Free**
5. **Click "Create Database"**
6. **Wait 2-3 minutes**

### Step 2: Get Connection String

1. **Click on your new PostgreSQL database**
2. **Find "Internal Database URL"** (not External)
3. **Copy it** - looks like:
   ```
   postgres://username:password@dpg-xxxxx-a.oregon-postgres.render.com/crm
   ```
4. **Save it!**

### Step 3: Connect to Your Web Service

1. **Go to your Web Service** (tierney-ohlms-crm)
2. **Click "Environment"** tab
3. **Scroll to "Environment Variables"**
4. **Check if "DATABASE_URL" exists:**
   - ✅ **If it exists:** Render auto-connected it! You're done with this step.
   - ❌ **If it doesn't exist:**
     - Click "Add Environment Variable"
     - **Key:** `DATABASE_URL`
     - **Value:** Paste your Internal Database URL from Step 2
     - Click "Save Changes"

### Step 4: Update Code (I've Already Done This!)

The code has been updated to:
- ✅ Use PostgreSQL when `DATABASE_URL` is set
- ✅ Use SQLite for local development
- ✅ Added PostgreSQL driver to requirements.txt

### Step 5: Push Updated Code to GitHub

**In PowerShell:**

```powershell
cd "C:\Users\PaulOhlms\Desktop\CRM Tool"
git add .
git commit -m "Add PostgreSQL support for persistent database"
git push
```

### Step 6: Wait for Auto-Deploy

- Render will detect the push
- It will rebuild your service (3-5 minutes)
- Database tables will be created automatically
- Your data will now persist! 🎉

---

## Verify It Works

1. **Go to your live site**
2. **Log in**
3. **Add a test client**
4. **Refresh the page** - data should still be there!
5. **Restart the service** (in Render dashboard) - data should still be there!

---

## That's It!

Your database will now save permanently. The code automatically:
- Uses PostgreSQL on Render (persistent)
- Uses SQLite locally (for development)

No more lost data! 🎉

