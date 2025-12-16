# Troubleshooting Guide

## Error -102: Connection Refused

This error means the server isn't running. Follow these steps:

### Step 1: Verify Python Installation

1. Open PowerShell or Command Prompt
2. Run: `python --version`
3. If you get an error, Python isn't installed or not in PATH

**To fix:**
- Download Python from https://www.python.org/downloads/
- During installation, check "Add Python to PATH"
- Restart your terminal after installation

### Step 2: Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

If that doesn't work, try:
```powershell
python3 -m pip install -r requirements.txt
```

### Step 3: Seed the Database

```powershell
python seed.py
```

### Step 4: Start the Server

```powershell
python -m uvicorn main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Step 5: Open in Browser

- Go to: `http://localhost:8000` or `http://127.0.0.1:8000`
- Login: `admin@firm.com` / `admin123`

## Quick Fix: Use the Batch File

1. Double-click `start_server.bat`
2. It will automatically:
   - Check Python
   - Install dependencies if needed
   - Seed the database if needed
   - Start the server

## Common Issues

### "Python not found"
- Install Python and add it to PATH
- Or use full path: `C:\Python39\python.exe -m uvicorn main:app --reload`

### "Module not found"
- Run: `python -m pip install -r requirements.txt`

### "Port 8000 already in use"
- Another process is using port 8000
- Change port: `uvicorn main:app --reload --port 8001`
- Then use: `http://localhost:8001`

### "Database locked"
- Close any other instances of the app
- Delete `crm.db` and run `python seed.py` again

## Still Having Issues?

1. Run the test script: `python test_setup.py`
2. Check for error messages in the terminal
3. Make sure you're in the correct directory: `C:\Users\PaulOhlms\Desktop\CRM Tool`

