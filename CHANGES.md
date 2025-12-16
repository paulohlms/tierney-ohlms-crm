# CRM Improvements - Change Log

## Summary of Changes

This document outlines all improvements made to the Tierney & Ohlms CRM system.

---

## 1. Client Model Updates

### Changes Made:
- ✅ **Removed EIN field** - No longer stored or displayed
- ✅ **Added "Dead" status** - For lost prospects
- ✅ **Added "Unknown" entity type** - For clients where entity type is not yet determined
- ✅ **Added `next_follow_up_date` field** - Tracks when to follow up with prospects

### Migration:
Run the migration script to update existing databases:
```bash
python migrate_database.py
```

This will:
- Remove the `ein_last4` column
- Add the `next_follow_up_date` column
- Preserve all existing data

---

## 2. Enhanced Clients List Page

### New Features:

#### Inline Editing
- **Entity Type**: Dropdown directly in the table
- **Fiscal Year End**: Text input directly in the table
- **Status**: Dropdown directly in the table
- Changes save immediately without page refresh

#### Revenue Column
- Shows calculated annual revenue for each client
- Based on sum of all active services
- Calculation: Monthly × 12, Quarterly × 4, Annual × 1

#### Sorting
- Sort by: Client Name, Status, or Revenue
- Click column headers to sort (ascending/descending)
- Sort indicators (↑↓) show current sort

#### Filtering
- **Status filter**: Filter by any status (Active, Prospect, Dead, etc.)
- **Entity Type filter**: Filter by entity type
- **Follow-Up filter**: 
  - "Needed": Prospects due today or overdue
  - "Overdue": Prospects past their follow-up date
- **Search**: Still works for client name search

#### Export to CSV
- Export button exports filtered client list
- Includes all client data and calculated revenue
- Filename includes date: `clients_export_YYYYMMDD.csv`

---

## 3. Prospect Follow-Up Tracking

### Features:
- **Next Follow-Up Date** field on client form
- Visual indicators on clients list:
  - Red (overdue): Past follow-up date
  - Orange (due today): Follow-up date is today
- Filter to see prospects needing follow-up

### Future Automation Ready:
- Database structure supports automated email reminders
- See `daily_reminders.py` for implementation

---

## 4. Email Automation (Phase 1 - Internal)

### Implementation:
- **Email Service Abstraction** (`email_service.py`)
  - Easy to swap email providers (SMTP, SendGrid, AWS SES, etc.)
  - Currently supports SMTP and Console (for development)

- **Daily Reminder Job** (`daily_reminders.py`)
  - Sends internal reminder emails about prospects needing follow-up
  - Run daily via cron or task scheduler

### Setup:
1. Configure email (optional - defaults to console output):
   ```bash
   export SMTP_HOST=smtp.example.com
   export SMTP_PORT=587
   export SMTP_USER=your-email@example.com
   export SMTP_PASSWORD=your-password
   export EMAIL_FROM=crm@tierneyohlms.com
   ```

2. Configure reminder recipients:
   ```bash
   export REMINDER_EMAILS=user1@example.com,user2@example.com
   ```

3. Schedule daily job:
   - **Windows**: Task Scheduler
   - **Linux/Mac**: Cron: `0 9 * * * /path/to/python /path/to/daily_reminders.py`

### Testing:
Run manually to test:
```bash
python daily_reminders.py
```

---

## 5. Dashboard

### New Dashboard Page (`/dashboard`)

Shows key metrics:
- **Monthly Recurring Revenue (MRR)**: Sum of monthly fees × 12
- **Annualized Revenue (ARR)**: Total annual revenue from all active services
- **Active Clients**: Count of clients with "Active" status
- **Prospects**: Count of clients with "Prospect" status
- **Dead Clients**: Count of clients with "Dead" status
- **Revenue by Service Type**: Breakdown showing revenue per service type

### Access:
- Navigate to `/dashboard` or click "Dashboard" in navigation
- Root URL (`/`) now redirects to dashboard

---

## 6. Exporting & Filtering

### Export Features:
- **CSV Export**: Export filtered client list
- Includes: Name, Entity Type, Fiscal Year End, Status, Next Follow-Up Date, Annual Revenue, Created At
- Preserves all active filters when exporting

### Filtering:
- All filters work together (AND logic)
- Filters persist in URL for bookmarking/sharing
- Clear button resets all filters

---

## 7. Branding Updates

### Changes:
- Application title: "Tierney & Ohlms CRM"
- Updated in:
  - Page titles
  - Navigation bar
  - All templates

---

## Usage Guide

### Adding a Prospect with Follow-Up:
1. Click "+ New Client"
2. Set Status to "Prospect"
3. Set "Next Follow-Up Date"
4. Save

### Quick Status Update:
1. Go to Clients list
2. Click the Status dropdown for any client
3. Select new status
4. Change saves automatically

### Viewing Prospects Needing Follow-Up:
1. Go to Clients list
2. In "Follow-Up" filter, select "Needed" or "Overdue"
3. Click "Apply Filters"

### Exporting Client List:
1. Apply any filters you want
2. Click "Export CSV"
3. File downloads with current filter settings

### Viewing Dashboard:
1. Click "Dashboard" in navigation
2. View all key metrics at a glance

---

## Technical Notes

### Database Migration:
- Migration script handles schema changes safely
- Existing data is preserved
- Run once after updating code

### Revenue Calculation:
- Only includes **active** services
- Monthly services: `monthly_fee × 12`
- Quarterly services: `monthly_fee × 4`
- Annual services: `monthly_fee × 1`
- Services without frequency default to monthly

### Inline Editing:
- Uses AJAX to save changes
- No page refresh required
- Visual feedback on save (green flash)

### Email Service:
- Abstraction allows easy provider swapping
- Defaults to console output if SMTP not configured
- No breaking changes to existing code

---

## Files Changed

### Models & Database:
- `models.py` - Updated Client model
- `migrate_database.py` - New migration script
- `schemas.py` - Updated schemas

### Business Logic:
- `crud.py` - Added revenue calculation, enhanced filtering
- `main.py` - New routes (dashboard, export, inline updates)

### Templates:
- `templates/base.html` - Updated branding, added dashboard link
- `templates/clients_list.html` - Complete rewrite with new features
- `templates/client_form.html` - Removed EIN, added follow-up date
- `templates/client_detail.html` - Removed EIN reference
- `templates/dashboard.html` - New dashboard page

### New Files:
- `email_service.py` - Email abstraction
- `daily_reminders.py` - Daily reminder job
- `CHANGES.md` - This file

---

## Next Steps (Future Enhancements)

- Client-facing email automation
- Advanced reporting
- Task automation
- Integration with accounting software
- Mobile-responsive improvements

---

## Support

For questions or issues, contact the development team.

