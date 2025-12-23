# Find Database Connection String - Detailed Help

**Having trouble finding the connection string? Let's try different ways.**

---

## Method 1: Through Settings Menu

### Step-by-Step:

1. **In Supabase dashboard**, look at the **left sidebar**
2. **Find "Settings"** - it has a **gear icon** ⚙️
3. **Click "Settings"**
4. **You'll see a submenu** appear with options like:
   - General
   - API
   - Database
   - Auth
   - etc.
5. **Click "Database"** (it's usually the 3rd or 4th option)
6. **The page will change** - you'll see database settings
7. **Scroll down** on this page
8. **Look for a section called:**
   - "Connection string" OR
   - "Connection pooling" OR
   - "Database URL" OR
   - "Connection info"

---

## Method 2: Through Project Settings

### Alternative Path:

1. **Click "Settings"** (gear icon)
2. **Look for "Project Settings"** (might be a heading or section)
3. **Under "Project Settings"**, you should see:
   - API
   - Database ← **Click this one**
   - Auth
   - Storage
   - etc.
4. **Click "Database"**
5. **Scroll down** to find connection information

---

## Method 3: Direct Database Page

### Another Way:

1. **Look at the left sidebar** for "Database" (not in Settings)
2. **Click "Database"** directly from the sidebar
3. **You might see tabs** at the top like:
   - Tables
   - Functions
   - Extensions
   - Connection Pooling
   - Settings
4. **Click "Connection Pooling"** or **"Settings"** tab
5. **Look for connection string information**

---

## Method 4: What to Look For

**The connection string looks like this:**

```
postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
```

**Or it might be shown as:**

```
Host: db.xxxxx.supabase.co
Port: 5432
Database: postgres
User: postgres
Password: [YOUR-PASSWORD]
```

**If you see it in the second format, you need to put it together like the first format.**

---

## Method 5: Build It Manually

**If you can't find the connection string, you can build it yourself:**

### What You Need:
1. **Your database password** (the one you created when setting up the project)
2. **Your project reference** (found in Project URL)

### Steps:

1. **Get your Project URL:**
   - Settings → API → Project URL
   - It looks like: `https://abcdefghijklmnop.supabase.co`
   - The part after `https://` and before `.supabase.co` is your project reference
   - Example: `abcdefghijklmnop`

2. **Build the connection string:**
   ```
   postgresql://postgres:YOUR_PASSWORD@db.YOUR_PROJECT_REF.supabase.co:5432/postgres
   ```

3. **Replace:**
   - `YOUR_PASSWORD` with your actual database password
   - `YOUR_PROJECT_REF` with your project reference from step 1

**Example:**
- Project URL: `https://abcdefghijklmnop.supabase.co`
- Project reference: `abcdefghijklmnop`
- Password: `MyPassword123`
- Connection string: `postgresql://postgres:MyPassword123@db.abcdefghijklmnop.supabase.co:5432/postgres`

---

## Method 6: Check Connection Pooling

**Sometimes it's under Connection Pooling:**

1. **Settings → Database**
2. **Look for "Connection Pooling"** section
3. **Click on it** or expand it
4. **You might see connection strings there**

---

## What If You Still Can't Find It?

### Option A: Use the Manual Method (Method 5 above)
- This always works if you have your password and project reference

### Option B: Reset Your Password
1. **Settings → Database**
2. **Look for "Database password"** section
3. **Click "Reset database password"** or **"Generate new password"**
4. **Copy the new password**
5. **Use Method 5** to build the connection string with the new password

### Option C: Check Supabase Documentation
- The interface might have changed
- Go to: https://supabase.com/docs/guides/database/connecting-to-postgres
- This shows current ways to find connection strings

---

## Quick Checklist - What You Actually Need

**For the connection string, you need:**

1. ✅ **Database password** (you created this when setting up the project)
   - If you forgot it: Settings → Database → Reset password

2. ✅ **Project reference** (from your Project URL)
   - Found in: Settings → API → Project URL
   - It's the part between `https://` and `.supabase.co`

3. ✅ **Put it together:**
   ```
   postgresql://postgres:YOUR_PASSWORD@db.YOUR_PROJECT_REF.supabase.co:5432/postgres
   ```

---

## Screenshot Guide - What to Look For

**In the Database settings page, look for:**

- A section with a heading like "Connection string"
- A code box showing a URL starting with `postgresql://`
- Text that says "URI" or "Connection URI"
- A button that says "Copy" or has a copy icon
- Tabs at the top that say "URI", "JDBC", "Golang", etc.

**If you see any of these, that's where the connection string is!**

---

## Still Stuck?

**Tell me:**
1. **What do you see** when you click Settings → Database?
2. **What sections or headings** are on that page?
3. **Do you see anything** that mentions "connection", "URI", "postgresql", or "database URL"?

**I'll help you find it based on what you're seeing!**

---

## Alternative: I Can Help You Build It

**If you can find these two things, I can help you build the connection string:**

1. **Your Project URL** (from Settings → API)
   - Example: `https://abcdefghijklmnop.supabase.co`

2. **Your database password** (or reset it if you forgot)

**Just tell me these two things and I'll give you the exact connection string to use!**

---

**Try Method 5 (Build It Manually) - that's the easiest and always works!** 🚀

