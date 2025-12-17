# Run Locally - Simple Setup Guide

This guide will get your Whiskey Inventory Management System running on your computer only (not online).

**Time needed:** 15-20 minutes

---

## Step 1: Install Node.js (5 minutes)

1. **Go to:** https://nodejs.org/
2. **Click the big green "Download Node.js" button**
3. **Run the downloaded file** (it will be in your Downloads folder)
4. **Follow the installation:**
   - Click "Next" on each screen
   - Make sure "Add to PATH" is checked (it usually is)
   - Click "Install"
   - Wait for it to finish
   - Click "Finish"

**Verify it worked:**
- Open **Command Prompt** (Windows: Press `Windows Key + R`, type `cmd`, press Enter)
- Type: `node --version`
- You should see a version number like `v20.10.0`
- If you see an error, try installing again

---

## Step 2: Set Up Supabase (10 minutes)

### 2.1 Create Supabase Account

1. **Go to:** https://supabase.com
2. **Click "Start your project"** (top right)
3. **Sign up** with GitHub or Email
4. **Verify your email** if needed

### 2.2 Create a Project

1. **Click "New Project"** (green button)
2. **Fill in:**
   - **Name:** `Whiskey Inventory` (or any name)
   - **Database Password:** Create a strong password (**WRITE IT DOWN!**)
   - **Region:** Choose closest to you
   - **Pricing Plan:** Select **"Free"**
3. **Click "Create new project"**
4. **Wait 2-3 minutes** for setup (don't close the page!)

### 2.3 Get Your Credentials

Once your project is ready:

1. **Click "Settings"** (gear icon, left sidebar)
2. **Click "API"** (under Project Settings)
3. **Copy these two values:**
   - **Project URL** (looks like `https://xxxxx.supabase.co`)
   - **anon public key** (long string starting with `eyJ...`)

4. **Get database connection string:**
   - Still in Settings, click **"Database"**
   - Scroll to **"Connection string"**
   - Click **"URI"** tab
   - You'll see: `postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres`
   - **Replace `[YOUR-PASSWORD]`** with the password you created
   - Copy the entire string

**Save all three values in a text file!**

### 2.4 Create Your First User

1. **Click "Authentication"** (left sidebar)
2. **Click "Users"**
3. **Click "Add user"** → **"Create new user"**
4. **Enter:**
   - **Email:** Your email (e.g., `you@company.com`)
   - **Password:** Create a password (**WRITE IT DOWN!**)
5. **Click "Create user"**

---

## Step 3: Set Up the Code (5 minutes)

### 3.1 Open Your Project Folder

1. **Navigate to your project folder** on your computer
2. **Right-click in the folder** → **"Open in Terminal"** or **"Open PowerShell here"**
   - If you don't see this option:
     - Open Command Prompt
     - Type: `cd "C:\Users\YourName\Desktop\CRM Tool"` (or your actual folder path)
     - Press Enter

### 3.2 Install Dependencies

1. **In the terminal**, type:
   ```
   npm install
   ```
2. **Press Enter**
3. **Wait 2-5 minutes** (you'll see lots of text scrolling)
4. When done, you'll see your command prompt again

**If you see errors:**
- Make sure you're in the correct folder
- Make sure Node.js is installed (Step 1)
- Try running `npm install` again

### 3.3 Create Environment File

1. **In your project folder**, create a new file named `.env.local`
   - **Windows:** Right-click → New → Text Document → Name it `.env.local`
   - **Important:** It must start with a dot (`.env.local` not `env.local`)

2. **Open `.env.local`** in Notepad or any text editor

3. **Copy and paste this**, then fill in your values:

```
NEXT_PUBLIC_SUPABASE_URL=your_project_url_here
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key_here
DATABASE_URL=your_database_connection_string_here
```

4. **Replace the placeholders** with your actual values from Step 2.3

**Example:**
```
NEXT_PUBLIC_SUPABASE_URL=https://abcdefghijklmnop.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
DATABASE_URL=postgresql://postgres:MyPassword123@db.abcdefghijklmnop.supabase.co:5432/postgres
```

5. **Save the file**

### 3.4 Set Up Database

1. **In your terminal** (still in project folder), type:
   ```
   npm run db:generate
   ```
2. **Press Enter** and wait (~30 seconds)

3. **Then type:**
   ```
   npm run db:push
   ```
4. **Press Enter** and wait
   - You should see "Your database is now in sync"

**If you see errors:**
- Check that `.env.local` has correct values
- Make sure your Supabase project is active
- Verify your database password is correct

---

## Step 4: Run the Application (1 minute)

### 4.1 Start the Server

1. **In your terminal** (still in project folder), type:
   ```
   npm run dev
   ```
2. **Press Enter**
3. **You'll see:**
   ```
   ▲ Next.js 14.0.4
   - Local:        http://localhost:3000
   ```
4. **Keep this terminal window open!** Don't close it while using the app.

### 4.2 Open in Browser

1. **Open your web browser** (Chrome, Firefox, Edge, etc.)
2. **Type in the address bar:**
   ```
   http://localhost:3000
   ```
3. **Press Enter**
4. **You should see the login page!**

### 4.3 Log In

1. **Enter the email and password** you created in Step 2.4
2. **Click "Sign In"**
3. **You should see the dashboard!**

---

## ✅ You're Done!

Your application is now running locally on your computer!

**To use it:**
1. Make sure the terminal is running `npm run dev`
2. Open http://localhost:3000 in your browser
3. Log in and use the app!

**To stop it:**
- Press `Ctrl + C` in the terminal window

**To start it again:**
- Open terminal in project folder
- Run: `npm run dev`

---

## Troubleshooting

### "npm: command not found"
- Node.js isn't installed or not in PATH
- Reinstall Node.js (Step 1)

### "Cannot connect to database"
- Check your `.env.local` file has correct values
- Make sure Supabase project is active
- Verify database password is correct

### "Port 3000 already in use"
- Another program is using port 3000
- Close other applications
- Or use a different port: `npm run dev -- -p 3001`
- Then go to: `http://localhost:3001`

### "Authentication failed"
- Make sure you created a user in Supabase (Step 2.4)
- Check that your Supabase URL and keys are correct in `.env.local`
- Try creating a new user in Supabase

### Page shows "Loading..." forever
- Check your terminal for error messages
- Make sure `npm run dev` is still running
- Verify your `.env.local` file is correct
- Try refreshing the page

---

## Daily Usage

**Every time you want to use the app:**

1. **Open terminal/command prompt**
2. **Navigate to project folder:**
   ```
   cd "C:\Users\YourName\Desktop\CRM Tool"
   ```
3. **Start the server:**
   ```
   npm run dev
   ```
4. **Open browser:** http://localhost:3000
5. **Log in and use it!**

**To stop:** Press `Ctrl + C` in the terminal

---

## Next Steps

Once it's running:
1. **Create a test barrel batch** to see how it works
2. **Explore all the features** - they're all documented in the app
3. **Add more users** in Supabase if needed (Authentication → Users)

---

## Security Note

**Never share your `.env.local` file!** It contains sensitive credentials. Keep it on your computer only.

---

**That's it! You're all set to use the application locally on your computer.** 🎉

If you run into any issues, check the troubleshooting section above or let me know what error you're seeing!

