"""
Quick test script to verify the setup is correct.
Run this to check if all dependencies are installed.
"""
import sys

print("Python version:", sys.version)
print("\nChecking dependencies...")

try:
    import fastapi
    print("✓ FastAPI installed")
except ImportError:
    print("✗ FastAPI NOT installed - run: pip install -r requirements.txt")

try:
    import uvicorn
    print("✓ Uvicorn installed")
except ImportError:
    print("✗ Uvicorn NOT installed - run: pip install -r requirements.txt")

try:
    import sqlalchemy
    print("✓ SQLAlchemy installed")
except ImportError:
    print("✗ SQLAlchemy NOT installed - run: pip install -r requirements.txt")

try:
    import jinja2
    print("✓ Jinja2 installed")
except ImportError:
    print("✗ Jinja2 NOT installed - run: pip install -r requirements.txt")

try:
    from starlette.middleware.sessions import SessionMiddleware
    print("✓ Starlette installed")
except ImportError:
    print("✗ Starlette NOT installed - run: pip install -r requirements.txt")

try:
    from passlib.context import CryptContext
    print("✓ Passlib installed")
except ImportError:
    print("✗ Passlib NOT installed - run: pip install -r requirements.txt")

print("\nChecking project files...")
import os
files_to_check = ["main.py", "models.py", "database.py", "auth.py", "crud.py", "schemas.py"]
for file in files_to_check:
    if os.path.exists(file):
        print(f"✓ {file} exists")
    else:
        print(f"✗ {file} MISSING")

print("\n" + "="*50)
print("If all checks passed, you can run:")
print("  python seed.py")
print("  uvicorn main:app --reload")
print("="*50)

