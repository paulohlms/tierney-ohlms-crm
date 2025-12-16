# Login Troubleshooting Guide

## Quick Fix

**The system now automatically creates admin users when the server starts!**

### Step 1: Restart Your Server
```bash
# Stop the server (press Ctrl+C)
# Then restart:
python -m uvicorn main:app --reload
```

### Step 2: Check Console Output
When the server starts, you should see one of these:
- `✅ Admin users created!` - Users were just created
- `✅ Found X existing user(s). Skipping bootstrap.` - Users already exist

### Step 3: Try Login
- **Email:** `Paul@tierneyohlms.com`
- **Password:** `ChangeMe123!`

OR

- **Email:** `Dan@tierneyohlms.com`
- **Password:** `ChangeMe123!`

## If Login Still Doesn't Work

### Option 1: Run Test Script
```bash
python test_login.py
```

This will show you:
- How many users exist
- List all users
- Test if login works

### Option 2: Run Migration Manually
```bash
python migrate_add_users.py
```

This will:
- Create users table if it doesn't exist
- Add admin users if they don't exist

### Option 3: Check Server Console
Look for error messages when you start the server. Common issues:

**"Users table not ready yet"**
- This is OK - the table will be created automatically
- Try logging in again after a few seconds

**"Error bootstrapping users"**
- Check the full error message
- May indicate database permission issues

**"No users found" but bootstrap didn't run**
- Check that `bootstrap_admin_users()` is being called
- Look for import errors

### Option 4: Verify Database
The users table should exist. If you're unsure, you can check by running:
```bash
python test_login.py
```

## Common Issues

### Issue: "Invalid email or password"
**Possible causes:**
1. Users table is empty (bootstrap didn't run)
2. Password hash is incorrect
3. Email case sensitivity (try exact case: `Paul@tierneyohlms.com`)

**Solution:**
- Restart server to trigger bootstrap
- Check console for bootstrap messages
- Try running `python migrate_add_users.py`

### Issue: "Login error" (500 error)
**Possible causes:**
1. Users table doesn't exist
2. Database connection issue
3. Import error in auth module

**Solution:**
- Check server console for full error
- Ensure database file exists
- Try running `python seed.py` first

### Issue: Bootstrap runs but login still fails
**Possible causes:**
1. Password hashing issue
2. Case sensitivity in email
3. User marked as inactive

**Solution:**
- Check `test_login.py` output
- Verify email is exact: `Paul@tierneyohlms.com` (capital P)
- Check if user.active = True in database

## Updated Credentials

**OLD (no longer works):**
- admin@firm.com / admin123

**NEW (use these):**
- Paul@tierneyohlms.com / ChangeMe123!
- Dan@tierneyohlms.com / ChangeMe123!

## After Successful Login

1. Go to **Settings** (in navigation)
2. **Change your password immediately!**
3. Add other users as needed

## Still Having Issues?

1. **Check server console** - Look for error messages
2. **Run test script** - `python test_login.py`
3. **Check database** - Ensure `crm.db` exists and is not corrupted
4. **Restart server** - Sometimes a fresh start helps

