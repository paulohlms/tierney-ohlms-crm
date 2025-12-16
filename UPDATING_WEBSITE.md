# How to Update Your Hosted Website

## Quick Answer: It's Easy!

After initial setup, updating is just **3 simple steps** that take about 2-3 minutes.

---

## The Update Process (2-3 minutes)

### Step 1: Make Your Changes Locally
1. Edit files on your computer (in `C:\Users\PaulOhlms\Desktop\CRM Tool`)
2. Test locally if you want:
   ```
   python -m uvicorn main:app --reload
   ```
3. Make sure everything works

### Step 2: Upload Changes to GitHub (1 minute)
In PowerShell (in your CRM folder):

```
cd "C:\Users\PaulOhlms\Desktop\CRM Tool"
git add .
git commit -m "Updated dashboard design"
git push
```

That's it! The changes are now on GitHub.

### Step 3: Render Auto-Deploys (1-2 minutes)
- Render automatically detects the changes
- It rebuilds and redeploys your site
- Usually takes 1-2 minutes
- Your site updates automatically!

**You don't need to do anything - Render handles it automatically.**

---

## Detailed Step-by-Step

### Making Changes Locally

1. **Open your files** in any text editor (VS Code, Notepad++, etc.)
2. **Make your changes** (edit templates, add features, etc.)
3. **Test locally** (optional but recommended):
   ```powershell
   cd "C:\Users\PaulOhlms\Desktop\CRM Tool"
   python -m uvicorn main:app --reload
   ```
4. **Check it works** at `http://localhost:8000`

### Uploading Changes

**In PowerShell:**

1. Go to your CRM folder:
   ```
   cd "C:\Users\PaulOhlms\Desktop\CRM Tool"
   ```

2. Check what changed:
   ```
   git status
   ```
   (Shows which files you modified)

3. Add all changes:
   ```
   git add .
   ```

4. Commit with a message:
   ```
   git commit -m "Description of what you changed"
   ```
   Examples:
   - `git commit -m "Updated client list design"`
   - `git commit -m "Added new filter option"`
   - `git commit -m "Fixed revenue calculation"`

5. Push to GitHub:
   ```
   git push
   ```

### Automatic Deployment

- Render watches your GitHub repository
- When you push, it automatically:
  1. Detects the change
  2. Rebuilds your app
  3. Deploys the new version
  4. Your site updates!

**Check deployment status:**
- Go to your Render dashboard
- Click on your service
- See "Events" tab for deployment progress
- Green checkmark = deployed successfully

---

## Common Update Scenarios

### Scenario 1: Update a Template (HTML/CSS)
1. Edit the template file (e.g., `templates/clients_list.html`)
2. Test locally
3. `git add .`
4. `git commit -m "Updated clients list layout"`
5. `git push`
6. Wait 1-2 minutes
7. Refresh your live site - changes are there!

### Scenario 2: Add a New Feature
1. Edit Python files (e.g., `main.py`, `crud.py`)
2. Test locally
3. `git add .`
4. `git commit -m "Added export to Excel feature"`
5. `git push`
6. Wait for deployment
7. New feature is live!

### Scenario 3: Fix a Bug
1. Find and fix the bug
2. Test that it's fixed locally
3. `git add .`
4. `git commit -m "Fixed revenue calculation bug"`
5. `git push`
6. Bug is fixed on live site!

### Scenario 4: Update Database Schema
1. Make model changes
2. Update migration script
3. Test locally
4. `git add .`
5. `git commit -m "Added new client field"`
6. `git push`
7. Render runs migration automatically during build

---

## Quick Reference Commands

**Always start with:**
```
cd "C:\Users\PaulOhlms\Desktop\CRM Tool"
```

**Then:**
```
git add .
git commit -m "Your description here"
git push
```

**That's it!** Your site updates automatically.

---

## Checking if Update Worked

1. Go to your Render dashboard
2. Click on your service
3. Check "Events" tab:
   - ✅ Green checkmark = Success
   - ❌ Red X = Error (check logs)

4. Visit your live site URL
5. Refresh the page (Ctrl+F5 to clear cache)
6. See your changes!

---

## Troubleshooting

### "Nothing to commit"
- You haven't made any changes, or
- You already committed everything
- Run `git status` to see what's happening

### "Permission denied"
- Make sure you're logged into GitHub
- Check your Git credentials

### "Changes not showing on live site"
- Wait 2-3 minutes (deployment takes time)
- Clear browser cache (Ctrl+F5)
- Check Render dashboard for errors
- Make sure you pushed to the right branch (usually "main")

### "Site is down after update"
- Check Render dashboard → Logs
- Look for error messages
- Common issues:
  - Syntax error in code
  - Missing dependency in requirements.txt
  - Database migration failed

---

## Best Practices

1. **Test locally first** - Catch errors before deploying
2. **Use descriptive commit messages** - Helps track what changed
3. **Check Render logs** if something breaks
4. **Make small, frequent updates** - Easier to debug
5. **Keep a backup** - Git is your backup!

---

## Time Breakdown

- **Making changes:** Varies (5 min - 2 hours)
- **Uploading to GitHub:** 1 minute
- **Automatic deployment:** 1-2 minutes
- **Total update time:** Usually 2-3 minutes after you make changes

---

## Summary

**The workflow is:**
1. Edit files locally
2. `git add .` → `git commit -m "message"` → `git push`
3. Wait 1-2 minutes
4. Changes are live!

**It's that simple!** Once set up, updating is just 3 commands and a short wait.

