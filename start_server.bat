@echo off
echo ========================================
echo Starting CRM Server
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found!
echo.

REM Check if dependencies are installed
echo Checking dependencies...
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
) else (
    echo Dependencies OK
)

echo.

REM Check if database exists
if not exist "crm.db" (
    echo Database not found. Seeding database...
    python seed.py
    if errorlevel 1 (
        echo ERROR: Failed to seed database
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo Starting server...
echo Open http://localhost:8000 in your browser
echo Press CTRL+C to stop the server
echo ========================================
echo.

python -m uvicorn main:app --reload

