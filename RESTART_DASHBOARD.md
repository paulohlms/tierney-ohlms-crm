# Step-by-Step: Restarting to See New Dashboard

## Quick Overview

You need to:
1. Stop the server (if running)
2. Start the server again
3. Open the dashboard in your browser

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

## Step 4: Start the Server

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

## Step 5: Open in Your Browser

1. Open your web browser (Chrome, Edge, Firefox, etc.)
2. In the address bar, type: `http://localhost:8000`
3. Press Enter

---

## Step 6: Log In

- **Email:** `admin@firm.com`
- **Password:** `admin123`

---

## Step 7: View the New Dashboard

1. Click **"Dashboard"** in the top navigation bar
2. You should now see the **Sales Pipeline Dashboard** with:

   **Prospects Pipeline (Blue Section):**
   - Total estimated revenue
   - Number of prospects
   - Table of all prospect deals

   **Closed/Won in 2025 (Green Section):**
   - Total actual revenue
   - Number of won deals
   - Table of all won deals

   **Lost Deals Tracker (Red Section):**
   - Total estimated value lost
   - Number of lost deals
   - Table of all lost deals

---

## What Changed?

The dashboard now shows:
- ✅ **Prospects** - All clients with "Prospect" status
- ✅ **Won Deals** - All clients with "Active" status (treated as closed/won)
- ✅ **Lost Deals** - All clients with "Dead" status

All data comes from your actual CRM database!

---

## Troubleshooting

### Server won't start:
- Make sure you're in the right folder (Step 3)
- Check that Python is installed correctly

### Can't see the new dashboard:
- Make sure you clicked "Dashboard" (not "Clients")
- Try refreshing your browser (F5)
- Make sure the server is running (Step 4)

### Dashboard shows "No prospects found":
- This is normal if you don't have any clients with "Prospect" status yet
- Go to Clients → New Client → Set status to "Prospect"
- Then refresh the dashboard

---

## Quick Reference

**To start the server:**
```
cd "C:\Users\PaulOhlms\Desktop\CRM Tool"
python -m uvicorn main:app --reload
```

**To stop the server:**
- Press Ctrl + C in the PowerShell window

**Dashboard URL:**
- http://localhost:8000/dashboard

---

That's it! The new sales pipeline dashboard is now active.

