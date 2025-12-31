# 🚀 START HERE: Database Setup

## Quick Start (15 minutes)

### 1️⃣ Create Database (5 min)
1. Go to https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Name: `tierney-ohlms-crm-db`
4. Plan: **Starter ($7/month)** for always-on, or **Free** for testing
5. Click **"Create Database"**
6. Wait 2 minutes

### 2️⃣ Get Connection String (1 min)
1. Click your new database
2. Copy **"Internal Database URL"**
   - Looks like: `postgresql://user:pass@host/db`

### 3️⃣ Connect Your App (3 min)
1. Go to your **Web Service**
2. Click **"Environment"** tab
3. Add variable:
   - **Key**: `DATABASE_URL`
   - **Value**: Paste connection string
4. Click **"Save Changes"**
5. Wait 3-5 min for redeploy

### 4️⃣ Test It (2 min)
1. Visit your website
2. Create test data (user/client/timesheet)
3. Refresh page - data should still be there ✅

### 5️⃣ Set Up Backups (4 min)
1. Click **"New +"** → **"Cron Job"**
2. Name: `crm-hourly-backup`
3. Schedule: `0 * * * *` (every hour)
4. Command: `python backup_database_python.py`
5. Add environment variable:
   - **Key**: `DATABASE_URL`
   - **Value**: **External Connection String** (from database page)
6. Click **"Create Cron Job"**

---

## ✅ Done!

Your data now:
- ✅ Saves permanently
- ✅ Backs up every hour
- ✅ Won't be lost

---

## 📚 Need More Help?

- **Quick Guide**: `QUICK_DATABASE_SETUP.md`
- **Detailed Guide**: `DATABASE_SETUP_RENDER.md`
- **Step-by-Step**: `STEP_BY_STEP_DATABASE.md`

---

## 🆘 Problems?

**Data not saving?**
- Check `DATABASE_URL` is set in web service
- Check database is running (not paused)
- Check web service logs

**Backup not working?**
- Check cron job logs
- Verify `DATABASE_URL` is set in cron job
- Use **External** connection string for backups

---

**That's it! Follow the 5 steps above and you're done!** 🎉


