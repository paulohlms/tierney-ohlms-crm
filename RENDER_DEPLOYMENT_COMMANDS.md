# Render Deployment Commands

## Pre-deploy Command

Run the migration script before the application starts to ensure the database schema is up to date:

```bash
python migrate_db.py
```

**Full command for Render:**
```
python migrate_db.py && echo "Migration completed successfully"
```

## Start Command

Start the FastAPI application with Uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

## Complete Render Configuration

### Pre-deploy Command:
```
python migrate_db.py && echo "Migration completed successfully"
```

### Start Command:
```
uvicorn main:app --host 0.0.0.0 --port $PORT
```

## Environment Variables

Make sure these are set in Render:

- `DATABASE_URL`: Your PostgreSQL connection string (Render automatically provides this)
- `IS_PRODUCTION`: Set to `true` for production (enables HTTPS cookies)

## Migration Script Behavior

The `migrate_db.py` script:

1. ✅ **Idempotent**: Can be run multiple times safely
2. ✅ **Checks before adding**: Verifies columns don't exist before adding
3. ✅ **Handles postgres:// prefix**: Automatically converts to postgresql://
4. ✅ **Comprehensive logging**: Shows exactly what was added
5. ✅ **Exit codes**: Returns 0 on success, 1 on failure

## Verification

After deployment, check the logs for:

```
✓ MIGRATION COMPLETED SUCCESSFULLY
```

If you see errors, check:
- DATABASE_URL is set correctly
- Database is accessible from Render
- Tables exist (run Base.metadata.create_all first if needed)

## Troubleshooting

### Migration fails with "table does not exist"
- The migration script requires tables to exist first
- Ensure `Base.metadata.create_all(engine)` runs before migration
- This happens automatically in `main.py` startup

### Migration shows "already exists" errors
- This is normal - the script is idempotent
- Columns that already exist are skipped
- Check logs for "already exists - skipping" messages

### Still getting UndefinedColumn errors
- Check that migration actually ran (look for "MIGRATION COMPLETE" in logs)
- Verify columns exist: `SELECT column_name FROM information_schema.columns WHERE table_name = 'timesheets'`
- Re-run migration manually if needed

