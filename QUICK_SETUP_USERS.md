# Quick Setup - User Management System

## Step 1: Run Migration
```bash
python migrate_add_users.py
```

This creates:
- `users` table in database
- Two admin accounts:
  - **Paul@tierneyohlms.com** (password: `ChangeMe123!`)
  - **Dan@tierneyohlms.com** (password: `ChangeMe123!`)

## Step 2: Restart Server
```bash
python -m uvicorn main:app --reload
```

## Step 3: First Login
1. Go to http://localhost:8000/login
2. Login with: `Paul@tierneyohlms.com` / `ChangeMe123!`
3. **IMMEDIATELY** go to Settings and change your password!

## Step 4: Access Settings
1. Click "Settings" in navigation (only visible to admins)
2. You'll see the user management interface

## Step 5: Add Users
1. Click "+ Add User"
2. Fill in:
   - Name
   - Email
   - Role (Staff, Manager, Admin, Limited)
   - Password
3. Check/uncheck permissions as needed
4. Click "Save"

## Available Permissions (26 total)

### Dashboard & Clients
- View Dashboard
- View Clients
- Create Clients
- Edit Clients
- Delete Clients
- Export Clients

### Related Data
- Create/Delete Contacts
- Create/Edit/Delete Services
- Create/Edit/Delete Tasks
- Create/Delete Notes

### Timesheets
- View Own Timesheets (default)
- View All Timesheets
- Create Timesheets (default)
- Edit Own Timesheets (default)
- Edit All Timesheets
- Delete Own Timesheets (default)
- Delete All Timesheets

### System
- View Settings
- Manage Users
- Manage Permissions

## Default Permissions

**New Staff Users** get:
- View Own Timesheets ✓
- Create Timesheets ✓
- Edit Own Timesheets ✓
- Delete Own Timesheets ✓

**Admin Users** get ALL permissions automatically.

## Important Notes

- **Change default passwords immediately!**
- Admins have full access (cannot be restricted)
- Users can only edit/delete their own timesheets (unless granted permission)
- Settings page only visible to users with `view_settings` permission
- User management requires `manage_users` permission

