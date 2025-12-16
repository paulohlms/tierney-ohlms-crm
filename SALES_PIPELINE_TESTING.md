# Sales Pipeline Dashboard - Testing Instructions

## Quick Start

1. **Open the file:**
   - Double-click `sales_pipeline_dashboard.html`
   - Or open it in your web browser

2. **Verify it loads:**
   - You should see the dashboard with 3 sections (Prospects, Won, Lost)
   - Charts should display at the top
   - Pipeline funnel should show numbers

---

## Testing Data Persistence

### Test 1: Add a Deal
1. Click **"+ Add Deal"** button
2. Fill in the form:
   - Deal Name: "Test Deal"
   - Company: "Test Company"
   - Status: "Prospect"
   - Estimated Value: 50000
   - Expected Close Date: 2025-12-31
   - Notes: "Test notes"
3. Click **"Save Deal"**
4. Verify the deal appears in the Prospects table
5. **Refresh the page** (F5)
6. **Verify the deal is still there** (data persisted!)

### Test 2: Edit a Deal
1. Find any deal in the table
2. Click **"Edit"** button
3. Change the deal name to "Updated Deal"
4. Click **"Save Deal"**
5. Verify the change appears immediately
6. **Refresh the page**
7. **Verify the change persisted**

### Test 3: Delete a Deal
1. Find any deal
2. Click **"Delete"** button
3. Confirm the deletion
4. Verify the deal disappears
5. **Refresh the page**
6. **Verify the deal is still gone**

### Test 4: Reset Data
1. Click **"Reset Data"** button
2. Confirm the reset
3. Verify all data returns to defaults
4. Your custom deals should be gone
5. Default 15 deals should appear

---

## Testing Search & Filters

### Test 5: Global Search
1. Type "Acme" in the search box
2. Verify only deals with "Acme" appear
3. Clear the search
4. All deals should reappear

### Test 6: Status Filter
1. Select "Won" from the status dropdown
2. Verify only won deals show
3. Select "All Status"
4. All deals should reappear

### Test 7: Date Range Filter
1. Set "From" date to: 2025-10-01
2. Set "To" date to: 2025-12-31
3. Verify only deals with dates in that range appear
4. Clear the dates
5. All deals should reappear

---

## Testing Table Sorting

### Test 8: Sort by Column
1. Click any column header (e.g., "Estimated Value")
2. Verify the table sorts ascending
3. Click again
4. Verify it sorts descending
5. Try different columns

---

## Testing Charts

### Test 9: Charts Update
1. Add a new "Won" deal with a close date
2. Verify the monthly revenue chart updates
3. Verify the status distribution pie chart updates
4. Delete the deal
5. Charts should update again

---

## Testing Dark Mode

### Test 10: Toggle Dark Mode
1. Click the **"🌙 Dark"** button
2. Verify the page switches to dark theme
3. Click **"☀️ Light"** button
4. Verify it switches back
5. **Refresh the page**
6. **Verify your preference persisted**

---

## Testing Export

### Test 11: Export Data
1. Click **"Export JSON"** button
2. A file should download
3. Open the file in a text editor
4. Verify it contains all your deals in JSON format

---

## Testing Responsive Design

### Test 12: Mobile View
1. Open browser developer tools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Select a mobile device
4. Verify:
   - Layout stacks vertically
   - Tables are scrollable
   - Buttons are accessible
   - Charts resize properly

---

## Testing Form Validation

### Test 13: Required Fields
1. Click **"+ Add Deal"**
2. Try to submit without filling required fields
3. Browser should prevent submission
4. Fill in required fields
5. Submit should work

### Test 14: Number Validation
1. In the value field, try entering negative number
2. Try entering text
3. Browser should validate (numbers only, positive)

---

## Testing Section Collapse

### Test 15: Collapse Sections
1. Click **"Collapse"** on any section
2. Section should hide
3. Click **"▶"** to expand
4. Section should show again

---

## Expected Behavior Summary

✅ **Data Persistence:**
- All changes save automatically
- Data persists after page refresh
- Reset button restores defaults

✅ **CRUD Operations:**
- Add deals works
- Edit deals works
- Delete deals works (with confirmation)
- Forms validate input

✅ **Search & Filters:**
- Global search filters across all fields
- Status filter works
- Date range filter works
- Filters combine correctly

✅ **Interactivity:**
- Tables sort by clicking headers
- Charts update automatically
- Funnel updates automatically
- Dark mode toggles and persists

✅ **Visual:**
- Responsive on mobile
- Animations work smoothly
- Colors match status (blue/green/red)
- Professional appearance

---

## Troubleshooting

### Data not persisting?
- Check browser console for errors (F12)
- Make sure localStorage is enabled
- Try in a different browser

### Charts not showing?
- Check browser console for errors
- Make sure you have internet (Chart.js CDN)
- Verify deals have dates for monthly chart

### Search not working?
- Make sure you're typing in the search box
- Check that deals match your search term
- Try clearing filters

### Modal not opening?
- Check browser console for errors
- Make sure JavaScript is enabled
- Try refreshing the page

---

## Future Extension Ideas

1. **Import JSON:**
   - Add "Import JSON" button
   - Allow uploading exported files
   - Merge or replace data

2. **Advanced Filters:**
   - Filter by value range
   - Filter by company
   - Save filter presets

3. **Deal Stages:**
   - Add more status options
   - Track deal progression
   - Add probability percentages

4. **Notes History:**
   - Track note changes over time
   - Add timestamps to notes
   - Activity log

5. **Email Integration:**
   - Send deal summaries via email
   - Export to CSV for email
   - Email reminders for follow-ups

6. **Team Collaboration:**
   - Add user assignments to deals
   - Track who added/edited deals
   - Comments/activity feed

7. **Reporting:**
   - Generate PDF reports
   - Weekly/monthly summaries
   - Win rate analysis

8. **Integration:**
   - Connect to Google Sheets
   - Sync with CRM systems
   - API for data access

---

## Notes

- All data is stored in browser localStorage
- No backend/server required
- Works completely offline (except Chart.js CDN)
- Data is specific to each browser/computer
- Export JSON to backup your data regularly

