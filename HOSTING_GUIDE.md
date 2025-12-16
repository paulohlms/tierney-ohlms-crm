# How to Host Your CRM Tool - Step-by-Step Guide

## Time Estimate: 30-60 minutes

## Recommended Option: Render (Easiest & Free)

Render is perfect for internal tools - free tier, easy setup, automatic HTTPS.

---

## Option 1: Render (Recommended - 30-45 minutes)

### What You'll Need:
- A GitHub account (free)
- Your CRM code
- About 30-45 minutes

### Step 1: Create GitHub Account (5 minutes)

1. Go to: https://github.com
2. Click "Sign up"
3. Create a free account
4. Verify your email

### Step 2: Install Git (5 minutes)

1. Go to: https://git-scm.com/download/win
2. Download Git for Windows
3. Run the installer
4. Use all default settings
5. Click "Next" through everything

### Step 3: Upload Your Code to GitHub (10 minutes)

**In PowerShell (in your CRM folder):**

1. Initialize Git:
   ```
   cd "C:\Users\PaulOhlms\Desktop\CRM Tool"
   git init
   ```

2. Create a `.gitignore` file (I'll create this for you)

3. Add all files:
   ```
   git add .
   ```

4. Create first commit:
   ```
   git commit -m "Initial commit"
   ```

5. Create repository on GitHub:
   - Go to: https://github.com/new
   - Name it: `tierney-ohlms-crm` (or any name)
   - Don't check "Initialize with README"
   - Click "Create repository"

6. Connect and push:
   ```
   git remote add origin https://github.com/YOUR-USERNAME/tierney-ohlms-crm.git
   git branch -M main
   git push -u origin main
   ```
   (Replace YOUR-USERNAME with your GitHub username)

### Step 4: Deploy to Render (15 minutes)

1. Go to: https://render.com
2. Sign up with GitHub (click "Get Started for Free")
3. Authorize Render to access GitHub
4. Click "New +" → "Web Service"
5. Connect your repository:
   - Select your `tierney-ohlms-crm` repository
   - Click "Connect"
6. Configure:
   - **Name:** `tierney-ohlms-crm` (or any name)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt && python migrate_database.py`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free
7. Click "Create Web Service"
8. Wait 5-10 minutes for deployment
9. Your site will be at: `https://tierney-ohlms-crm.onrender.com` (or similar)

### Step 5: Set Up Database (5 minutes)

1. In Render dashboard, go to your service
2. Click "Environment"
3. Add environment variable:
   - Key: `DATABASE_URL`
   - Value: `sqlite:///./crm.db` (or we can switch to PostgreSQL later)
4. Click "Save Changes"
5. Service will restart automatically

### Step 6: Access Your CRM

1. Go to your Render URL (from Step 4)
2. Log in with: `admin@firm.com` / `admin123`
3. Done!

---

## Option 2: Railway (Alternative - 30-45 minutes)

### Step 1: Sign Up
1. Go to: https://railway.app
2. Sign up with GitHub

### Step 2: Deploy
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your repository
4. Railway auto-detects Python
5. Add start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Click "Deploy"
7. Wait for deployment
8. Get your URL from the dashboard

---

## Option 3: PythonAnywhere (Good for Python Apps - 20-30 minutes)

### Step 1: Sign Up
1. Go to: https://www.pythonanywhere.com
2. Create free "Beginner" account

### Step 2: Upload Files
1. Go to "Files" tab
2. Upload all your CRM files
3. Or use Git to clone your repo

### Step 3: Set Up Web App
1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Select Python 3.10
5. Click "Next" → "Next"

### Step 4: Configure
1. In "Web" tab, edit WSGI file:
   ```python
   import sys
   path = '/home/YOUR-USERNAME/tierney-ohlms-crm'
   if path not in sys.path:
       sys.path.append(path)
   
   from main import app
   application = app
   ```

2. Set working directory to your CRM folder
3. Click "Reload"
4. Your site will be at: `YOUR-USERNAME.pythonanywhere.com`

---

## What You Need to Change Before Hosting

### 1. Update Secret Key
In `main.py`, change:
```python
app.add_middleware(SessionMiddleware, secret_key="your-secret-key-change-in-production")
```
To a random string (generate one online or use: `openssl rand -hex 32`)

### 2. Update Database Path (if needed)
The current SQLite setup works, but for production you might want PostgreSQL.

### 3. Update Email Settings (optional)
If you want email reminders to work, add SMTP settings in Render's environment variables.

---

## Quick Comparison

| Option | Time | Cost | Difficulty | Best For |
|--------|------|------|------------|----------|
| **Render** | 30-45 min | Free | Easy | **Recommended** |
| Railway | 30-45 min | Free | Easy | Good alternative |
| PythonAnywhere | 20-30 min | Free | Medium | Python-focused |

---

## Security Notes

1. **Change default password** after first login
2. **Use HTTPS** (all options provide this)
3. **Update secret key** (see above)
4. **Consider adding more users** in `auth.py`

---

## Troubleshooting

### "Module not found" errors:
- Make sure `requirements.txt` has all dependencies
- Check build logs in Render/Railway dashboard

### Database issues:
- SQLite works but consider PostgreSQL for production
- Make sure migration ran during build

### Can't access site:
- Check if service is running (green status)
- Look at logs in dashboard
- Make sure port is set correctly

---

## Next Steps After Hosting

1. Update your team with the URL
2. Change default password
3. Add more users in `auth.py`
4. Set up daily email reminders (optional)
5. Bookmark the URL

---

## Need Help?

If you get stuck:
1. Check the error logs in your hosting dashboard
2. Make sure all files are uploaded
3. Verify `requirements.txt` is correct
4. Check that start command is correct

---

**Recommended: Start with Render - it's the easiest!**

