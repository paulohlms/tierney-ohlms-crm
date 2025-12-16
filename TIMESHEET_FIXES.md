# Timesheet Fixes Applied

## Issues Fixed

### 1. ✅ Undefined Variable Error
**Problem:** `can_view_all` variable was referenced but never defined
**Fix:** Added `can_view_all = has_permission(current_user, "view_all_timesheets")` before using it

### 2. ✅ Missing Permission Checks
**Problem:** Routes didn't check if user has permission to access timesheets
**Fix:** Added permission checks to all timesheet routes:
- List: Checks for `view_own_timesheets` or `view_all_timesheets`
- Create: Checks for `create_timesheets`
- Edit: Already had checks via `can_edit_timesheet()`
- Delete: Already had checks via `can_delete_timesheet()`

## Routes Fixed

1. **GET /timesheets** - List timesheets
   - Added permission check
   - Fixed `can_view_all` variable

2. **GET /timesheets/new** - New timesheet form
   - Added `create_timesheets` permission check

3. **POST /timesheets/new** - Create timesheet
   - Added `create_timesheets` permission check

4. **GET /timesheets/{id}/edit** - Edit form
   - Already had proper checks

5. **POST /timesheets/{id}/edit** - Update timesheet
   - Already had proper checks

6. **POST /timesheets/{id}/delete** - Delete timesheet
   - Already had proper checks

## Testing Checklist

- [ ] Timesheet list page loads
- [ ] Can view own timesheets
- [ ] Admins can view all timesheets
- [ ] Can create new timesheet entry
- [ ] Can edit own timesheet entry
- [ ] Can delete own timesheet entry
- [ ] Permission checks work correctly
- [ ] Error messages display properly

## Next Steps

1. Test the timesheet functionality
2. Verify all routes work correctly
3. Check error handling
4. Test permission system

