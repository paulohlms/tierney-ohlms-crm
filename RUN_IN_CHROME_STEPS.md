# Run Whiskey Inventory in Chrome - Step by Step

Follow these steps exactly to get your inventory system running in Chrome.

---

## Step 1: Check if Node.js is Installed (2 minutes)

1. **Open PowerShell:**
   - Press `Windows Key + X`
   - Click "Windows PowerShell" or "Terminal"

2. **Type this and press Enter:**
   ```
   node --version
   ```

3. **What you should see:**
   - ✅ **If you see a version number** (like `v20.10.0`): Skip to Step 2
   - ❌ **If you see an error**: Install Node.js first (see below)

### Install Node.js (if needed):
1. Go to: https://nodejs.org/
2. Click the big green "Download Node.js" button
3. Run the downloaded file
4. Click "Next" on everything (use defaults)
5. Make sure "Add to PATH" is checked
6. Click "Install"
7. Wait for it to finish
8. **Close and reopen PowerShell**, then try `node --version` again

---

## Step 2: Set Up Supabase (10 minutes)

### 2.1 Create Account
1. **Go to:** https://supabase.com
2. Click **"Start your project"** (top right)
3. **Sign up** with GitHub or Email
4. **Verify your email** if needed

### 2.2 Create Project
1. Click **"New Project"** (green button)
2. Fill in:
   - **Name:** `Whiskey Inventory`
   - **Database Password:** Create a password (**WRITE IT DOWN!**)
   - **Region:** Choose closest to you
   - **Pricing:** Select **"Free"**
3. Click **"Create new project"**
4. **Wait 2-3 minutes** (don't close the page!)

### 2.3 Get Your Credentials
Once your project is ready:

1. Click **"Settings"** (gear icon, left sidebar)
2. Click **"API"**
3. **Copy these two things:**
   - **Project URL** (looks like `https://xxxxx.supabase.co`)
   - **anon public key** (long string starting with `eyJ...`)

4. **Get database connection string:**
   - Click **"Database"** (still in Settings)
   - Scroll to **"Connection string"**
   - Click **"URI"** tab
   - You'll see: `postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres`
   - **Replace `[YOUR-PASSWORD]`** with the password you created
   - **Copy the entire string**

**Save all three in a text file!**

### 2.4 Create Your Login User
1. Click **"Authentication"** (left sidebar)
2. Click **"Users"**
3. Click **"Add user"** → **"Create new user"**
4. Enter:
   - **Email:** Your email (e.g., `you@company.com`)
   - **Password:** Create a password (**WRITE IT DOWN!**)
5. Click **"Create user"**

---

## Step 3: Open Your Project Folder (1 minute)

1. **Open File Explorer**
2. **Go to:** `C:\Users\PaulOhlms\Desktop\CRM Tool`
3. **Click in the address bar** (at the top)
4. **Type:** `powershell`
5. **Press Enter**
6. **PowerShell opens in that folder!**

---

## Step 4: Install Dependencies (3 minutes)

1. **In PowerShell** (you should be in the CRM Tool folder), type:
   ```
   npm install
   ```
2. **Press Enter**
3. **Wait 2-5 minutes** (you'll see lots of text scrolling)
4. **When done**, you'll see your command prompt again

**If you see errors:**
- Make sure you're in the right folder
- Make sure Node.js is installed (Step 1)
- Try running `npm install` again

---

## Step 5: Create Environment File (2 minutes)

1. **In your CRM Tool folder**, create a new file named `.env.local`
   - **Right-click** in the folder → **New** → **Text Document**
   - **Name it:** `.env.local` (must start with a dot!)
   - If Windows asks about changing the extension, click **"Yes"**

2. **Right-click `.env.local`** → **Open with** → **Notepad**

3. **Copy and paste this:**
   ```
   NEXT_PUBLIC_SUPABASE_URL=your_project_url_here
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key_here
   DATABASE_URL=your_database_connection_string_here
   ```

4. **Replace the placeholders:**
   - Replace `your_project_url_here` with your Project URL from Step 2.3
   - Replace `your_anon_key_here` with your anon key from Step 2.3
   - Replace `your_database_connection_string_here` with your connection string from Step 2.3

**Example of what it should look like:**
```
NEXT_PUBLIC_SUPABASE_URL=https://abcdefghijklmnop.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTYxNjIzOTAyMiwiZXhwIjoxOTMxODE1MDIyfQ.abcdefghijklmnopqrstuvwxyz
DATABASE_URL=postgresql://postgres:MyPassword123@db.abcdefghijklmnop.supabase.co:5432/postgres
```

5. **Save the file** (Ctrl+S)

---

## Step 6: Set Up Database (2 minutes)

1. **In PowerShell** (still in CRM Tool folder), type:
   ```
   npm run db:generate
   ```
2. **Press Enter** and wait (~30 seconds)

3. **Then type:**
   ```
   npm run db:push
   ```
4. **Press Enter** and wait
   - You should see: "Your database is now in sync" or similar

**If you see errors:**
- Check that `.env.local` has the correct values
- Make sure your Supabase project is active
- Verify your database password is correct

---

## Step 7: Start the Application (1 minute)

1. **In PowerShell** (still in CRM Tool folder), type:
   ```
   npm run dev
   ```
2. **Press Enter**
3. **You'll see:**
   ```
   ▲ Next.js 14.0.4
   - Local:        http://localhost:3000
   ```
4. **Keep this PowerShell window open!** Don't close it.

---

## Step 8: Open in Chrome (30 seconds)

1. **Open Google Chrome**
2. **In the address bar**, type:
   ```
   http://localhost:3000
   ```
3. **Press Enter**
4. **You should see the login page!**

---

## Step 9: Log In (30 seconds)

1. **Enter the email and password** you created in Step 2.4
2. **Click "Sign In"**
3. **You should see the dashboard!**

---

## ✅ You're Done!

Your Whiskey Inventory Management System is now running in Chrome!

**To use it:**
- Make sure PowerShell is running `npm run dev`
- Keep Chrome open at http://localhost:3000
- Use the app!

**To stop it:**
- Press `Ctrl + C` in the PowerShell window

**To start it again later:**
1. Open PowerShell in the CRM Tool folder
2. Type: `npm run dev`
3. Open Chrome: http://localhost:3000

---

## Troubleshooting

### "npm: command not found"
- Node.js isn't installed - go back to Step 1

### "Cannot connect to database"
- Check your `.env.local` file has correct values
- Make sure Supabase project is active
- Verify database password is correct

### "Port 3000 already in use"
- Close other applications using port 3000
- Or use: `npm run dev -- -p 3001`
- Then go to: http://localhost:3001

### "Authentication failed"
- Make sure you created a user in Supabase (Step 2.4)
- Check that your Supabase URL and keys are correct
- Try creating a new user in Supabase

### Page shows "Loading..." forever
- Check PowerShell for error messages
- Make sure `npm run dev` is still running
- Verify your `.env.local` file is correct
- Try refreshing the page (F5)

### Chrome shows "This site can't be reached"
- Make sure `npm run dev` is running in PowerShell
- Check that you typed `http://localhost:3000` correctly
- Try closing and reopening Chrome

---

## Quick Reference

**Start the app:**
```powershell
cd "C:\Users\PaulOhlms\Desktop\CRM Tool"
npm run dev
```

**Then open Chrome:** http://localhost:3000

**Stop the app:** Press `Ctrl + C` in PowerShell

---

**That's it! Follow these steps and you'll have it running in Chrome in about 20 minutes.** 🎉

