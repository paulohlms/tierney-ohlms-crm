# Pre-Deployment Steps for Render

## ✅ Step 1: Verify Local Instance Works
Your local instance is working! ✅

## Step 2: Generate SECRET_KEY

**Generated SECRET_KEY:**
```
XsVJ_vI3v_8FiOrhV_1Ujpl8c5PtmAM42wNVPsI_WqM
```

**Save this** - you'll need it in Step 6.

## Step 3: Commit All Changes to Git

### 3.1 Check Current Status
```powershell
git status
```

### 3.2 Commit Important Files
```powershell
# Commit the new deployment files
git add RENDER_DEPLOYMENT_CHECKLIST.md PRE_DEPLOYMENT_STEPS.md RUN_LOCALLY.md start_local.ps1 render.yaml

# Commit any code changes (if any)
git add main.py migrations.py crud.py database.py

# Commit everything
git commit -m "Pre-deployment: Add deployment documentation and verify configuration"
```

### 3.3 Push to Repository
```powershell
git push
```

**Action Required:** Run these commands now

## Step 4: Verify Repository Connection

Make sure your GitHub/GitLab repository is:
- ✅ Up to date
- ✅ All code pushed
- ✅ Connected to Render (or ready to connect)

## Step 5: Create PostgreSQL Database on Render

### 5.1 Create Database
1. Go to Render Dashboard: https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name:** `tierney-ohlms-crm-db` (or your choice)
   - **Database:** `crm` (or your choice)
   - **User:** (auto-generated)
   - **Region:** Choose closest to you
   - **Plan:** Free (or your choice)
4. Click **"Create Database"**

### 5.2 Copy Database URL
After creation, you'll see:
- **Internal Database URL** (for linking)
- **External Database URL** (for local testing if needed)

**Action Required:** Create PostgreSQL database on Render

## Step 6: Create Web Service on Render

### 6.1 Create Web Service
1. In Render Dashboard: **"New +"** → **"Web Service"**
2. Connect your repository (GitHub/GitLab)
3. Select your repository and branch (`main`)

### 6.2 Configure Service Settings

**Basic Settings:**
- **Name:** `tierney-ohlms-crm`
- **Environment:** `Python 3`
- **Region:** Same as database
- **Branch:** `main`
- **Root Directory:** (leave empty)

**Build & Deploy:**
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Advanced Settings:**
- **Auto-Deploy:** `Yes` (deploys on git push)
- **Health Check Path:** `/health` or `/` (HEAD request)

### 6.3 Set Environment Variables

Click **"Environment"** tab and add:

1. **SECRET_KEY**
   - Key: `SECRET_KEY`
   - Value: `XsVJ_vI3v_8FiOrhV_1Ujpl8c5PtmAM42wNVPsI_WqM`
   - (Use the generated key from Step 2)

2. **RENDER** (for production detection)
   - Key: `RENDER`
   - Value: `true`

3. **DATABASE_URL** (auto-set when linking)
   - This will be automatically set when you link the PostgreSQL service
   - Don't set it manually

### 6.4 Link PostgreSQL Database

1. In Web Service settings, scroll to **"Add Environment Variable"**
2. Click **"Link Resource"** or **"Add from Resource"**
3. Select your PostgreSQL database
4. Render will automatically add `DATABASE_URL`

**Action Required:** Create Web Service and set environment variables

## Step 7: Verify Configuration

### 7.1 Final Checklist

**Environment Variables:**
- [ ] `SECRET_KEY` = `XsVJ_vI3v_8FiOrhV_1Ujpl8c5PtmAM42wNVPsI_WqM`
- [ ] `RENDER` = `true`
- [ ] `DATABASE_URL` = (auto-set by linking PostgreSQL)

**Commands:**
- [ ] Build Command: `pip install -r requirements.txt`
- [ ] Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Database:**
- [ ] PostgreSQL database created
- [ ] Database linked to Web Service
- [ ] `DATABASE_URL` is set automatically

## Step 8: Deploy

### 8.1 Manual Deploy (First Time)
1. Click **"Manual Deploy"** → **"Deploy latest commit"**
2. Watch the build logs
3. Wait for deployment to complete

### 8.2 Verify Deployment

**Check Logs For:**
- ✅ `[STARTUP] Starting CRM Application`
- ✅ `[BACKGROUND] Creating database tables...`
- ✅ `[BACKGROUND] Running database migrations...`
- ✅ `[MIGRATION] Migrating timesheets table...`
- ✅ `[MIGRATION] Added column 'timesheets.updated_at'`
- ✅ `[MIGRATION] Timesheets table updated`
- ✅ `[STARTUP] Application ready - port should be open now`

**Access Your App:**
- URL will be: `https://tierney-ohlms-crm.onrender.com` (or your custom domain)
- Test login with: `admin@tierneyohlms.com` / `ChangeMe123!`

## Step 9: Post-Deployment Verification

### 9.1 Test All Features
- [ ] Login works
- [ ] Dashboard loads
- [ ] Clients tab loads
- [ ] Prospects tab loads
- [ ] Timesheets tab loads
- [ ] No errors in logs

### 9.2 Check for Errors
If you see errors:
1. Check Render logs
2. Look for `[MIGRATION ERROR]` messages
3. Look for `[CLIENTS]` or `[PROSPECTS]` error messages
4. Verify `DATABASE_URL` is set correctly

## Troubleshooting

### If deployment fails:
1. Check build logs for Python errors
2. Verify all dependencies in `requirements.txt`
3. Check Python version compatibility

### If app starts but tabs don't load:
1. Check logs for `[MIGRATION]` messages
2. Verify timesheets migration ran
3. Check for `UndefinedColumn` errors

### If database connection fails:
1. Verify PostgreSQL database is running
2. Check `DATABASE_URL` is set correctly
3. Verify database is linked to Web Service

## Quick Reference

**SECRET_KEY:** `XsVJ_vI3v_8FiOrhV_1Ujpl8c5PtmAM42wNVPsI_WqM`

**Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Build Command:** `pip install -r requirements.txt`

**Login:** `admin@tierneyohlms.com` / `ChangeMe123!`

