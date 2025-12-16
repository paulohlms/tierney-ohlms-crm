# User Management & Permissions System - Setup Guide

## Overview
A comprehensive user management system with role-based permissions has been added to the CRM. This allows you to control what each user can see and do in the system.

## Initial Setup

### Step 1: Run Database Migration
```bash
python migrate_add_users.py
```

This will:
- Create the `users` table
- Add two admin users:
  - **Paul@tierneyohlms.com** (Admin)
  - **Dan@tierneyohlms.com** (Admin)
  - Default password: `ChangeMe123!` (CHANGE THIS IMMEDIATELY!)

### Step 2: Update Login Route
The login system now uses the database instead of hardcoded users. The migration script creates the initial admin accounts.

### Step 3: First Login
1. Go to http://localhost:8000/login
2. Login with: `Paul@tierneyohlms.com` / `ChangeMe123!`
3. **IMMEDIATELY** go to Settings and change your password!

## Permission System

### Available Permissions

#### Dashboard & Clients
- `view_dashboard` - Access dashboard page
- `view_clients` - View client list and details
- `create_clients` - Add new clients
- `edit_clients` - Modify client information
- `delete_clients` - Remove clients
- `export_clients` - Export client data to CSV

#### Related Data
- `create_contacts` - Add contacts to clients
- `delete_contacts` - Remove contacts
- `create_services` - Add services to clients
- `edit_services` - Modify services
- `delete_services` - Remove services
- `create_tasks` - Add tasks to clients
- `edit_tasks` - Modify tasks
- `delete_tasks` - Remove tasks
- `create_notes` - Add notes to clients
- `delete_notes` - Remove notes

#### Timesheets
- `view_own_timesheets` - View your own time entries (default)
- `view_all_timesheets` - View all users' time entries
- `create_timesheets` - Log time entries (default)
- `edit_own_timesheets` - Edit your own entries (default)
- `edit_all_timesheets` - Edit any user's entries
- `delete_own_timesheets` - Delete your own entries (default)
- `delete_all_timesheets` - Delete any user's entries

#### System
- `view_settings` - Access settings page
- `manage_users` - Create/edit/delete users
- `manage_permissions` - Assign permissions to users

### User Roles

#### Admin (Full Access)
- All permissions automatically enabled
- Can manage users and permissions
- Cannot be restricted
- Examples: Paul@tierneyohlms.com, Dan@tierneyohlms.com

#### Manager
- Typically has most view/create/edit permissions
- Usually cannot delete clients or manage users
- Custom permissions can be assigned

#### Staff (Default)
- Default permissions:
  - View own timesheets
  - Create timesheets
  - Edit own timesheets
  - Delete own timesheets
- Additional permissions must be granted

#### Limited
- Minimal permissions
- Typically only own timesheet access
- Custom permissions can be assigned

## Using the Settings Page

### Accessing Settings
1. Login as an admin user
2. Click "Settings" in the navigation bar
3. You'll see a list of all users

### Adding a New User
1. Click "+ Add User"
2. Fill in:
   - Name
   - Email
   - Role (Staff, Manager, Admin, Limited)
   - Password
3. Check/uncheck permissions as needed
4. Click "Save"

### Editing a User
1. Click "Edit" next to any user
2. Modify:
   - Name
   - Role
   - Password (leave blank to keep current)
   - Active status
   - Permissions
3. Click "Save"

### Deactivating a User
1. Click "Deactivate" next to a user
2. Confirm the action
3. User will be marked inactive (soft delete)

## Permission Enforcement

### How It Works
- Each route checks for required permissions
- Users without permission see "403 Forbidden" error
- Admins bypass all permission checks
- Timesheet permissions check ownership (own vs all)

### Route Protection Examples
- `/dashboard` requires `view_dashboard`
- `/clients` requires `view_clients`
- `/clients/new` requires `create_clients`
- `/settings` requires `view_settings`
- `/settings/users/new` requires `manage_users`

## Default Behavior

### New Users
When creating a new user:
- Default role: Staff
- Default permissions:
  - `view_own_timesheets`: true
  - `create_timesheets`: true
  - `edit_own_timesheets`: true
  - `delete_own_timesheets`: true
- All other permissions: false

### Admin Users
- Role set to "Admin" automatically grants all permissions
- Permission checkboxes are disabled (all checked)
- Cannot be restricted

## Security Notes

1. **Passwords**: Stored as bcrypt hashes (secure)
2. **Sessions**: User data stored in session (server-side)
3. **Permission Checks**: Enforced on every route
4. **Soft Deletes**: Users are deactivated, not deleted
5. **Self-Protection**: Users cannot delete their own accounts

## Troubleshooting

### Can't Access Settings
- Ensure you have `view_settings` permission
- Check that you're logged in as an admin

### Permission Not Working
- Check that permission is assigned in Settings
- Verify user role (Admin bypasses checks)
- Clear browser cache and re-login

### Can't Edit Timesheet
- Check `edit_own_timesheets` or `edit_all_timesheets` permission
- Verify you own the timesheet (if using own permission)

### Migration Errors
- Ensure database exists (run `python seed.py` first if needed)
- Check that SQLite is working
- Verify no existing users table conflicts

## Files Modified

- `models.py` - Added User model
- `schemas.py` - Added User schemas
- `auth.py` - Complete rewrite for database users
- `crud.py` - Added User CRUD operations
- `main.py` - Added Settings routes, permission checks
- `templates/base.html` - Added Settings link
- `templates/settings.html` - New Settings page

## Files Created

- `migrate_add_users.py` - User table migration
- `PERMISSIONS_ANALYSIS.md` - Detailed permissions documentation
- `USER_MANAGEMENT_SETUP.md` - This file

## Next Steps

1. Run migration: `python migrate_add_users.py`
2. Login as admin and change password
3. Add additional users as needed
4. Assign appropriate permissions to each user
5. Test permissions by logging in as different users

