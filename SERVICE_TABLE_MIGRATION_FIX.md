# Service Table Migration Fix

## Problem

**Error:**
```
sqlalchemy.exc.ProgrammingError: (psycopg.errors.UndefinedColumn)
column "service_type" of relation "services" does not exist
```

**Root Cause:**
The `services` table in PostgreSQL is missing the `service_type` column (and possibly other columns) that the SQLAlchemy `Service` model expects. The migration system was only handling `users` and `clients` tables, but not the `services` table.

## Solution

### 1. Added Services Table Migration Function

Created `_migrate_services_table()` function in `migrations.py` that:
- Checks which columns exist in the `services` table
- Adds missing columns based on the Service model:
  - `service_type` (VARCHAR NOT NULL DEFAULT 'Other')
  - `billing_frequency` (VARCHAR, optional)
  - `monthly_fee` (DOUBLE PRECISION, optional)
  - `active` (BOOLEAN DEFAULT TRUE)

### 2. Integrated into Main Migration Flow

Updated `migrate_database_schema()` to:
- Check if `services` table exists
- Call `_migrate_services_table()` if it exists
- Return success only if all table migrations succeed

## Migration Code

### Added to `migrations.py`:

```python
def _migrate_services_table(conn, inspector) -> bool:
    """
    Add missing columns to services table.
    
    Returns:
        True if all required columns exist or were added, False otherwise
    """
    try:
        columns = {col['name'] for col in inspector.get_columns('services')}
        columns_to_add = []
        
        # Define required columns with their SQL definitions
        # Based on the Service model in models.py
        required_columns = {
            'service_type': "VARCHAR NOT NULL DEFAULT 'Other'",  # Required field
            'billing_frequency': 'VARCHAR',
            'monthly_fee': 'DOUBLE PRECISION',
            'active': 'BOOLEAN DEFAULT TRUE'
        }
        
        for col_name, col_def in required_columns.items():
            if col_name not in columns:
                columns_to_add.append((col_name, col_def))
        
        # Add missing columns
        for col_name, col_def in columns_to_add:
            try:
                # PostgreSQL allows adding NOT NULL columns with DEFAULT in one statement
                # This automatically populates existing rows with the default value
                conn.execute(text(f"ALTER TABLE services ADD COLUMN {col_name} {col_def}"))
                print(f"[MIGRATION] Added column 'services.{col_name}'")
            except Exception as e:
                # Check if column was actually added (might have been added concurrently)
                inspector = inspect(engine)
                current_columns = {col['name'] for col in inspector.get_columns('services')}
                if col_name in current_columns:
                    print(f"[MIGRATION] Column 'services.{col_name}' already exists")
                else:
                    print(f"[MIGRATION ERROR] Could not add column 'services.{col_name}': {e}")
                    return False
        
        # Verify all columns exist
        inspector = inspect(engine)
        final_columns = {col['name'] for col in inspector.get_columns('services')}
        for col_name in required_columns.keys():
            if col_name not in final_columns:
                print(f"[MIGRATION ERROR] Column 'services.{col_name}' is missing after migration")
                return False
        
        return True
    except Exception as e:
        print(f"[MIGRATION ERROR] Error migrating services table: {e}")
        import traceback
        traceback.print_exc()
        return False
```

### Updated `migrate_database_schema()`:

```python
# Migrate services table
services_success = False
if 'services' in inspector.get_table_names():
    services_success = _migrate_services_table(conn, inspector)
else:
    print("[MIGRATION] Services table does not exist - will be created by Base.metadata.create_all")
    services_success = True  # Table will be created fresh

if users_success and clients_success and services_success:
    print("[MIGRATION] Migration completed successfully")
    return True
```

## Service Model (Already Correct)

The `Service` model in `models.py` is correct and matches the migration:

```python
class Service(Base):
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    service_type = Column(String, nullable=False)  # Required
    billing_frequency = Column(String)  # Optional
    monthly_fee = Column(Float)  # Optional
    active = Column(Boolean, default=True)
    
    client = relationship("Client", back_populates="services")
```

## How It Works

1. **On Startup**: The `startup_event` in `main.py` calls `migrate_database_schema()`
2. **Migration Checks**: The function checks if the `services` table exists
3. **Column Detection**: It inspects existing columns in the table
4. **Column Addition**: Missing columns are added with appropriate types and defaults
5. **Verification**: After adding, it verifies all required columns exist

## SQL Generated

The migration will execute SQL like:
```sql
ALTER TABLE services ADD COLUMN service_type VARCHAR NOT NULL DEFAULT 'Other';
ALTER TABLE services ADD COLUMN billing_frequency VARCHAR;
ALTER TABLE services ADD COLUMN monthly_fee DOUBLE PRECISION;
ALTER TABLE services ADD COLUMN active BOOLEAN DEFAULT TRUE;
```

## Result

After this migration runs:
- ✅ `service_type` column will exist (required, with default 'Other')
- ✅ `billing_frequency` column will exist (optional)
- ✅ `monthly_fee` column will exist (optional)
- ✅ `active` column will exist (default TRUE)
- ✅ Service creation will work without database errors

## Deployment

The migration runs automatically on application startup. After deploying:
1. The migration will detect missing columns
2. Add them to the database
3. Service creation will work correctly

No manual database changes required!

