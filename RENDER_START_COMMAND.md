# Render Start Command Configuration

## Exact Commands for Render Dashboard

### Pre-deploy Command (Optional - for manual migrations):
```
python migrate_db.py && echo "Migration completed successfully"
```

### Start Command (REQUIRED):
```
python migrate_db.py && uvicorn main:app --host 0.0.0.0 --port $PORT
```

**OR** (if you want to ensure migrations run but don't want to block startup):

```
uvicorn main:app --host 0.0.0.0 --port $PORT
```

The self-healing migration in `main.py` will automatically run on startup, so the second option is recommended.

## Recommended Configuration

### Start Command:
```
uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Why this works:**
- The self-healing migration (`self_heal_schema.py`) runs automatically in `main.py` startup
- It checks and adds missing columns every time the app starts
- No need to run `migrate_db.py` separately
- Faster startup (migration runs in background)

### Alternative (if you want explicit migration before startup):
```
python migrate_db.py && uvicorn main:app --host 0.0.0.0 --port $PORT
```

**When to use this:**
- If you want to see migration output in logs before app starts
- If you want to fail fast if migration fails (though self-healing will still run)

## How Self-Healing Works

1. **On Startup:**
   - `main.py` calls `initialize_database_background()`
   - This runs `self_heal_all_schema()` automatically
   - Missing columns are added immediately
   - Logs show: `[SELF-HEAL] ✓ Successfully added column 'timesheets.staff_member'`

2. **Idempotent:**
   - Can run multiple times safely
   - Checks column existence before adding
   - Skips columns that already exist

3. **Non-Blocking:**
   - Runs in background thread
   - Doesn't delay server startup
   - Render port scan succeeds immediately

## Verification

After deployment, check logs for:
```
[SELF-HEAL] Starting self-healing schema migration for timesheets...
[SELF-HEAL] ✓ Successfully added column 'timesheets.staff_member'
[SELF-HEAL] ✓ Successfully added column 'timesheets.entry_date'
[SELF-HEAL] ✓ Self-healing complete: Added X column(s)
```

## Troubleshooting

If columns are still missing:
1. Check logs for `[SELF-HEAL]` messages
2. Verify DATABASE_URL is set correctly
3. Check database permissions (ALTER TABLE requires proper privileges)
4. Manually verify: `SELECT column_name FROM information_schema.columns WHERE table_name = 'timesheets'`

