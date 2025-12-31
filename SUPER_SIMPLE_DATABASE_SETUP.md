# Super Simple Database Setup - For Non-Coders

**Hi! This guide is written for people who aren't programmers. Every step is explained in plain English.**

---

## What We're Doing (In Simple Terms)

Right now, when you add data to your website, it disappears when the server restarts. We're going to:
1. Create a permanent storage place (like a filing cabinet)
2. Connect your website to that storage
3. Set up automatic backups (like making copies every hour)

**Time needed: About 15 minutes**

---

## PART 1: Create the Storage (Like a Filing Cabinet)

### Step 1: Go to Your Render Account

1. Open your web browser (Chrome, Firefox, etc.)
2. Go to: **https://dashboard.render.com**
3. Log in with your email and password
4. You should see your website listed

### Step 2: Create a New Database

1. Look at the **top right corner** of the page
2. You'll see a button that says **"New +"** (it's usually blue or green)
3. **Click** on "New +"
4. A menu will appear with options
5. **Click** on **"PostgreSQL"** (it's in the list)

### Step 3: Fill Out the Form

A form will appear. Fill it out like this:

**Name:**
- Type: `tierney-ohlms-crm-db`
- (This is just a name for your storage - you can use any name you want)

**Database:**
- Leave this as the default (usually `crm_db` or similar)
- Don't change this

**User:**
- Leave this as the default (usually `crm_user` or similar)
- Don't change this

**Region:**
- Click the dropdown
- Choose the one closest to you:
  - If you're in the US: Choose **"Oregon (US West)"**
  - If you're in Europe: Choose **"Frankfurt (EU Central)"**
  - If you're not sure: Choose **"Oregon (US West)"**

**PostgreSQL Version:**
- Leave this as the default (usually 16)
- Don't change this

**Plan:**
- You'll see two options:
  - **Free** = Free but turns off after 90 days of no use
  - **Starter ($7/month)** = Always on, never turns off
- **Recommendation:** Choose **"Starter ($7/month)"** if you want it to always work
- Choose **"Free"** if you're just testing

### Step 4: Create It

1. Scroll down to the bottom of the form
2. Click the **"Create Database"** button (usually green or blue)
3. Wait 2-3 minutes
4. You'll see a message saying it's being created
5. When it's done, you'll see your new database in the list

**✅ Good! You've created your storage. Now let's connect your website to it.**

---

## PART 2: Connect Your Website to the Storage

### Step 5: Find Your Connection String (Like an Address)

1. **Click** on the database you just created (it should be in your list)
2. You'll see a page with information about your database
3. Scroll down until you see a section called **"Connections"** or **"Connection Information"**
4. You'll see something that looks like this:
   ```
   postgresql://crm_user:password123@dpg-xxxxx-a.oregon-postgres.render.com/crm_db
   ```
5. Look for **"Internal Database URL"** (it might say "Internal" or "Internal Database URL")
6. **Click the copy button** next to it (it looks like two squares overlapping, or says "Copy")
7. **Save this somewhere** - open Notepad or a text file and paste it there
8. **Label it:** "Internal Database URL"

**✅ Good! You've copied the address. Now let's tell your website where to find the storage.**

### Step 6: Add the Address to Your Website

1. Go back to your Render dashboard (click "Dashboard" or the Render logo)
2. **Find your website** in the list (it's probably called something like "tierney-ohlms-crm" or similar)
3. **Click** on your website
4. You'll see several tabs at the top: "Overview", "Logs", "Environment", etc.
5. **Click** on the **"Environment"** tab

### Step 7: Add the Environment Variable

1. You'll see a list of environment variables (or it might be empty)
2. Look for a button that says **"Add Environment Variable"** or **"Add"** (usually at the top)
3. **Click** that button
4. A form will appear with two boxes:
   - **Key** (left box)
   - **Value** (right box)

5. In the **Key** box, type exactly this (copy and paste):
   ```
   DATABASE_URL
   ```
   (Make sure it's all capital letters, with an underscore between DATABASE and URL)

6. In the **Value** box, **paste** the connection string you copied in Step 5
   (The one that starts with `postgresql://`)

7. **Click** the **"Save Changes"** button (usually at the bottom)

### Step 8: Wait for Your Website to Update

1. After you save, Render will automatically start updating your website
2. You'll see a message like "Deploying..." or "Building..."
3. **Wait 3-5 minutes** - don't close the page
4. You'll see it change to "Live" when it's done

**✅ Good! Your website is now connected to the storage. Let's test it!**

---

## PART 3: Test That It Works

### Step 9: Test Your Website

1. Go to your website (the URL you use to access it)
2. **Log in** if you need to
3. **Create some test data:**
   - Try creating a new user
   - Or create a new client
   - Or add a timesheet entry
   - (Just add something simple to test)

4. **After you create it, refresh the page:**
   - Press **F5** on your keyboard, or
   - Click the refresh button in your browser

5. **Check:** Is the data you just created still there?
   - ✅ **YES** = It's working! Great job!
   - ❌ **NO** = Something went wrong (see troubleshooting below)

**✅ If it's working, you're almost done! Now let's set up backups.**

---

## PART 4: Set Up Automatic Backups (Every Hour)

### Step 10: Create a Backup Job

1. Go back to your Render dashboard
2. Click the **"New +"** button again (top right)
3. This time, click on **"Cron Job"** (it's in the menu)

### Step 11: Fill Out the Backup Form

A form will appear. Fill it out:

**Name:**
- Type: `crm-hourly-backup`
- (This is just a name - you can use any name)

**Schedule:**
- Type exactly this: `0 * * * *`
- (This means "run every hour at the top of the hour" - like 1:00 PM, 2:00 PM, etc.)

**Command:**
- Type exactly this: `python backup_database_python.py`
- (This tells it which backup script to run)

**Branch:**
- Click the dropdown
- Choose **"main"** (or "master" if that's what you see)

**Root Directory:**
- Leave this **empty** (don't type anything)

**Plan:**
- Choose **"Free"** (backups don't need the paid plan)

### Step 12: Add the Database Address to the Backup Job

1. Scroll down in the form
2. Look for **"Environment Variables"** section
3. Click **"Add Environment Variable"** button

4. In the **Key** box, type:
   ```
   DATABASE_URL
   ```
   (Same as before - all capitals, underscore)

5. Now go back to your **database page** (the one you created in Part 1)
6. Look for **"External Connection String"** (this time it says "External", not "Internal")
7. **Copy** that one (click the copy button)
8. Go back to the cron job form
9. **Paste** it in the **Value** box

10. Click **"Add"** or **"Save"** (to add this variable)

11. (Optional) Add another variable for security:
    - Click **"Add Environment Variable"** again
    - **Key**: `BACKUP_TOKEN`
    - **Value**: Type any random text, like `my-secret-token-12345`
    - Click **"Add"**

### Step 13: Create the Backup Job

1. Scroll to the bottom of the form
2. Click **"Create Cron Job"** button
3. Wait 1-2 minutes
4. You'll see your new backup job in the list

**✅ Good! Backups are now set up!**

---

## PART 5: Verify Everything Works

### Step 14: Check That Backups Are Running

1. **Wait for the next hour** (e.g., if it's 2:30 PM, wait until 3:00 PM)
2. Go to your Render dashboard
3. **Click** on your backup job (`crm-hourly-backup`)
4. Click the **"Logs"** tab
5. You should see messages like:
   - "Starting database backup..."
   - "✅ Backup created successfully"
   - "✅ Backup process completed successfully"

**If you see those messages, everything is working! 🎉**

---

## ✅ You're Done!

**What you've accomplished:**
- ✅ Created permanent storage for your data
- ✅ Connected your website to that storage
- ✅ Set up automatic backups every hour
- ✅ Your data will now save permanently and be backed up

**Your data is now:**
- Saved permanently (won't disappear)
- Backed up every hour automatically
- Protected from loss

---

## 🆘 Troubleshooting (If Something Goes Wrong)

### Problem: "I can't find the 'New +' button"

**Solution:**
- Make sure you're logged into Render
- Try refreshing the page (F5)
- Look in the top right corner of the page

### Problem: "I don't see 'PostgreSQL' in the menu"

**Solution:**
- Make sure you clicked "New +" first
- The menu should appear below it
- Look for "PostgreSQL" - it might be in a submenu

### Problem: "The form won't let me create the database"

**Solution:**
- Make sure you filled in the "Name" field
- Make sure you selected a "Region"
- Make sure you selected a "Plan"
- Try refreshing the page and starting over

### Problem: "I can't find the connection string"

**Solution:**
- Make sure you clicked on your database (not your website)
- Scroll down on the database page
- Look for a section called "Connections" or "Connection Information"
- It might be in a tab - look for tabs at the top

### Problem: "I added DATABASE_URL but data still doesn't save"

**Solution:**
1. Check that you spelled it exactly: `DATABASE_URL` (all capitals, underscore)
2. Check that you pasted the full connection string (starts with `postgresql://`)
3. Make sure you clicked "Save Changes"
4. Wait 5 minutes for the website to update
5. Try creating test data again

### Problem: "The backup job isn't running"

**Solution:**
1. Check that the schedule is exactly: `0 * * * *`
2. Check that the command is exactly: `python backup_database_python.py`
3. Make sure you added the `DATABASE_URL` environment variable
4. Make sure you used the **External** connection string (not Internal)
5. Check the logs tab for error messages

### Problem: "I'm confused about Internal vs External connection strings"

**Simple explanation:**
- **Internal** = Use this for your website (only works from Render)
- **External** = Use this for backups (works from anywhere)
- **Rule:** Website = Internal, Backups = External

---

## 📞 Still Need Help?

If you're stuck:
1. Take a screenshot of what you're seeing
2. Note which step you're on
3. Describe what's happening (or not happening)
4. Ask for help with that specific step

**Remember:** There's no such thing as a stupid question. If something doesn't make sense, ask!

---

## 🎉 Congratulations!

You've successfully set up a database and backups - that's a big accomplishment! Your data is now safe and will be backed up automatically every hour.

