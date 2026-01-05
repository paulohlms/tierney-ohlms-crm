# Schema Drift Analysis Report

## A) Root Cause Analysis

### Problem Identified:
**ORM ↔ Database Schema Drift**

The SQLAlchemy models define columns that don't exist in the actual database, causing:
- Query failures: `psycopg.errors.UndefinedColumn: column timesheets.staff_member does not exist`
- Performance collapse: Queries fail, causing timeouts and hangs
- UI sluggishness: Failed queries block the event loop

### Root Causes:

1. **Incomplete Migrations**
   - Migrations may not have run successfully
   - Table creation may have happened before migrations
   - Migration errors were silently ignored

2. **Model Updates Without Database Updates**
   - Models were updated but migrations weren't applied
   - Database schema was created from an older model version

3. **No Schema Validation**
   - No startup checks to ensure models match database
   - Drift goes undetected until queries fail

## B) Model ↔ DB Diff Report

### Timesheets Table

**Model Definition (models.py:119-141):**
```python
class Timesheet(Base):
    __tablename__ = "timesheets"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    staff_member = Column(String, nullable=False)  # ← MISSING IN DB
    entry_date = Column(Date, nullable=False, index=True)
    start_time = Column(String)
    end_time = Column(String)
    hours = Column(Float, nullable=False)
    project_task = Column(String)
    description = Column(Text)
    billable = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
```

**Database Schema (Expected):**
- `id` ✓
- `client_id` ✓
- `staff_member` ✗ **MISSING**
- `entry_date` ✗ **MISSING**
- `start_time` ✗ **MISSING**
- `end_time` ✗ **MISSING**
- `hours` ✗ **MISSING**
- `project_task` ✗ **MISSING**
- `description` ✗ **MISSING**
- `billable` ✗ **MISSING**
- `created_at` ✗ **MISSING**
- `updated_at` ✗ **MISSING**

**Status:** Table likely exists but is missing most columns.

### Other Tables

Need to validate:
- `clients` - Check for `owner_name`, `owner_email`, `next_follow_up_date`, `last_reminder_sent`, `created_at`
- `users` - Check for `name`, `role`, `permissions`, `active`, `created_at`, `updated_at`
- `services` - Check for `service_type`, `billing_frequency`, `monthly_fee`, `active`
- `contacts` - Check for `role`, `email`, `phone`
- `tasks` - Check for `title`, `due_date`, `status`, `notes`
- `notes` - Check for `content`, `created_at`

## C) Migration Plan

### Strategy: Add Missing Columns to Database

**Rationale:** 
- Models represent the desired state
- Database should be updated to match models
- Safer than removing model columns (could break code)

### Migration Steps:

1. **Validate Current State**
   - Run schema validator to get exact diff
   - Identify all missing columns

2. **Add Missing Columns**
   - Use `ALTER TABLE` with appropriate defaults
   - Handle NOT NULL constraints with defaults
   - Verify columns were added

3. **Update Existing Data**
   - Set default values for new NOT NULL columns
   - Migrate data if needed

4. **Verify Schema**
   - Re-run validator to confirm alignment
   - Test queries to ensure they work

## D) Corrected Models

Models are correct - no changes needed. The issue is the database schema needs to be updated.

## E) Verification Plan

After migration:
1. Run schema validator
2. Test all CRUD operations
3. Test dashboard revenue calculations
4. Test timesheet operations
5. Monitor logs for any schema errors

