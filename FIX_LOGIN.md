# Fix Login Issues - Quick Guide

## Problem
If login isn't working, the users table might not exist or be empty.

## Solution
The system now **automatically creates admin users** when the server starts if none exist.

## What Happens on Server Start

1. Database tables are created (including `users` table)
2. System checks if any users exist
3. If no users found, automatically creates:
   - **Paul@tierneyohlms.com** / **ChangeMe123!**
   - **Dan@tierneyohlms.com** / **ChangeMe123!**

## How to Fix

### Step 1: Restart Your Server
```bash
# Stop the server (Ctrl+C)
# Then restart:
python -m uvicorn main:app --reload
```

### Step 2: Check Console Output
You should see one of these messages:
- `✅ Admin users created!` - Users were just created
- `✅ Found X existing user(s). Skipping bootstrap.` - Users already exist

### Step 3: Try Login
- Email: `Paul@tierneyohlms.com`
- Password: `ChangeMe123!`

OR

- Email: `Dan@tierneyohlms.com`
- Password: `ChangeMe123!`

## If Still Not Working

### Option 1: Run Migration Manually
```bash
python migrate_add_users.py
```

### Option 2: Check Database
The users table should exist. If you see errors about the table not existing, the database might need to be recreated:
```bash
# Delete old database (backup first!)
# Then run:
python seed.py
python migrate_add_users.py
```

### Option 3: Check Server Logs
Look for error messages in the console when you start the server. Common issues:
- Database file locked
- Permission errors
- Table creation errors

## Updated Login Credentials

**Old (no longer works):**
- admin@firm.com / admin123

**New (use these):**
- Paul@tierneyohlms.com / ChangeMe123!
- Dan@tierneyohlms.com / ChangeMe123!

## After Successful Login

1. **IMMEDIATELY** go to Settings
2. Change your password
3. Add other users as needed

