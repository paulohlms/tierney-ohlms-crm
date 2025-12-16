# How to Start Your CRM Server

## Quick Steps

### Step 1: Open PowerShell
Open PowerShell in the CRM Tool folder:
```
C:\Users\PaulOhlms\Desktop\CRM Tool
```

### Step 2: Start the Server
Run this command:
```bash
python -m uvicorn main:app --reload
```

### Step 3: Wait for This Message
You should see:
```
INFO: Uvicorn running on http://127.0.0.1:8000
```

### Step 4: Open in Chrome
Go to:
```
http://localhost:8000
```

OR

```
http://127.0.0.1:8000
```

## Common Issues

### Issue: "Python was not found"
**Solution:** Use the full path:
```bash
C:\Users\PaulOhlms\AppData\Local\Programs\Python\Python314\python.exe -m uvicorn main:app --reload
```

### Issue: "No module named uvicorn"
**Solution:** Install dependencies:
```bash
python -m pip install -r requirements.txt
```

### Issue: Server starts but site won't load
**Solutions:**
1. Make sure you're using `http://localhost:8000` (not https)
2. Try `http://127.0.0.1:8000`
3. Check if another program is using port 8000
4. Make sure the server is actually running (check PowerShell window)

### Issue: Server crashes on startup
**Check:**
- Did you run `python EMERGENCY_FIX.py` to create users?
- Are there error messages in the PowerShell window?
- Copy and paste the error message

## What You Should See

When the server starts successfully, you'll see:
```
INFO: Will watch for changes in these directories: ['C:\\Users\\PaulOhlms\\Desktop\\CRM Tool']
INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO: Started reloader process [XXXXX] using WatchFiles
✅ Found X existing user(s). Skipping bootstrap.
```

Then open Chrome and go to: `http://localhost:8000`

