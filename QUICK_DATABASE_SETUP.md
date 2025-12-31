# Quick Database Setup Guide - Render

## 🚀 Fast Setup (5 Steps)

### Step 1: Create PostgreSQL Database
1. Go to https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Name it: `tierney-ohlms-crm-db`
4. Choose **Starter plan ($7/month)** for always-on, or **Free** for testing
5. Click **"Create Database"**
6. Wait 2 minutes

### Step 2: Copy Connection String
1. Click on your new database
2. Find **"Internal Database URL"**
3. Copy it (looks like: `postgresql://user:pass@host/db`)

### Step 3: Add to Web Service
1. Go to your **Web Service** (your CRM app)
2. Click **"Environment"** tab
3. Click **"Add Environment Variable"**
4. **Key**: `DATABASE_URL`
5. **Value**: Paste the connection string from Step 2
6. Click **"Save Changes"**

### Step 4: Wait for Redeploy
- Render will automatically redeploy (3-5 minutes)
- Check logs to make sure no errors

### Step 5: Test It
1. Visit your website
2. Create a test entry (user, client, etc.)
3. Refresh page - data should still be there ✅

---

## 🔄 Set Up Hourly Backups

### Option A: Render Cron Job (Easiest)

1. **Go to Render Dashboard**
2. **Click "New +"** → **"Cron Job"**
3. **Fill in:**
   - **Name**: `crm-hourly-backup`
   - **Schedule**: `0 * * * *` (every hour)
   - **Command**: `python backup_database.py`
   - **Environment Variables:**
     - `DATABASE_URL`: Your **External Connection String** (from database page)
     - `BACKUP_TOKEN`: Any random string (for security)
4. **Click "Create Cron Job"**

### Option B: Manual Backup Script

If cron jobs aren't available, you can run backups manually or use a different service.

---

## ✅ Verification Checklist

- [ ] PostgreSQL database created
- [ ] `DATABASE_URL` added to web service
- [ ] Web service redeployed successfully
- [ ] Test entry created and persists after refresh
- [ ] Backup cron job created (if using Option A)
- [ ] Backup runs successfully (check logs after 1 hour)

---

## 🆘 Common Issues

**Data not saving?**
- Check `DATABASE_URL` is set correctly
- Check database is running (not paused on free tier)
- Check app logs for errors

**Backup not working?**
- Check cron job logs
- Verify `DATABASE_URL` is set in cron job
- Make sure you're using **External Connection String** for backups

**Need help?**
- Check full guide: `DATABASE_SETUP_RENDER.md`
- Check Render logs for specific errors

---

**That's it! Your database will now persist and backup every hour.** 🎉


