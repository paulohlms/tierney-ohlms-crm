# Render Deployment Guide - Encoding Fixes

## Quick Deploy After Encoding Fixes

### Step 1: Commit and Push Changes

```bash
# Check what files were changed
git status

# Add all template and encoding fix files
git add templates/*.html
git add fix_all_templates_encoding.py
git add main.py  # If Jinja2 config was updated

# Commit with descriptive message
git commit -m "Fix template encoding: Convert all HTML templates to UTF-8

- Fixed UnicodeDecodeError in templates
- Converted all .html files to clean UTF-8 without BOM
- Updated Jinja2 environment for UTF-8 handling
- Added batch encoding fix script"

# Push to GitHub
git push origin main
```

### Step 2: Verify Before Deploying

```bash
# Run encoding check locally
python fix_all_templates_encoding.py

# Verify all files are clean
python -c "import os; files = [f for f in os.listdir('templates') if f.endswith('.html')]; [print(f'{f}: {\"OK\" if b\"\\xff\" not in open(f\"templates/{f}\", \"rb\").read()[:100] else \"HAS FF\"}') for f in files]"
```

### Step 3: Deploy on Render

1. **Go to Render Dashboard**
   - Navigate to your service
   - Click "Manual Deploy"
   - **IMPORTANT:** Select "Clear build cache & deploy"
   - Click "Deploy"

2. **Why Clear Build Cache?**
   - Render caches Python packages and build artifacts
   - Old corrupted template files might be cached
   - Clearing cache ensures fresh deployment

## Monitoring Render Logs for Encoding Errors

### Accessing Logs

1. **Via Render Dashboard:**
   - Go to your service
   - Click "Logs" tab
   - View real-time logs

2. **Via Render CLI:**
   ```bash
   # Install Render CLI (if not installed)
   npm install -g render-cli
   
   # Login
   render login
   
   # View logs
   render logs <service-name>
   ```

### What to Look For

#### ✅ Success Indicators:
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:10000
[OK] Found 13 existing user(s). Skipping bootstrap.
```

#### ❌ Encoding Error Indicators:
```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xfe
Error loading template: encoding error
```

#### 🔍 Search Commands in Logs:
- Search for: `UnicodeDecodeError`
- Search for: `encoding`
- Search for: `template`
- Search for: `dashboard.html`

### Real-Time Monitoring

```bash
# Watch logs in real-time (Render CLI)
render logs <service-name> --follow

# Or use curl to check health endpoint
curl https://your-app.onrender.com/health
```

## Environment Variables to Enforce UTF-8

### Add These in Render Dashboard

1. **Go to Render Dashboard:**
   - Your Service → Environment
   - Click "Add Environment Variable"

2. **Add These Variables:**

| Variable Name | Value | Purpose |
|--------------|-------|---------|
| `PYTHONIOENCODING` | `utf-8` | Forces Python I/O to UTF-8 |
| `LANG` | `en_US.UTF-8` | Sets system locale to UTF-8 |
| `LC_ALL` | `en_US.UTF-8` | Sets all locale categories to UTF-8 |
| `LC_CTYPE` | `en_US.UTF-8` | Sets character classification to UTF-8 |
| `PYTHONUNBUFFERED` | `1` | Ensures immediate log output |

### How to Add in Render:

1. **Via Dashboard:**
   ```
   Service → Environment → Add Environment Variable
   ```

2. **Via render.yaml (if using):**
   ```yaml
   services:
     - type: web
       name: tierney-ohlms-crm
       envVars:
         - key: PYTHONIOENCODING
           value: utf-8
         - key: LANG
           value: en_US.UTF-8
         - key: LC_ALL
           value: en_US.UTF-8
         - key: LC_CTYPE
           value: en_US.UTF-8
         - key: PYTHONUNBUFFERED
           value: "1"
   ```

## Build Commands to Enforce UTF-8

### Option 1: Pre-Build Script

Create `build.sh`:

```bash
#!/bin/bash
# Pre-build script to ensure UTF-8 encoding

set -e

echo "Setting UTF-8 environment variables..."
export PYTHONIOENCODING=utf-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
export LC_CTYPE=en_US.UTF-8

echo "Verifying template encoding..."
python3 -c "
import os
files = [f for f in os.listdir('templates') if f.endswith('.html')]
for f in files:
    path = f'templates/{f}'
    with open(path, 'rb') as file:
        content = file.read()
        if b'\xff' in content[:100]:
            print(f'ERROR: {f} has FF bytes!')
            exit(1)
        if content.startswith(b'\xef\xbb\xbf'):
            print(f'WARNING: {f} has BOM')
print('All templates verified as UTF-8')
"

echo "Build script completed successfully"
```

**In Render Dashboard:**
- Service → Settings → Build Command
- Add: `chmod +x build.sh && ./build.sh && pip install -r requirements.txt`

### Option 2: Modify Build Command

**In Render Dashboard:**
- Service → Settings → Build Command
- Replace with:
  ```bash
  export PYTHONIOENCODING=utf-8 && export LANG=en_US.UTF-8 && export LC_ALL=en_US.UTF-8 && pip install -r requirements.txt
  ```

### Option 3: Add to requirements.txt Hook

Create `.render-build.sh`:

```bash
#!/bin/bash
export PYTHONIOENCODING=utf-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
pip install -r requirements.txt
```

## Complete Deployment Checklist

### Before Deploying:

- [ ] All template files are UTF-8 (run `python fix_all_templates_encoding.py`)
- [ ] Changes committed to Git
- [ ] Changes pushed to GitHub
- [ ] Jinja2 environment configured for UTF-8 (check `main.py`)

### During Deployment:

- [ ] Clear build cache in Render
- [ ] Monitor logs for encoding errors
- [ ] Check for `UnicodeDecodeError` in logs

### After Deployment:

- [ ] Test login: `https://your-app.onrender.com/login`
- [ ] Test dashboard: `https://your-app.onrender.com/dashboard`
- [ ] Check browser console for errors (F12)
- [ ] Verify no encoding errors in Render logs

## Troubleshooting Persistent Encoding Errors

### If Error Persists After Deploy:

#### Step 1: Verify Files in Git
```bash
# Check file encoding in repository
git ls-files templates/*.html | xargs file

# Should show: "UTF-8 Unicode text"
```

#### Step 2: Force Re-encode All Templates
```bash
# Run fix script
python fix_all_templates_encoding.py

# Force commit
git add -f templates/*.html
git commit -m "Force UTF-8 encoding for all templates"
git push
```

#### Step 3: Add Environment Variables
Add all UTF-8 environment variables listed above in Render dashboard.

#### Step 4: Clear Build Cache Again
- Manual Deploy → Clear build cache & deploy

#### Step 5: Check Render Build Logs
Look for:
- File encoding during build
- Python version (should be 3.12+)
- Any warnings about file encoding

#### Step 6: Verify in Deployed Environment
```bash
# SSH into Render (if available)
# Or check via Render Shell
# Verify template files:
ls -la templates/
file templates/dashboard.html
```

## Render-Specific Configuration

### render.yaml (Optional but Recommended)

Create `render.yaml` in project root:

```yaml
services:
  - type: web
    name: tierney-ohlms-crm
    runtime: python
    buildCommand: |
      export PYTHONIOENCODING=utf-8
      export LANG=en_US.UTF-8
      export LC_ALL=en_US.UTF-8
      pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHONIOENCODING
        value: utf-8
      - key: LANG
        value: en_US.UTF-8
      - key: LC_ALL
        value: en_US.UTF-8
      - key: LC_CTYPE
        value: en_US.UTF-8
      - key: PYTHONUNBUFFERED
        value: "1"
      - key: DATABASE_URL
        sync: false  # Set in Render dashboard
      - key: SECRET_KEY
        sync: false  # Set in Render dashboard
```

## Quick Reference Commands

### Git Commands:
```bash
# Check status
git status

# Add encoding fixes
git add templates/*.html fix_all_templates_encoding.py main.py

# Commit
git commit -m "Fix template encoding to UTF-8"

# Push
git push origin main
```

### Verification Commands:
```bash
# Check encoding locally
python fix_all_templates_encoding.py

# Check for FF bytes
certutil -dump templates\*.html | findstr /C:"FF"

# Verify UTF-8
python -c "with open('templates/dashboard.html', 'rb') as f: print('UTF-8 OK' if f.read().decode('utf-8') else 'ERROR')"
```

### Render Log Monitoring:
```bash
# Search for encoding errors
# In Render logs, search for: UnicodeDecodeError

# Check deployment status
# Render Dashboard → Deploys → Latest deploy
```

## Success Criteria

After deployment, you should see:

✅ **In Render Logs:**
- No `UnicodeDecodeError` messages
- Application starts successfully
- Templates load without errors

✅ **In Browser:**
- Login page loads correctly
- Dashboard loads without errors
- No encoding issues in browser console

✅ **In Application:**
- All templates render correctly
- No 500 errors related to encoding
- All Jinja2 tags work properly

