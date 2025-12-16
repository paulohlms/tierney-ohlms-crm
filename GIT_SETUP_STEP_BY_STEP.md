# Step-by-Step: Git Setup & Upload to GitHub

## Problem: Git Not Found

If you see `git : The term 'git' is not recognized`, Git isn't installed yet.

---

## Step 1: Install Git (5 minutes)

### Option A: Download & Install Git

1. **Go to:** https://git-scm.com/download/win
2. **Click the big download button** (it will say something like "Click here to download")
3. **Run the installer** (Git-2.x.x-64-bit.exe)
4. **Use ALL default settings** - just keep clicking "Next":
   - ✅ Click "Next" on every screen
   - ✅ Don't change any options
   - ✅ Click "Install" when you get to the end
   - ✅ Click "Finish" when done

5. **IMPORTANT:** After installation, **close and reopen PowerShell**:
   - Close your current PowerShell window completely
   - Open a NEW PowerShell window
   - This makes Git available

### Option B: Check if Git is Already Installed

Sometimes Git is installed but PowerShell needs to be restarted.

1. **Close PowerShell completely**
2. **Open a NEW PowerShell window**
3. **Test Git:**
   ```powershell
   git --version
   ```
4. If you see a version number (like `git version 2.43.0`), Git is installed! ✅
5. If you still see an error, use Option A above

---

## Step 2: Verify You're in the Right Folder

**In your NEW PowerShell window:**

```powershell
cd "C:\Users\PaulOhlms\Desktop\CRM Tool"
```

**Check you're in the right place:**
```powershell
pwd
```

**Should show:** `C:\Users\PaulOhlms\Desktop\CRM Tool`

**List files to verify:**
```powershell
dir
```

**You should see:** `main.py`, `requirements.txt`, `templates`, etc.

---

## Step 3: Initialize Git (One Command at a Time)

**Run these commands ONE AT A TIME** (wait for each to finish):

### Command 1: Initialize Git
```powershell
git init
```

**Expected output:** `Initialized empty Git repository in C:/Users/PaulOhlms/Desktop/CRM Tool/.git/`

**If you see an error:** Let me know what it says!

---

### Command 2: Add All Files
```powershell
git add .
```

**Expected output:** (No output is normal - this means it worked!)

**If you see errors:** Let me know!

---

### Command 3: Create First Commit
```powershell
git commit -m "Initial commit: Tierney & Ohlms CRM"
```

**Expected output:** Something like:
```
[main (root-commit) abc1234] Initial commit: Tierney & Ohlms CRM
 X files changed, Y insertions(+)
```

**If you see an error about email/name:**
- Git needs to know who you are. Run these first:
  ```powershell
  git config --global user.name "Your Name"
  git config --global user.email "your-email@example.com"
  ```
- Then try the commit again

---

## Step 4: Create GitHub Repository (In Browser)

**Before pushing, you need to create the repository on GitHub:**

1. **Go to:** https://github.com/new
2. **Fill in:**
   - **Repository name:** `tierney-ohlms-crm` (or any name you like)
   - **Description:** (optional) "Tierney & Ohlms CRM"
   - **Visibility:** Choose "Private" (recommended) or "Public"
   - **DO NOT check** "Add a README file"
   - **DO NOT check** "Add .gitignore"
   - **DO NOT check** "Choose a license"
3. **Click "Create repository"**

**You'll see a page with instructions - DON'T follow those yet!**

---

## Step 5: Connect to GitHub (Back in PowerShell)

**You'll need your GitHub username.** If you don't know it:
- Go to: https://github.com
- Click your profile picture (top right)
- Your username is shown there

**Then run these commands (replace YOUR-USERNAME with your actual GitHub username):**

### Command 1: Connect to GitHub
```powershell
git remote add origin https://github.com/YOUR-USERNAME/tierney-ohlms-crm.git
```

**Replace `YOUR-USERNAME` with your actual GitHub username!**

**Example:** If your username is `paulohlms`, the command would be:
```powershell
git remote add origin https://github.com/paulohlms/tierney-ohlms-crm.git
```

**Expected output:** (No output means it worked!)

---

### Command 2: Set Branch Name
```powershell
git branch -M main
```

**Expected output:** (No output is normal)

---

### Command 3: Push to GitHub
```powershell
git push -u origin main
```

**This is where you'll be asked for credentials:**

**GitHub will ask for:**
- **Username:** Your GitHub username
- **Password:** **DON'T use your GitHub password!** Use a Personal Access Token instead

---

## Step 6: Create Personal Access Token (For Password)

**GitHub requires a token instead of password:**

1. **Go to:** https://github.com/settings/tokens
2. **Click:** "Generate new token" → "Generate new token (classic)"
3. **Fill in:**
   - **Note:** `CRM Deployment` (or any name)
   - **Expiration:** Choose "90 days" or "No expiration" (your choice)
   - **Scopes:** Check **"repo"** (this gives access to repositories)
4. **Scroll down and click:** "Generate token"
5. **IMPORTANT:** Copy the token immediately! It looks like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - You won't be able to see it again!
   - Paste it somewhere safe temporarily

**Back in PowerShell:**
- When it asks for **Password**, paste your token (the `ghp_...` string)
- Press Enter

**Expected output:**
```
Enumerating objects: X, done.
Counting objects: 100% (X/X), done.
Writing objects: 100% (X/X), done.
To https://github.com/YOUR-USERNAME/tierney-ohlms-crm.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

**🎉 Success! Your code is now on GitHub!**

---

## Troubleshooting

### Error: "fatal: not a git repository"
**Solution:** Make sure you ran `git init` first and you're in the CRM Tool folder

### Error: "remote origin already exists"
**Solution:** Run this first:
```powershell
git remote remove origin
```
Then try `git remote add origin` again

### Error: "Authentication failed"
**Solution:** 
- Make sure you're using a Personal Access Token, not your password
- Make sure the token has "repo" permission
- Try generating a new token

### Error: "repository not found"
**Solution:**
- Make sure you created the repository on GitHub first
- Check that the repository name matches exactly
- Make sure your username is correct

### Error: "git config" errors
**Solution:** Run these first:
```powershell
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

---

## What's Next?

Once your code is on GitHub, you can proceed to **Part 2: Deploy to Render** in the hosting guide!

---

## Quick Command Reference

**If you need to start over:**
```powershell
# Make sure you're in the right folder
cd "C:\Users\PaulOhlms\Desktop\CRM Tool"

# Initialize Git
git init

# Add files
git add .

# Commit
git commit -m "Initial commit: Tierney & Ohlms CRM"

# Connect to GitHub (replace YOUR-USERNAME)
git remote add origin https://github.com/YOUR-USERNAME/tierney-ohlms-crm.git

# Set branch
git branch -M main

# Push (will ask for username and token)
git push -u origin main
```

