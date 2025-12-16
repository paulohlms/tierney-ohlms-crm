# 2025 Sales Pipeline Dashboard

A standalone, client-side sales pipeline dashboard for tracking prospects, won deals, and lost deals in 2025.

## Features

- **Prospects Pipeline**: Track active prospects with estimated revenue and expected close dates
- **Closed/Won Deals**: View all deals won in 2025 with actual revenue
- **Lost Deals Tracker**: Monitor lost opportunities with reasons
- **Interactive Tables**: Click column headers to sort data
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Real-time Calculations**: Summary cards automatically calculate from data

## How to Run Locally

### Option 1: Direct File Open
1. Simply double-click `sales_pipeline_dashboard.html`
2. It will open in your default web browser
3. No server or installation required!

### Option 2: Using a Local Server (Recommended)
If you want to test with a local server:

**Python:**
```bash
# Python 3
python -m http.server 8000

# Then open: http://localhost:8000/sales_pipeline_dashboard.html
```

**Node.js:**
```bash
npx http-server

# Then open the URL shown (usually http://localhost:8080)
```

**VS Code:**
- Install "Live Server" extension
- Right-click `sales_pipeline_dashboard.html`
- Select "Open with Live Server"

## Data Structure

All data is hardcoded in JavaScript within the HTML file. To modify:

1. Open `sales_pipeline_dashboard.html` in a text editor
2. Find the `salesData` array in the `<script>` section
3. Add, modify, or remove deal objects
4. Save and refresh your browser

### Deal Object Structure

**Prospect:**
```javascript
{
    id: 1,
    dealName: "Deal Name",
    company: "Company Name",
    status: "Prospect",
    estimatedValue: 150000,
    expectedCloseDate: "2025-12-31",
    notes: "Any notes here"
}
```

**Won:**
```javascript
{
    id: 7,
    dealName: "Deal Name",
    company: "Company Name",
    status: "Won",
    actualRevenue: 85000,
    closeDate: "2025-10-15",
    estimatedValue: 85000
}
```

**Lost:**
```javascript
{
    id: 12,
    dealName: "Deal Name",
    company: "Company Name",
    status: "Lost",
    estimatedValue: 45000,
    lostDate: "2025-11-20",
    reason: "Chose competitor"
}
```

## Customization

### Colors
The design uses a black and white theme matching Tierney & Ohlms branding:
- **Prospects**: Blue theme (#2563eb)
- **Won**: Green theme (#16a34a)
- **Lost**: Red theme (#dc2626)

To change colors, edit the CSS variables in the `<style>` section.

### Adding More Data
Simply add more objects to the `salesData` array. The dashboard will automatically:
- Calculate new totals
- Display new deals in tables
- Update summary cards

## Browser Compatibility

Works in all modern browsers:
- Chrome/Edge (recommended)
- Firefox
- Safari
- Opera

## Notes

- All dates should be in 2025 (as specified)
- Currency is formatted as USD
- Tables are sortable by clicking column headers
- Design is responsive and mobile-friendly
- No backend required - completely static HTML/CSS/JS

## Support

This is a standalone dashboard. All functionality is client-side only.

