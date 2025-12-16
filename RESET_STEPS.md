# Step-by-Step: Applying CRM Updates

## Quick Overview

You need to:
1. Stop the server (if running)
2. Run the database migration
3. Restart the server
4. Test the new features

---

## Step 1: Stop the Server

**If your server is currently running:**

1. Go to the PowerShell window where you see "Uvicorn running"
2. Click in that window
3. Press **Ctrl + C**
4. If it asks "Terminate batch job?", type **Y** and press Enter
5. The window should show a normal prompt again

**If the server is not running, skip to Step 2.**

---

## Step 2: Open PowerShell

1. Press the **Windows key**
2. Type: `powershell`
3. Press **Enter**

---

## Step 3: Go to Your CRM Folder

Type this and press Enter:

```
cd "C:\Users\PaulOhlms\Desktop\CRM Tool"
```

You should see:
```
PS C:\Users\PaulOhlms\Desktop\CRM Tool>
```

---

## Step 4: Run the Database Migration

This updates your database to work with the new features.

Type this and press Enter:

```
python migrate_database.py
```

**What you should see:**
```
Starting database migration...
==================================================
✓ Removed ein_last4 column
✓ Added next_follow_up_date column

✓ Database migration completed successfully!
```

**If you see errors:**
- Make sure you're in the right folder (Step 3)
- Make sure Python is installed correctly

---

## Step 5: Start the Server

Type this and press Enter:

```
python -m uvicorn main:app --reload
```

**What you should see:**
```
INFO:     Will watch for changes in these directories: ['C:\\Users\\PaulOhlms\\Desktop\\CRM Tool']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Application startup complete.
```

**KEEP THIS WINDOW OPEN!** Don't close it.

---

## Step 6: Open in Your Browser

1. Open your web browser (Chrome, Edge, Firefox, etc.)
2. In the address bar, type: `http://localhost:8000`
3. Press Enter

---

## Step 7: Log In

- **Email:** `admin@firm.com`
- **Password:** `admin123`

---

## Step 8: Test the New Features

### Check the Dashboard:
1. Click **"Dashboard"** in the top navigation
2. You should see:
   - Monthly Recurring Revenue
   - Annualized Revenue
   - Client counts
   - Revenue by service type

### Check the Clients List:
1. Click **"Clients"** in the top navigation
2. You should see:
   - **Revenue column** showing dollar amounts
   - **Inline dropdowns** for Entity Type and Status
   - **Filter section** at the top
   - **Export CSV button**

### Try Inline Editing:
1. Find a client in the list
2. Click the **Status dropdown** for that client
3. Change the status
4. It should save automatically (you'll see a brief green flash)

### Try Filtering:
1. In the filter section, select a **Status** (like "Active")
2. Click **"Apply Filters"**
3. The list should update to show only that status

### Try Export:
1. Apply some filters (optional)
2. Click **"Export CSV"**
3. A file should download with your client data

---

## Troubleshooting

### "Database migration completed" but I see errors:
- The migration worked, but there might be some warnings
- As long as you see "✓ Database migration completed successfully!", you're good

### Server won't start:
- Make sure you ran the migration first (Step 4)
- Check that you're in the right folder
- Try closing and reopening PowerShell

### Can't see new features:
- Make sure you restarted the server (Step 5)
- Try refreshing your browser (F5)
- Make sure you're logged in

### Inline editing doesn't work:
- Make sure JavaScript is enabled in your browser
- Try refreshing the page

---

## What Changed?

- ✅ Removed EIN field (no longer shown)
- ✅ Added "Dead" status option
- ✅ Added "Unknown" entity type
- ✅ Added Next Follow-Up Date field
- ✅ Added Revenue column (calculated automatically)
- ✅ Added inline editing (edit directly in the table)
- ✅ Added sorting (click column headers)
- ✅ Added filtering (Status, Entity Type, Follow-Up)
- ✅ Added CSV export
- ✅ Added Dashboard page
- ✅ Updated branding to "Tierney & Ohlms CRM"

---

## Need Help?

If something doesn't work:
1. Check that the server is running (Step 5)
2. Make sure you ran the migration (Step 4)
3. Try refreshing your browser
4. Check the PowerShell window for error messages

---

## Quick Reference

**To start the server later:**
```
cd "C:\Users\PaulOhlms\Desktop\CRM Tool"
python -m uvicorn main:app --reload
```

**To stop the server:**
- Press Ctrl + C in the PowerShell window

**To run migration again (if needed):**
```
python migrate_database.py
```

