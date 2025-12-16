# CRM Permissions Analysis

## Feature Inventory & Permission Requirements

### 1. Dashboard
- **View Dashboard**: View sales pipeline, revenue summaries, charts
- **Permission**: `view_dashboard`

### 2. Clients Module
- **View Clients**: List all clients, search, filter
- **Permission**: `view_clients`
- **Create Client**: Add new clients
- **Permission**: `create_clients`
- **Edit Client**: Modify client information
- **Permission**: `edit_clients`
- **Delete Client**: Remove clients
- **Permission**: `delete_clients`
- **Export Clients**: Export client list to CSV
- **Permission**: `export_clients`
- **View Client Details**: See full client information
- **Permission**: `view_clients` (included in view)

### 3. Contacts
- **View Contacts**: See contacts on client detail page
- **Permission**: `view_clients` (inherited)
- **Create Contact**: Add contacts to clients
- **Permission**: `create_contacts`
- **Delete Contact**: Remove contacts
- **Permission**: `delete_contacts`

### 4. Services
- **View Services**: See services on client detail page
- **Permission**: `view_clients` (inherited)
- **Create Service**: Add services to clients
- **Permission**: `create_services`
- **Edit Service**: Toggle active status
- **Permission**: `edit_services`
- **Delete Service**: Remove services
- **Permission**: `delete_services`

### 5. Tasks
- **View Tasks**: See tasks on client detail page
- **Permission**: `view_clients` (inherited)
- **Create Task**: Add tasks to clients
- **Permission**: `create_tasks`
- **Edit Task**: Update task status
- **Permission**: `edit_tasks`
- **Delete Task**: Remove tasks
- **Permission**: `delete_tasks`

### 6. Notes
- **View Notes**: See notes on client detail page
- **Permission**: `view_clients` (inherited)
- **Create Note**: Add notes to clients
- **Permission**: `create_notes`
- **Delete Note**: Remove notes
- **Permission**: `delete_notes`

### 7. Timesheets
- **View Own Timesheets**: See only your own time entries
- **Permission**: `view_own_timesheets` (default for all users)
- **View All Timesheets**: See all users' time entries
- **Permission**: `view_all_timesheets`
- **Create Timesheet**: Log time entries
- **Permission**: `create_timesheets` (default for all users)
- **Edit Own Timesheets**: Modify your own entries
- **Permission**: `edit_own_timesheets` (default for all users)
- **Edit All Timesheets**: Modify any user's entries
- **Permission**: `edit_all_timesheets`
- **Delete Own Timesheets**: Remove your own entries
- **Permission**: `delete_own_timesheets` (default for all users)
- **Delete All Timesheets**: Remove any user's entries
- **Permission**: `delete_all_timesheets`

### 8. Settings/User Management
- **View Settings**: Access settings page
- **Permission**: `view_settings`
- **Manage Users**: Create, edit, delete users
- **Permission**: `manage_users`
- **Manage Permissions**: Assign permissions to users
- **Permission**: `manage_permissions`

## Permission Categories

### Core Permissions (Client Management)
- `view_clients` - View client list and details
- `create_clients` - Add new clients
- `edit_clients` - Modify client information
- `delete_clients` - Remove clients
- `export_clients` - Export client data

### Related Data Permissions
- `create_contacts` - Add contacts
- `delete_contacts` - Remove contacts
- `create_services` - Add services
- `edit_services` - Modify services
- `delete_services` - Remove services
- `create_tasks` - Add tasks
- `edit_tasks` - Modify tasks
- `delete_tasks` - Remove tasks
- `create_notes` - Add notes
- `delete_notes` - Remove notes

### Timesheet Permissions
- `view_own_timesheets` - View your own entries (default)
- `view_all_timesheets` - View all entries
- `create_timesheets` - Log time (default)
- `edit_own_timesheets` - Edit your own entries (default)
- `edit_all_timesheets` - Edit any entries
- `delete_own_timesheets` - Delete your own entries (default)
- `delete_all_timesheets` - Delete any entries

### System Permissions
- `view_dashboard` - Access dashboard
- `view_settings` - Access settings page
- `manage_users` - Create/edit/delete users
- `manage_permissions` - Assign permissions

## User Roles

### Admin (Full Access)
- All permissions enabled
- Can manage users and permissions
- Examples: Paul@tierneyohlms.com, Dan@tierneyohlms.com

### Manager (Most Access)
- All view permissions
- All create/edit permissions
- Limited delete permissions (no client deletion)
- Cannot manage users/permissions

### Staff (Standard Access)
- View clients, dashboard
- Create/edit own timesheets
- Create contacts, services, tasks, notes
- Cannot delete clients or manage users

### Limited Staff (Restricted Access)
- View own timesheets only
- View assigned clients only (future feature)
- Create own timesheets
- No edit/delete permissions

## Permission Storage

Permissions will be stored as a JSON string in the database:
```json
{
  "view_dashboard": true,
  "view_clients": true,
  "create_clients": false,
  "edit_clients": false,
  "delete_clients": false,
  ...
}
```

## Default Permissions

### New User Defaults
- `view_own_timesheets`: true
- `create_timesheets`: true
- `edit_own_timesheets`: true
- `delete_own_timesheets`: true

All other permissions default to false and must be explicitly granted.

