# Running the CRM Application Locally (PowerShell)

## Prerequisites
- Python 3.13 installed
- PowerShell (Windows)

## Step-by-Step Instructions

### Step 1: Navigate to Project Directory
```powershell
cd "C:\Users\PaulOhlms\Desktop\CRM Tool"
```

### Step 2: Create Virtual Environment (if not exists)
```powershell
python -m venv venv
```

### Step 3: Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

**If you get an execution policy error, run this first:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 4: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 5: Verify Database Setup
The app uses SQLite locally (no DATABASE_URL needed). The database file `crm.db` will be created automatically.

**Optional: Delete old database to start fresh**
```powershell
if (Test-Path "crm.db") { Remove-Item "crm.db" }
```

### Step 6: Run the Application
```powershell
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Step 7: Access the Application
Open your browser and go to:
```
http://127.0.0.1:8000
```

### Step 8: Login Credentials
- Email: `admin@tierneyohlms.com`
- Password: `ChangeMe123!`

## Troubleshooting

### If port 8000 is in use:
```powershell
uvicorn main:app --reload --host 127.0.0.1 --port 8001
```

### If you see import errors:
```powershell
pip install --upgrade -r requirements.txt
```

### To see detailed logs:
The application will show logs in the PowerShell window. Look for:
- `[MIGRATION]` messages
- `[FORCE SYNC]` messages (should be skipped for SQLite)
- `[STARTUP]` messages

### To stop the server:
Press `Ctrl+C` in the PowerShell window

## Quick Start (All in One)
```powershell
# Navigate to project
cd "C:\Users\PaulOhlms\Desktop\CRM Tool"

# Activate venv (if exists)
if (Test-Path "venv\Scripts\Activate.ps1") {
    .\venv\Scripts\Activate.ps1
} else {
    python -m venv venv
    .\venv\Scripts\Activate.ps1
}

# Install/upgrade dependencies
pip install --upgrade -r requirements.txt

# Run the app
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

