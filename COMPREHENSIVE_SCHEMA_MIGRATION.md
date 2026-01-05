# Comprehensive Database Schema Migration

## Problem

Multiple tables have schema mismatches between SQLAlchemy models and PostgreSQL database:

1. **services.service_type** does not exist
2. **timesheets.entry_date** does not exist  
3. **contacts.role** does not exist

## Root Cause

The migration system (`migrations.py`) was only handling `users` and `clients` tables. It was missing migrations for:
- `services` table
- `contacts` table
- `timesheets` table
- `tasks` table
- `notes` table

## Solution: Complete Schema Reconciliation

### Model vs Database Analysis

#### **Service Model** (models.py lines 61-78)
**Expected Columns:**
- `id` (Integer, PK)
- `client_id` (Integer, FK, NOT NULL)
- `service_type` (String, NOT NULL) ⚠️ MISSING
- `billing_frequency` (String, optional) ⚠️ MISSING
- `monthly_fee` (Float, optional) ⚠️ MISSING
- `active` (Boolean, default=True) ⚠️ MISSING

#### **Contact Model** (models.py lines 42-58)
**Expected Columns:**
- `id` (Integer, PK)
- `client_id` (Integer, FK, NOT NULL)
- `name` (String, NOT NULL)
- `role` (String, optional) ⚠️ MISSING
- `email` (String, optional) ⚠️ MISSING
- `phone` (String, optional) ⚠️ MISSING

#### **Timesheet Model** (models.py lines 119-141)
**Expected Columns:**
- `id` (Integer, PK)
- `client_id` (Integer, FK, NOT NULL)
- `staff_member` (String, NOT NULL) ⚠️ MISSING
- `entry_date` (Date, NOT NULL, indexed) ⚠️ MISSING
- `start_time` (String, optional) ⚠️ MISSING
- `end_time` (String, optional) ⚠️ MISSING
- `hours` (Float, NOT NULL) ⚠️ MISSING
- `project_task` (String, optional) ⚠️ MISSING
- `description` (Text, optional) ⚠️ MISSING
- `billable` (Boolean, default=True) ⚠️ MISSING
- `created_at` (DateTime, optional) ⚠️ MISSING
- `updated_at` (DateTime, optional) ⚠️ MISSING

#### **Task Model** (models.py lines 81-98)
**Expected Columns:**
- `id` (Integer, PK)
- `client_id` (Integer, FK, NOT NULL)
- `title` (String, NOT NULL) ⚠️ MISSING
- `due_date` (Date, optional) ⚠️ MISSING
- `status` (String, NOT NULL, default="Open") ⚠️ MISSING
- `notes` (Text, optional) ⚠️ MISSING

#### **Note Model** (models.py lines 101-116)
**Expected Columns:**
- `id` (Integer, PK)
- `client_id` (Integer, FK, NOT NULL)
- `content` (Text, NOT NULL) ⚠️ MISSING
- `created_at` (DateTime, optional) ⚠️ MISSING

## Migration Functions Added

### 1. `_migrate_contacts_table()`
Adds missing columns to `contacts` table:
- `role` (VARCHAR)
- `email` (VARCHAR)
- `phone` (VARCHAR)

### 2. `_migrate_timesheets_table()`
Adds missing columns to `timesheets` table:
- `entry_date` (DATE NOT NULL DEFAULT CURRENT_DATE)
- `staff_member` (VARCHAR NOT NULL DEFAULT 'Unknown')
- `start_time` (VARCHAR)
- `end_time` (VARCHAR)
- `hours` (DOUBLE PRECISION NOT NULL DEFAULT 0)
- `project_task` (VARCHAR)
- `description` (TEXT)
- `billable` (BOOLEAN DEFAULT TRUE)
- `created_at` (TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP)
- `updated_at` (TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP)

### 3. `_migrate_tasks_table()`
Adds missing columns to `tasks` table:
- `title` (VARCHAR NOT NULL DEFAULT 'Untitled Task')
- `due_date` (DATE)
- `status` (VARCHAR NOT NULL DEFAULT 'Open')
- `notes` (TEXT)

### 4. `_migrate_notes_table()`
Adds missing columns to `notes` table:
- `content` (TEXT NOT NULL DEFAULT '')
- `created_at` (TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP)

### 5. `_migrate_services_table()` (Already exists, verified)
Adds missing columns to `services` table:
- `service_type` (VARCHAR NOT NULL DEFAULT 'Other')
- `billing_frequency` (VARCHAR)
- `monthly_fee` (DOUBLE PRECISION)
- `active` (BOOLEAN DEFAULT TRUE)

## Migration Flow

The `migrate_database_schema()` function now:
1. Migrates `users` table
2. Migrates `clients` table
3. Migrates `services` table
4. Migrates `contacts` table (NEW)
5. Migrates `timesheets` table (NEW)
6. Migrates `tasks` table (NEW)
7. Migrates `notes` table (NEW)

All migrations run automatically on application startup.

## SQL Generated

### Contacts Table
```sql
ALTER TABLE contacts ADD COLUMN role VARCHAR;
ALTER TABLE contacts ADD COLUMN email VARCHAR;
ALTER TABLE contacts ADD COLUMN phone VARCHAR;
```

### Timesheets Table
```sql
ALTER TABLE timesheets ADD COLUMN entry_date DATE NOT NULL DEFAULT CURRENT_DATE;
ALTER TABLE timesheets ADD COLUMN staff_member VARCHAR NOT NULL DEFAULT 'Unknown';
ALTER TABLE timesheets ADD COLUMN start_time VARCHAR;
ALTER TABLE timesheets ADD COLUMN end_time VARCHAR;
ALTER TABLE timesheets ADD COLUMN hours DOUBLE PRECISION NOT NULL DEFAULT 0;
ALTER TABLE timesheets ADD COLUMN project_task VARCHAR;
ALTER TABLE timesheets ADD COLUMN description TEXT;
ALTER TABLE timesheets ADD COLUMN billable BOOLEAN DEFAULT TRUE;
ALTER TABLE timesheets ADD COLUMN created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE timesheets ADD COLUMN updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP;
```

### Tasks Table
```sql
ALTER TABLE tasks ADD COLUMN title VARCHAR NOT NULL DEFAULT 'Untitled Task';
ALTER TABLE tasks ADD COLUMN due_date DATE;
ALTER TABLE tasks ADD COLUMN status VARCHAR NOT NULL DEFAULT 'Open';
ALTER TABLE tasks ADD COLUMN notes TEXT;
```

### Notes Table
```sql
ALTER TABLE notes ADD COLUMN content TEXT NOT NULL DEFAULT '';
ALTER TABLE notes ADD COLUMN created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP;
```

## Verification

After migration, all tables will have:
- ✅ All columns expected by SQLAlchemy models
- ✅ Proper data types matching models
- ✅ Default values for NOT NULL columns
- ✅ Foreign key constraints preserved

## Result

- ✅ Service creation will work
- ✅ Timesheet summaries will work
- ✅ Client page will load without errors
- ✅ All CRUD operations will work
- ✅ No more schema mismatch errors

