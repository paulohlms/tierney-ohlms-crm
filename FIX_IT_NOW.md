# Fix localhost:3000 - Copy These Commands

**I found the problems! Follow these steps exactly.**

---

## Problem 1: Dependencies Not Installed

**Copy and paste this command, press Enter:**

```powershell
cd "C:\Users\PaulOhlms\Desktop\Whiskey Inventory"
```

**Then copy and paste this, press Enter:**

```powershell
npm install
```

**Wait 2-5 minutes** - you'll see lots of text scrolling.

**When it's done**, you'll see your command prompt again.

---

## Problem 2: Missing .env.local File

**Copy and paste this command, press Enter:**

```powershell
notepad .env.local
```

**Notepad opens** - copy and paste this:

```
NEXT_PUBLIC_SUPABASE_URL=your_project_url_here
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key_here
DATABASE_URL=your_database_connection_string_here
```

**Now you need to replace the placeholders with your actual Supabase credentials.**

**If you don't have Supabase set up yet:**
- See "Set Up Supabase" section below

**If you already have Supabase credentials:**
- Replace `your_project_url_here` with your Supabase Project URL
- Replace `your_anon_key_here` with your Supabase anon key
- Replace `your_database_connection_string_here` with your database connection string

**Then:**
- **Save** (Ctrl+S)
- **Close Notepad**

---

## Set Up Supabase (If You Haven't)

**If you don't have Supabase credentials yet:**

1. **Go to:** https://supabase.com
2. **Sign up** or log in
3. **Create a new project:**
   - Name: `Whiskey Inventory`
   - Password: Create one (write it down!)
   - Region: Closest to you
   - Plan: Free
4. **Wait 2-3 minutes** for setup
5. **Get credentials:**
   - Settings → API → Copy Project URL and anon key
   - Settings → Database → Copy connection string (replace [YOUR-PASSWORD])
6. **Create a user:**
   - Authentication → Users → Add user
   - Create email and password (write it down!)

---

## Step 3: Set Up Database

**Copy and paste this, press Enter:**

```powershell
npm run db:generate
```

**Wait ~30 seconds**, then copy and paste this, press Enter:

```powershell
npm run db:push
```

**Wait for it to finish.**

---

## Step 4: Start the App

**Copy and paste this, press Enter:**

```powershell
npm run dev
```

**You should see:**
```
▲ Next.js 14.0.4
- Local:        http://localhost:3000
✓ Ready
```

**If you see this, it's working!**

---

## Step 5: Open in Chrome

1. **Open Google Chrome**
2. **Type in address bar:** `http://localhost:3000`
3. **Press Enter**
4. **You should see the login page!**

---

## If You Still See Errors

**Copy the exact error message** and tell me what it says.

**Common fixes:**

### "Port 3000 already in use"
```powershell
npm run dev -- -p 3001
```
Then go to: http://localhost:3001

### "Cannot connect to database"
- Check your `.env.local` file has correct values
- Make sure Supabase project is active

### "npm: command not found"
- Install Node.js from https://nodejs.org/
- Close and reopen PowerShell

---

## Quick Checklist

- [ ] Ran `npm install` (took 2-5 minutes)
- [ ] Created `.env.local` file with Supabase credentials
- [ ] Ran `npm run db:generate`
- [ ] Ran `npm run db:push`
- [ ] Ran `npm run dev`
- [ ] See "Ready" message in PowerShell
- [ ] Opened Chrome to http://localhost:3000

**If all checked, it should work!**

---

**Start with the first command above and work through each step!** 🚀

