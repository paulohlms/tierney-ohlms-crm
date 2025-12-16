# Fix for Python 3.14 Compatibility Issue

The problem: Python 3.14 is very new and SQLAlchemy 2.0.23 doesn't work with it.

## Solution: Upgrade SQLAlchemy

In PowerShell, run these commands:

### Step 1: Upgrade SQLAlchemy
```
python -m pip install --upgrade sqlalchemy
```

### Step 2: Verify it worked
```
python -c "import sqlalchemy; print(sqlalchemy.__version__)"
```

You should see a version number like 2.0.27 or higher.

### Step 3: Try starting the server again
```
python -m uvicorn main:app --reload
```

---

## Alternative: If upgrade doesn't work

If the upgrade doesn't fix it, you can install Python 3.13 instead (which is more stable):

1. Download Python 3.13 from: https://www.python.org/downloads/
2. Install it (check "Add Python to environment variables")
3. Restart PowerShell
4. Run: `python -m pip install -r requirements.txt`
5. Run: `python seed.py`
6. Run: `python -m uvicorn main:app --reload`

