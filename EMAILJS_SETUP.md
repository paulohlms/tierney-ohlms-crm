# EmailJS Setup Guide for Follow-Up Reminders

This guide will help you set up EmailJS to enable automated follow-up email reminders for Prospect deals in your CRM.

## Step 1: Sign Up for EmailJS (Free)

1. Go to [https://www.emailjs.com](https://www.emailjs.com)
2. Click "Sign Up" and create a free account
3. Verify your email address

## Step 2: Create an Email Service

1. In the EmailJS dashboard, go to **Email Services**
2. Click **Add New Service**
3. Choose your email provider (Gmail, Outlook, etc.) or use "Custom SMTP"
4. Follow the setup instructions for your provider
5. **Note your Service ID** (you'll need this later)

## Step 3: Create an Email Template

1. Go to **Email Templates** in the EmailJS dashboard
2. Click **Create New Template**
3. Use the following template:

**Template Name:** Follow-Up Reminder

**Subject:**
```
Follow-Up Reminder: {{deal_name}} with {{company}}
```

**Content:**
```
Hi {{owner_name}},

This is a reminder to follow up on the prospect deal '{{deal_name}}' with {{company}} (estimated {{estimated_value}}).

Notes: {{notes}}
Expected close: {{expected_close_date}}

Follow-up date was {{follow_up_date}}.

— Your Pipeline CRM
```

4. **Note your Template ID** (you'll need this later)

## Step 4: Get Your Public Key

1. Go to **Account** → **General** in the EmailJS dashboard
2. Find your **Public Key** (also called User ID)
3. Copy this key

## Step 5: Update the Dashboard Code

1. Open `templates/dashboard.html`
2. Find this line near the top:
   ```javascript
   emailjs.init('YOUR_PUBLIC_KEY_HERE');
   ```
3. Replace `YOUR_PUBLIC_KEY_HERE` with your actual Public Key from Step 4

4. Find these lines in the JavaScript section:
   ```javascript
   const EMAILJS_SERVICE_ID = 'YOUR_SERVICE_ID_HERE';
   const EMAILJS_TEMPLATE_ID = 'YOUR_TEMPLATE_ID_HERE';
   ```

5. Replace `YOUR_SERVICE_ID_HERE` with your Service ID from Step 2
6. Replace `YOUR_TEMPLATE_ID_HERE` with your Template ID from Step 3

## Step 6: Test the Setup

1. Create a test Prospect deal:
   - Set **Owner Name** to your name
   - Set **Owner Email** to your email address
   - Set **Next Follow-Up Date** to today's date
   - Save the deal

2. Go to the Dashboard page
3. Click the **"Check & Send Due Reminders"** button
4. Check your email - you should receive the reminder!

## How It Works

- **Automatic Checking**: When you open the Dashboard, it automatically checks for due follow-ups and shows a banner if any are found
- **Manual Trigger**: Click "Check & Send Due Reminders" to manually check and send reminders
- **Spam Prevention**: Reminders are only sent once per day per deal (tracked by `last_reminder_sent` field)
- **Due Dates**: Reminders are sent for deals where the Next Follow-Up Date is today or in the past
- **Visual Indicators**: Overdue follow-ups are highlighted in red in the Prospects table

## Troubleshooting

### Emails Not Sending

1. **Check Browser Console**: Open Developer Tools (F12) and look for error messages
2. **Verify Keys**: Make sure all three values (Public Key, Service ID, Template ID) are correct
3. **Check EmailJS Dashboard**: Look for errors in the EmailJS dashboard under "Logs"
4. **Test Email Service**: Make sure your email service is properly configured in EmailJS

### Template Variables Not Working

- Make sure your template uses the exact variable names:
  - `{{deal_name}}`
  - `{{company}}`
  - `{{estimated_value}}`
  - `{{notes}}`
  - `{{owner_name}}`
  - `{{follow_up_date}}`
  - `{{expected_close_date}}`

### Reminders Sending Multiple Times

- The system tracks `last_reminder_sent` to prevent duplicate emails
- If you see multiple sends, check that the database update is working correctly

## Free Tier Limits

EmailJS free tier includes:
- 200 emails per month
- Basic email templates
- Standard support

For higher volumes, consider upgrading to a paid plan.

## Security Note

The Public Key, Service ID, and Template ID are safe to include in client-side code. They are designed to be public. However, your email service credentials are stored securely in EmailJS and never exposed.

