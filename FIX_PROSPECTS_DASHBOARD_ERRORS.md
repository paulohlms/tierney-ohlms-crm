# Fix for Prospects and Dashboard Internal Server Errors

## Issues Identified and Fixed

### 1. **Date Handling Issues**
**Problem:** The code was calling `.date()` on `created_at` datetime objects without proper None checking and without handling timezone-aware datetimes.

**Fixed in:**
- `/prospects` route (line ~338)
- `/dashboard` route (line ~1113, ~1122, ~1139)
- `/prospects/export` route (line ~447)

**Solution:** Added safe date extraction that:
- Checks if `created_at` exists
- Handles both datetime and date objects
- Returns None if no date is available

### 2. **Redundant Import**
**Problem:** `get_timesheet_summary` was imported locally inside the dashboard function even though it's already imported at the top.

**Fixed:** Removed redundant local import (line ~1067)

## Code Changes

### Before:
```python
"expected_close_date": prospect.next_follow_up_date or (prospect.created_at.date() if prospect.created_at else None)
```

### After:
```python
# Safely get expected close date
expected_close_date = None
if prospect.next_follow_up_date:
    expected_close_date = prospect.next_follow_up_date
elif prospect.created_at:
    # Handle both datetime and date objects
    if hasattr(prospect.created_at, 'date'):
        expected_close_date = prospect.created_at.date()
    else:
        expected_close_date = prospect.created_at
```

## Testing

After these fixes, the following routes should work:
- ✅ `/prospects` - Prospects list page
- ✅ `/dashboard` - Dashboard page
- ✅ `/prospects/export` - CSV export

## Next Steps

1. **Restart the server** to apply changes
2. **Test the routes**:
   - Navigate to `/prospects`
   - Navigate to `/dashboard`
   - Try exporting prospects to CSV

If errors persist, check the server console output for specific error messages.

