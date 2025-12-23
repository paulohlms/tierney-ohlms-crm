# How to Find Your Supabase Credentials - Step by Step

**Follow these steps to get your Project URL, anon key, and database connection string.**

---

## Step 1: Log Into Supabase

1. **Go to:** https://supabase.com
2. **Click "Sign In"** (top right) or **"Start your project"**
3. **Log in** with your account

---

## Step 2: Select Your Project

1. **You'll see a list of projects** (or just one if you only have one)
2. **Click on your project** (probably named "Whiskey Inventory" or similar)
3. **Wait for the dashboard to load**

---

## Step 3: Get Project URL and Anon Key

### 3.1 Open Settings

1. **Look at the left sidebar** - you'll see a menu
2. **Click on "Settings"** (it has a gear icon ⚙️)
3. **You'll see a submenu appear**

### 3.2 Go to API Settings

1. **Under "Project Settings"**, click **"API"**
2. **A page loads with API information**

### 3.3 Copy Project URL

1. **Look for "Project URL"** section
2. **You'll see a URL** like: `https://abcdefghijklmnop.supabase.co`
3. **Click the copy icon** (looks like two squares overlapping) next to it
4. **Or select the text and copy it** (Ctrl+C)
5. **Paste it somewhere safe** (like a text file)

**This is your `NEXT_PUBLIC_SUPABASE_URL`**

### 3.4 Copy Anon Public Key

1. **Scroll down a bit** on the same page
2. **Look for "Project API keys"** section
3. **You'll see several keys listed:**
   - `anon` `public` (this is the one you need!)
   - `service_role` `secret` (don't use this one)
4. **Find the `anon` `public` key** - it's a long string starting with `eyJ...`
5. **Click the copy icon** next to it (or select and copy)
6. **Paste it somewhere safe**

**This is your `NEXT_PUBLIC_SUPABASE_ANON_KEY`**

---

## Step 4: Get Database Connection String

### 4.1 Go to Database Settings

1. **Still in Settings** (left sidebar)
2. **Click "Database"** (under "Project Settings")
3. **A new page loads**

### 4.2 Find Connection String

1. **Scroll down** to find "Connection string" section
2. **You'll see tabs:** `URI`, `JDBC`, `Golang`, etc.
3. **Click on the "URI" tab** (it should be selected by default)

### 4.3 Copy Connection String

1. **You'll see something like:**
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
   ```
2. **IMPORTANT:** You need to replace `[YOUR-PASSWORD]` with your actual password
3. **Remember the password you created** when you set up the project?
   - If you forgot it, you'll need to reset it (see below)
4. **Replace `[YOUR-PASSWORD]`** with your actual password
5. **Example:** If your password is `MyPassword123`, it should look like:
   ```
   postgresql://postgres:MyPassword123@db.abcdefghijklmnop.supabase.co:5432/postgres
   ```
6. **Select the entire string** and copy it (Ctrl+C)
7. **Paste it somewhere safe**

**This is your `DATABASE_URL`**

---

## Step 5: If You Forgot Your Database Password

**If you don't remember your database password:**

1. **Still in Database settings**
2. **Look for "Database password"** section
3. **Click "Reset database password"** or **"Generate new password"**
4. **Copy the new password** (write it down!)
5. **Use this new password** in your connection string

---

## Step 6: Put It All Together

**Now you have all three pieces:**

1. **Project URL:** `https://xxxxx.supabase.co`
2. **Anon Key:** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (long string)
3. **Database Connection String:** `postgresql://postgres:YourPassword@db.xxxxx.supabase.co:5432/postgres`

---

## Step 7: Add to .env.local File

1. **Open PowerShell** in Whiskey Inventory folder
2. **Type:**
   ```powershell
   notepad .env.local
   ```
3. **Notepad opens** - paste this template:

```
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
DATABASE_URL=
```

4. **Fill in your values:**
   - After `NEXT_PUBLIC_SUPABASE_URL=` paste your Project URL
   - After `NEXT_PUBLIC_SUPABASE_ANON_KEY=` paste your anon key
   - After `DATABASE_URL=` paste your connection string

**Example of what it should look like:**

```
NEXT_PUBLIC_SUPABASE_URL=https://abcdefghijklmnop.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTYxNjIzOTAyMiwiZXhwIjoxOTMxODE1MDIyfQ.abcdefghijklmnopqrstuvwxyz1234567890
DATABASE_URL=postgresql://postgres:MyPassword123@db.abcdefghijklmnop.supabase.co:5432/postgres
```

5. **Save** (Ctrl+S)
6. **Close Notepad**

---

## Visual Guide - Where to Click

### For Project URL and Anon Key:
```
Supabase Dashboard
├── Left Sidebar
│   └── Settings (gear icon) ⚙️
│       └── Project Settings
│           └── API ← Click here
│               ├── Project URL (copy this)
│               └── Project API keys
│                   └── anon public (copy this)
```

### For Database Connection String:
```
Supabase Dashboard
├── Left Sidebar
│   └── Settings (gear icon) ⚙️
│       └── Project Settings
│           └── Database ← Click here
│               └── Connection string
│                   └── URI tab (copy this, replace [YOUR-PASSWORD])
```

---

## Quick Checklist

- [ ] Logged into Supabase
- [ ] Selected my project
- [ ] Went to Settings → API
- [ ] Copied Project URL
- [ ] Copied anon public key
- [ ] Went to Settings → Database
- [ ] Clicked URI tab
- [ ] Copied connection string
- [ ] Replaced [YOUR-PASSWORD] with actual password
- [ ] Added all three to .env.local file
- [ ] Saved .env.local file

---

## Security Note

**Keep these credentials safe!**
- Don't share them publicly
- Don't commit .env.local to GitHub (it's already in .gitignore)
- These are like passwords - treat them carefully

---

## Still Having Trouble?

**If you can't find something:**

1. **Make sure you're logged into Supabase**
2. **Make sure you've selected the correct project**
3. **Look for the gear icon** (⚙️) - that's Settings
4. **Check both "API" and "Database"** under Project Settings

**If you see different options:**
- Supabase sometimes updates their interface
- Look for "API" or "Database" in the Settings menu
- The credentials are always in Settings somewhere

---

**That's it! Once you have all three values in your .env.local file, you're ready to run the app!** 🎉

