# Complete Step-by-Step Guide: Host Your CRM Online & Give People Access

## Overview
This guide will walk you through hosting your Tierney & Ohlms CRM online so your team can access it from anywhere. We'll use **Render** (free, easy, recommended).

**Time Required:** 45-60 minutes  
**Cost:** Free (for small teams)

---

## Part 1: Prepare Your Code (15 minutes)

### Step 1: Create a GitHub Account (if you don't have one)

1. Go to: **https://github.com**
2. Click **"Sign up"**
3. Fill in:
   - Username (e.g., `paulohlms`)
   - Email address
   - Password
4. Click **"Create account"**
5. Verify your email (check your inbox)

### Step 2: Install Git (if not already installed)

1. Go to: **https://git-scm.com/download/win**
2. Download **"Git for Windows"**
3. Run the installer
4. **Use all default settings** - just click "Next" through everything
5. Click "Finish"

### Step 3: Upload Your Code to GitHub

**Open PowerShell** and run these commands:

```powershell
# Navigate to your CRM folder
cd "C:\Users\PaulOhlms\Desktop\CRM Tool"

# Initialize Git (if not already done)
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Tierney & Ohlms CRM"

# Create repository on GitHub first, then:
# Go to https://github.com/new
# Name it: tierney-ohlms-crm
# Don't check "Initialize with README"
# Click "Create repository"

# Then connect and push (replace YOUR-USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR-USERNAME/tierney-ohlms-crm.git
git branch -M main
git push -u origin main
```

**Note:** GitHub will ask for your username and password. Use a **Personal Access Token** instead of password:
- Go to: https://github.com/settings/tokens
- Click "Generate new token (classic)"
- Name it: "CRM Deployment"
- Check "repo" permission
- Click "Generate token"
- Copy the token and use it as your password

---

## Part 2: Deploy to Render (20 minutes)

### Step 1: Sign Up for Render

1. Go to: **https://render.com**
2. Click **"Get Started for Free"**
3. Click **"Sign up with GitHub"**
4. Authorize Render to access your GitHub account
5. Complete your profile (name, email)

### Step 2: Create a New Web Service

1. In Render dashboard, click **"New +"** (top right)
2. Click **"Web Service"**
3. **Connect your repository:**
   - You'll see a list of your GitHub repositories
   - Find **"tierney-ohlms-crm"** (or whatever you named it)
   - Click **"Connect"** next to it

### Step 3: Configure Your Service

Fill in these settings:

**Basic Settings:**
- **Name:** `tierney-ohlms-crm` (or any name you like)
- **Region:** Choose closest to you (e.g., "Oregon (US West)")
- **Branch:** `main` (should be default)
- **Root Directory:** Leave empty (default)

**Build & Deploy:**
- **Environment:** `Python 3`
- **Build Command:** 
  ```
  pip install -r requirements.txt
  ```
- **Start Command:**
  ```
  uvicorn main:app --host 0.0.0.0 --port $PORT
  ```

**Plan:**
- Select **"Free"** (for now - you can upgrade later)

### Step 4: Add Environment Variables

**Before clicking "Create Web Service":**

1. Scroll down to **"Environment Variables"** section
2. Click **"Add Environment Variable"**
3. Add this variable:
   - **Key:** `SECRET_KEY`
   - **Value:** Generate a random string:
     - Go to: https://randomkeygen.com/
     - Copy a "CodeIgniter Encryption Keys" (long random string)
     - Paste it as the value
   - Click **"Add"**

**Important:** This keeps your sessions secure!

### Step 5: Deploy!

1. Scroll to bottom
2. Click **"Create Web Service"**
3. **Wait 5-10 minutes** - you'll see build logs
4. When it says **"Live"** (green), you're done!

### Step 6: Get Your URL

1. At the top of your service page, you'll see a URL like:
   ```
   https://tierney-ohlms-crm.onrender.com
   ```
2. **Copy this URL** - this is your live CRM!

---

## Part 3: Set Up Database & Initial Users (10 minutes)

### Step 1: Access Your Live Site

1. Open your Render URL in a browser
2. You should see the login page

### Step 2: First Login

The system will auto-create admin users on first startup. Try logging in with:
- **Email:** `Paul@tierneyohlms.com`
- **Password:** `ChangeMe123!`

**If login doesn't work:**
- The database might need to be initialized
- Check the Render logs (click "Logs" tab in Render dashboard)
- Look for any errors

### Step 3: Change Default Password (IMPORTANT!)

1. Log in successfully
2. Go to **Settings** tab
3. Find your user account
4. Click **"Edit"**
5. Change your password to something secure
6. Click **"Update User"**

---

## Part 4: Give People Access (5 minutes)

### Option A: Create User Accounts in the CRM (Recommended)

1. **Log in** to your live CRM
2. Go to **Settings** tab
3. Click **"+ Add User"** button
4. Fill in:
   - **Name:** User's full name
   - **Email:** Their email address
   - **Role:** Choose:
     - **Admin** - Full access to everything
     - **Manager** - Can view/edit most things
     - **Staff** - Limited access (can view, create timesheets)
   - **Password:** Create a temporary password (they'll change it)
5. Click **"Create User"**
6. **Share credentials** with the user:
   - Send them the CRM URL: `https://your-app.onrender.com`
   - Their email and temporary password
   - Tell them to change password on first login

### Option B: Share Admin Credentials (Quick but Less Secure)

1. Share the admin login:
   - URL: `https://your-app.onrender.com`
   - Email: `Paul@tierneyohlms.com`
   - Password: (your password)
2. **Not recommended** for multiple users - use Option A instead

---

## Part 5: Update Code After Changes (5 minutes)

When you make changes to your CRM and want to update the live site:

### Step 1: Commit Your Changes

**In PowerShell (in your CRM folder):**

```powershell
cd "C:\Users\PaulOhlms\Desktop\CRM Tool"

# Add all changed files
git add .

# Commit with a message
git commit -m "Description of what you changed"

# Push to GitHub
git push
```

### Step 2: Render Auto-Deploys

- Render **automatically detects** when you push to GitHub
- It will **rebuild and redeploy** your site
- Wait 3-5 minutes for deployment to complete
- Your changes will be live!

**To check deployment status:**
- Go to Render dashboard
- Click on your service
- Check the "Events" tab to see deployment progress

---

## Part 6: Security Best Practices

### 1. Change Default Passwords
- ✅ Change admin password immediately
- ✅ Have users change passwords on first login

### 2. Use Strong Passwords
- At least 12 characters
- Mix of letters, numbers, symbols
- Don't reuse passwords

### 3. Limit Admin Access
- Only give **Admin** role to trusted users
- Use **Staff** or **Manager** roles for others

### 4. Regular Backups (Optional)
- Render free tier doesn't include automatic backups
- Consider exporting data periodically:
  - Go to Clients → Export CSV
  - Save the file locally

---

## Troubleshooting

### Problem: "Site not loading" or "502 Bad Gateway"

**Solution:**
1. Check Render dashboard - is service "Live" (green)?
2. Check "Logs" tab for errors
3. Free tier services **spin down after 15 minutes of inactivity**
4. First load after inactivity takes 30-60 seconds (this is normal)
5. Consider upgrading to paid plan to avoid spin-down

### Problem: "Can't log in"

**Solution:**
1. Check if database was initialized:
   - Look at Render logs for errors
   - Database should auto-create on first startup
2. Try creating a new admin user:
   - If you have access to Render shell, you can run:
     ```bash
     python create_admin_users.py
     ```
3. Check that you're using correct email/password

### Problem: "Module not found" errors

**Solution:**
1. Check `requirements.txt` has all dependencies
2. Check Render build logs for installation errors
3. Make sure Python version is compatible (3.10+)

### Problem: "Database locked" errors

**Solution:**
- SQLite can have issues with multiple users
- Consider upgrading to PostgreSQL (Render offers free PostgreSQL)
- Or ensure only one user accesses at a time

### Problem: Changes not showing up

**Solution:**
1. Make sure you pushed to GitHub: `git push`
2. Check Render dashboard - is it deploying?
3. Wait 3-5 minutes for deployment to complete
4. Hard refresh browser: `Ctrl+F5` (Windows) or `Cmd+Shift+R` (Mac)

---

## Quick Reference

### Your Live URL
```
https://your-app-name.onrender.com
```
(Replace `your-app-name` with your actual Render service name)

### Default Admin Login (if auto-created)
- **Email:** `Paul@tierneyohlms.com`
- **Password:** `ChangeMe123!`
- **⚠️ CHANGE THIS IMMEDIATELY!**

### Render Dashboard
- **URL:** https://dashboard.render.com
- **Use this to:** Check status, view logs, update settings

### GitHub Repository
- **URL:** https://github.com/YOUR-USERNAME/tierney-ohlms-crm
- **Use this to:** View code, track changes

---

## Next Steps

1. ✅ **Share the URL** with your team
2. ✅ **Create user accounts** for each team member
3. ✅ **Change all default passwords**
4. ✅ **Test all features** to make sure everything works
5. ✅ **Bookmark the URL** for easy access
6. ✅ **Set up regular backups** (export CSV periodically)

---

## Need Help?

If you get stuck:
1. **Check Render logs** - Click "Logs" tab in Render dashboard
2. **Check GitHub** - Make sure code was pushed successfully
3. **Verify environment variables** - Make sure SECRET_KEY is set
4. **Test locally first** - Make sure it works on your computer before deploying

---

## Summary

**What you've accomplished:**
- ✅ Your CRM is live on the internet
- ✅ Your team can access it from anywhere
- ✅ You can update it by pushing to GitHub
- ✅ It's secure with HTTPS (automatic)
- ✅ It's free (Render free tier)

**Your CRM URL:** `https://your-app-name.onrender.com`

**Congratulations! Your CRM is now online and ready for your team! 🎉**

