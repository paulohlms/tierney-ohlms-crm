# Step-by-Step: Database Setup & Hourly Backups

Follow these steps in order. Each step builds on the previous one.

---

## 📋 Prerequisites

- ✅ Your app is already deployed on Render
- ✅ You have access to Render dashboard
- ✅ You know your Render website URL

---

## PART 1: Set Up PostgreSQL Database

### Step 1.1: Create Database

1. **Open Render Dashboard**
   - Go to: https://dashboard.render.com
   - Log in

2. **Create New PostgreSQL Database**
   - Click the **"New +"** button (top right)
   - Select **"PostgreSQL"** from the dropdown

3. **Configure Database**
   - **Name**: `tierney-ohlms-crm-db` (or your preferred name)
   - **Database**: `crm_db` (or leave default)
   - **User**: `crm_user` (or leave default)
   - **Region**: Choose closest to you
     - Example: `Oregon (US West)` or `Frankfurt (EU Central)`
   - **PostgreSQL Version**: `16` (or latest available)
   - **Plan**: 
     - **Free** = Spins down after 90 days of inactivity (good for testing)
     - **Starter ($7/month)** = Always on (recommended for production)

4. **Create**
   - Click **"Create Database"**
   - Wait 2-3 minutes for creation

### Step 1.2: Get Connection Strings

1. **Click on your new database** in the dashboard

2. **Find Connection Information**
   - Scroll to **"Connections"** section
   - You'll see two connection strings:

   **a) Internal Database URL** (for your web service)
   ```
   postgresql://crm_user:password@dpg-xxxxx-a.oregon-postgres.render.com/crm_db
   ```
   - ✅ Use this for your web service
   - ✅ Only works from other Render services

   **b) External Connection String** (for backups/outside access)
   ```
   postgresql://crm_user:password@dpg-xxxxx-a.oregon-postgres.render.com:5432/crm_db
   ```
   - ✅ Use this for backups
   - ✅ Works from anywhere

3. **Copy Both Strings**
   - Click the copy icon next to each
   - Save them somewhere safe (text file, password manager, etc.)

---

## PART 2: Connect Your App to Database

### Step 2.1: Add Environment Variable

1. **Go to Your Web Service**
   - In Render dashboard, click on your web service (your CRM app)

2. **Open Environment Tab**
   - Click **"Environment"** in the left sidebar

3. **Add DATABASE_URL**
   - Click **"Add Environment Variable"** button
   - **Key**: `DATABASE_URL`
   - **Value**: Paste the **Internal Database URL** from Step 1.2
   - Click **"Save Changes"**

4. **Wait for Redeploy**
   - Render will automatically redeploy (3-5 minutes)
   - You'll see "Deploying..." status

### Step 2.2: Verify Database Connection

1. **Check Deployment Logs**
   - Go to your web service
   - Click **"Logs"** tab
   - Look for any database connection errors
   - Should see successful connection messages

2. **Test Your Website**
   - Visit your website URL
   - Try creating a test entry:
     - Create a user
     - Create a client
     - Create a timesheet entry
   - **Refresh the page** - data should still be there ✅

3. **If Data Doesn't Save:**
   - Check `DATABASE_URL` is set correctly
   - Check database is running (not paused)
   - Check logs for errors
   - Verify your `database.py` uses `DATABASE_URL` when available

---

## PART 3: Set Up Hourly Backups

### Step 3.1: Choose Backup Method

**Option A: Render Cron Job** (Recommended - Easiest)
- ✅ Built into Render
- ✅ Automatic scheduling
- ✅ Free tier available

**Option B: Background Worker** (Alternative)
- Use if cron jobs aren't available
- Runs continuously

We'll use **Option A** (Cron Job).

### Step 3.2: Create Cron Job

1. **Go to Render Dashboard**
   - Click **"New +"** → **"Cron Job"**

2. **Configure Cron Job**
   - **Name**: `crm-hourly-backup`
   - **Schedule**: `0 * * * *`
     - This means: "Run at minute 0 of every hour"
     - Example: 1:00 PM, 2:00 PM, 3:00 PM, etc.
   - **Command**: `python backup_database_python.py`
   - **Branch**: `main` (or your main branch name)
   - **Root Directory**: Leave empty (or `/` if required)
   - **Plan**: **Free** tier is fine for backups

3. **Add Environment Variables**
   Click **"Add Environment Variable"** and add:

   **Variable 1:**
   - **Key**: `DATABASE_URL`
   - **Value**: Paste the **External Connection String** from Step 1.2
   - (Use External, not Internal, for backups)

   **Variable 2:**
   - **Key**: `BACKUP_TOKEN`
   - **Value**: Any random string (e.g., `my-secret-backup-token-12345`)
   - This is for security

4. **Create**
   - Click **"Create Cron Job"**
   - Wait 1-2 minutes for setup

### Step 3.3: Verify Backup Works

1. **Wait for First Backup**
   - Cron job runs on the hour (e.g., 2:00 PM, 3:00 PM)
   - Or manually trigger: Go to cron job → "Manual Deploy"

2. **Check Logs**
   - Go to your cron job
   - Click **"Logs"** tab
   - Look for:
     - `✅ Backup created successfully`
     - `✅ Backup process completed successfully`

3. **Check Backup Files** (if accessible)
   - Backups are saved as JSON files
   - Format: `backup_YYYYMMDD_HHMMSS.json`
   - Older backups (7+ days) are automatically deleted

---

## PART 4: Verify Everything Works

### Checklist

- [ ] PostgreSQL database created and running
- [ ] `DATABASE_URL` added to web service
- [ ] Web service redeployed successfully
- [ ] Test data created and persists after refresh
- [ ] Cron job created and scheduled
- [ ] Backup runs successfully (check logs)
- [ ] No errors in any logs

### Test Scenarios

1. **Data Persistence Test**
   - Create data on website
   - Close browser
   - Come back later
   - Data should still be there ✅

2. **Backup Test**
   - Wait for next hour
   - Check cron job logs
   - Should see successful backup message ✅

3. **Database Connection Test**
   - Check web service logs
   - Should see no connection errors ✅

---

## 🆘 Troubleshooting

### Problem: "Data not saving"

**Check:**
1. Is `DATABASE_URL` set in web service environment?
2. Is database running? (Free tier spins down after inactivity)
3. Check web service logs for errors
4. Verify `database.py` uses `DATABASE_URL` when available

**Solution:**
- Upgrade to Starter plan ($7/month) for always-on database
- Or manually wake up free tier database (visit database page)

### Problem: "Backup not running"

**Check:**
1. Is cron job created and enabled?
2. Is `DATABASE_URL` set in cron job environment?
3. Are you using **External Connection String** (not Internal)?
4. Check cron job logs for errors

**Solution:**
- Verify environment variables are set correctly
- Check schedule is correct (`0 * * * *`)
- Manually trigger backup to test

### Problem: "Database connection errors"

**Check:**
1. Is connection string correct?
2. Is database in same region as web service?
3. Are you using Internal URL for web service, External for backups?

**Solution:**
- Double-check connection strings
- Make sure database is running
- Verify region matches

---

## 📝 Summary

**What You've Set Up:**
1. ✅ PostgreSQL database on Render
2. ✅ Web service connected to database
3. ✅ Data persistence working
4. ✅ Hourly automated backups

**Your Data Is Now:**
- ✅ Saved permanently (not lost on restart)
- ✅ Backed up every hour
- ✅ Protected from data loss

**Next Steps:**
- Monitor backups for first few days
- Consider upgrading to Starter plan for production
- Set up additional backup storage (S3, etc.) if needed

---

**Congratulations! Your database is now set up and backing up every hour!** 🎉


