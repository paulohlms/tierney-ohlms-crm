# Follow-Up Email Reminders - Implementation Summary

## What Was Added

### 1. New Database Fields
- **owner_name** (String): Name of the person responsible for the deal
- **owner_email** (String): Email address for follow-up reminders
- **last_reminder_sent** (Date): Tracks when the last reminder was sent (prevents spam)

### 2. Updated Forms
- Client creation/edit forms now include:
  - Owner Name field
  - Owner Email field
  - Next Follow-Up Date field (with validation - cannot be in the past)
  - These fields are **required** when Status is set to "Prospect"

### 3. Dashboard Enhancements
- **New Columns**: Prospects table now shows:
  - Owner Name
  - Next Follow-Up Date (with visual indicators for overdue/due today)
- **Reminder Banner**: Shows at top of page when follow-ups are due
- **Check & Send Button**: Manual trigger to check and send reminders
- **EmailJS Integration**: Client-side email sending using EmailJS service

### 4. Automated Reminder Logic
- Checks for prospects where Next Follow-Up Date <= today
- Only sends if reminder hasn't been sent today (prevents spam)
- Sends email to Owner Email address
- Updates `last_reminder_sent` field after successful send
- Shows toast notifications for success/errors

## Setup Steps

### Step 1: Run Database Migration
```bash
python migrate_add_owner_fields.py
```

This adds the new columns to your existing database.

### Step 2: Set Up EmailJS
Follow the detailed instructions in `EMAILJS_SETUP.md` to:
1. Create an EmailJS account
2. Set up an email service
3. Create an email template
4. Get your Public Key, Service ID, and Template ID

### Step 3: Configure EmailJS in Dashboard
1. Open `templates/dashboard.html`
2. Find and replace these placeholders:
   - `YOUR_PUBLIC_KEY_HERE` → Your EmailJS Public Key
   - `YOUR_SERVICE_ID_HERE` → Your EmailJS Service ID
   - `YOUR_TEMPLATE_ID_HERE` → Your EmailJS Template ID

### Step 4: Test the System
1. Create a test Prospect deal:
   - Set Owner Name to your name
   - Set Owner Email to your email
   - Set Next Follow-Up Date to today
2. Go to Dashboard
3. Click "Check & Send Due Reminders"
4. Check your email!

## How It Works

### Automatic Checking
- When you open the Dashboard, it automatically checks for due follow-ups
- If any are found, a red banner appears at the top showing the count
- Overdue follow-ups are highlighted in red in the table

### Manual Trigger
- Click "Check & Send Due Reminders" button anytime
- System checks all Prospect deals
- Sends emails for due/overdue deals that haven't been reminded today
- Shows success/error notifications

### Spam Prevention
- Each deal can only receive one reminder per day
- Tracked by `last_reminder_sent` field
- System automatically updates this field after successful send

### Email Content
The email includes:
- Deal name and company
- Estimated value
- Notes (first 200 characters)
- Owner name
- Follow-up date
- Expected close date

## Visual Indicators

- **Red text with (OVERDUE)**: Follow-up date is in the past
- **Blue text with (DUE TODAY)**: Follow-up date is today
- **Red banner**: Shows count of due follow-ups at top of page

## Testing Checklist

- [ ] Run database migration
- [ ] Set up EmailJS account and get credentials
- [ ] Update dashboard.html with EmailJS credentials
- [ ] Create a test Prospect with follow-up date = today
- [ ] Click "Check & Send Due Reminders"
- [ ] Verify email received
- [ ] Check that `last_reminder_sent` was updated
- [ ] Try clicking again - should not send duplicate
- [ ] Create Prospect with overdue date - should show as overdue
- [ ] Test with multiple prospects due on same day

## Troubleshooting

### Emails Not Sending
1. Check browser console (F12) for errors
2. Verify EmailJS credentials are correct
3. Check EmailJS dashboard for service errors
4. Ensure email service is properly configured

### Reminders Sending Multiple Times
- Check that `last_reminder_sent` field is being updated
- Verify database connection is working
- Check browser console for API errors

### Template Variables Not Working
- Ensure template uses exact variable names from `EMAILJS_SETUP.md`
- Check EmailJS template editor for typos

## Notes

- **Client-Side Only**: Emails only send when the page is open and button is clicked
- **No Background Jobs**: This is a browser limitation - reminders require manual page visit
- **Free Tier**: EmailJS free tier includes 200 emails/month
- **Security**: Public Key, Service ID, and Template ID are safe to include in client-side code

## Files Modified

- `models.py` - Added owner_name, owner_email, last_reminder_sent fields
- `schemas.py` - Updated schemas to include new fields
- `main.py` - Updated routes to handle new fields
- `templates/client_form.html` - Added owner fields with validation
- `templates/dashboard.html` - Added EmailJS integration and reminder logic
- `seed.py` - Updated with realistic owner data
- `migrate_add_owner_fields.py` - New migration script

## Files Created

- `EMAILJS_SETUP.md` - Detailed EmailJS setup instructions
- `FOLLOW_UP_REMINDERS_GUIDE.md` - This file

