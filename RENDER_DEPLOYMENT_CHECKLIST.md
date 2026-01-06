# Render Deployment Checklist - Pre-Deployment Steps

## ✅ Step 1: Verify Local Instance Works
- [x] Application runs locally without errors
- [x] Database (SQLite) works correctly
- [x] Login works
- [x] All tabs (Dashboard, Clients, Prospects, Timesheets) load
- [x] No console errors

## Step 2: Review Code for Render Compatibility

### 2.1 Database Configuration
**File: `database.py`**
- ✅ Uses `DATABASE_URL` environment variable
- ✅ Falls back to SQLite if `DATABASE_URL` not set (local dev)
- ✅ Handles `postgres://` to `postgresql://` conversion
- ✅ Uses psycopg3 (Python 3.13 compatible)

**Action Required:** None - already configured correctly

### 2.2 Environment Variables Needed
**Required for Render:**
- `DATABASE_URL` - Automatically provided by Render PostgreSQL service
- `SECRET_KEY` - Must be set in Render environment variables
- `IS_PRODUCTION` - Should be set to `true` for production

**Action Required:** Set these in Render dashboard

### 2.3 Startup Commands
**Current Start Command:**
```
uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Pre-deploy Command (Optional):**
```
python migrate_db.py
```
OR (recommended - migrations run automatically):
```
# Leave empty - migrations run in startup event
```

**Action Required:** Verify start command in Render

### 2.4 File Structure
**Required Files:**
- ✅ `main.py` - Main application
- ✅ `database.py` - Database connection
- ✅ `models.py` - SQLAlchemy models
- ✅ `crud.py` - CRUD operations
- ✅ `auth.py` - Authentication
- ✅ `migrations.py` - Database migrations
- ✅ `requirements.txt` - Dependencies
- ✅ `templates/` - HTML templates
- ✅ `static/` - CSS/static files

**Action Required:** Verify all files are committed to Git

## Step 3: Git Repository Status

### 3.1 Check Git Status
```powershell
git status
```

**Action Required:** 
- Commit any uncommitted changes
- Push to GitHub/GitLab repository

### 3.2 Verify .gitignore
**Should ignore:**
- `venv/`
- `__pycache__/`
- `*.pyc`
- `crm.db` (local SQLite database)
- `.env` (if using local env file)

**Action Required:** Verify `.gitignore` is correct

## Step 4: Render-Specific Configuration

### 4.1 Python Version
**Current:** Python 3.13 (local)
**Render:** Should match - check Render supports Python 3.13

**Action Required:** Verify Python version in Render

### 4.2 Build Command
**Render Default:**
```
pip install -r requirements.txt
```

**Action Required:** Verify this is correct

### 4.3 Start Command
**Current:**
```
uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Action Required:** Set this in Render dashboard

### 4.4 Health Check
**Current:** `@app.head("/")` route returns 200 OK
**Action Required:** Verify Render health check path

## Step 5: Environment Variables Setup

### 5.1 Required Variables
1. **SECRET_KEY**
   - Generate a secure random string
   - Use: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
   - Set in Render: Environment → Add Environment Variable

2. **IS_PRODUCTION**
   - Value: `true`
   - Set in Render: Environment → Add Environment Variable

3. **DATABASE_URL**
   - Automatically provided by Render PostgreSQL service
   - Link PostgreSQL service to Web Service in Render

**Action Required:** Generate and set SECRET_KEY

## Step 6: Database Setup on Render

### 6.1 Create PostgreSQL Database
1. In Render dashboard: New → PostgreSQL
2. Name: `tierney-ohlms-crm-db` (or your choice)
3. Database: `crm` (or your choice)
4. User: Auto-generated
5. **Copy the Internal Database URL** (for linking)

### 6.2 Link Database to Web Service
1. In Web Service settings
2. Connect to PostgreSQL database
3. Render will automatically set `DATABASE_URL`

**Action Required:** Create PostgreSQL database on Render

## Step 7: Pre-Deployment Verification

### 7.1 Code Review Checklist
- [ ] No hardcoded local paths
- [ ] No local-only imports
- [ ] All environment variables use `os.getenv()`
- [ ] Database connection handles both SQLite and PostgreSQL
- [ ] Migrations run automatically on startup
- [ ] Error handling is comprehensive
- [ ] Logging is sufficient for debugging

### 7.2 Test Locally with PostgreSQL (Optional)
If you want to test with PostgreSQL locally:
1. Install PostgreSQL locally
2. Set `DATABASE_URL` environment variable
3. Run the app locally
4. Verify it works with PostgreSQL

**Action Required:** Optional - test with PostgreSQL locally

## Step 8: Final Pre-Deployment Steps

### 8.1 Commit All Changes
```powershell
git add .
git commit -m "Ready for Render deployment"
git push
```

### 8.2 Verify Repository is Up to Date
- All code changes committed
- All files pushed to remote
- No uncommitted changes

### 8.3 Document Current State
- Note any known issues
- Document login credentials
- Document any manual steps needed

## Step 9: Render Dashboard Configuration

### 9.1 Web Service Settings
- **Name:** `tierney-ohlms-crm` (or your choice)
- **Environment:** Python 3
- **Region:** Choose closest to you
- **Branch:** `main` (or your default branch)
- **Root Directory:** Leave empty (or `./` if needed)
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 9.2 Environment Variables
- `SECRET_KEY` = (generated secure key)
- `IS_PRODUCTION` = `true`
- `DATABASE_URL` = (auto-set by linking PostgreSQL)

### 9.3 Health Check Path
- Path: `/health` or `/` (HEAD request)
- Should return 200 OK

## Step 10: Post-Deployment Verification

After deployment, check:
1. Application starts without errors
2. Database migrations run successfully
3. Login works
4. All tabs load correctly
5. No errors in Render logs

## Quick Reference Commands

### Generate SECRET_KEY:
```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Check Git Status:
```powershell
git status
git log --oneline -5
```

### Test Import Locally:
```powershell
python -c "from main import app; print('OK')"
```

