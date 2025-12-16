# Fix User Creation Internal Error

## What I Fixed

1. ✅ Added error handling to the user creation route
2. ✅ Added better error messages in the Settings page
3. ✅ Fixed password hashing to use bcrypt directly (Python 3.14 compatible)

## How to See the Actual Error

**The error details will now show in:**
1. **Server console** (PowerShell window) - Look for "Error creating user:" or "Error in create_user:"
2. **Settings page** - You'll see a red error message at the top

## Common Causes

### 1. Password Hashing Issue (Most Likely)
- The bcrypt library might not be working correctly
- **Solution:** The hash_password function now uses bcrypt directly

### 2. Email Already Exists
- You're trying to create a user with an email that's already in use
- **Solution:** Use a different email address

### 3. Database Locked
- Another process is using the database
- **Solution:** Close any other instances of the CRM

### 4. Missing Permissions
- The user creating the account doesn't have `manage_users` permission
- **Solution:** Make sure you're logged in as an admin

## Next Steps

1. **Try creating a user again**
2. **Check the PowerShell window** where your server is running
3. **Look for error messages** - they'll tell you exactly what went wrong
4. **Copy the error message** and share it with me

## If It Still Doesn't Work

The error message in the PowerShell window will tell us exactly what's wrong. Common errors:

- **"password cannot be longer than 72 bytes"** - Already fixed
- **"UNIQUE constraint failed"** - Email already exists
- **"no such table: users"** - Database not set up correctly
- **"database is locked"** - Close other instances

Let me know what error message you see!

