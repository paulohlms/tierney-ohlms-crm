# Fix: localhost:3000 Not Working - Step by Step

**Let's get your app running! Follow these steps in order.**

---

## Step 1: Check You're in the Right Folder

**In PowerShell, type this and press Enter:**

```powershell
cd "C:\Users\PaulOhlms\Desktop\Whiskey Inventory"
```

**Then type:**
```powershell
pwd
```

**You should see:** `C:\Users\PaulOhlms\Desktop\Whiskey Inventory`

**If you see something else, you're in the wrong folder!**

---

## Step 2: Check if Files Are There

**Type this and press Enter:**

```powershell
dir
```

**You should see:**
- `package.json`
- `app` folder
- `components` folder
- `prisma` folder
- etc.

**If you don't see these files, the files weren't moved correctly!**

---

## Step 3: Check if Dependencies Are Installed

**Type this and press Enter:**

```powershell
Test-Path "node_modules"
```

**If it says `False`:**
- Dependencies aren't installed
- **Run this:**
  ```powershell
  npm install
  ```
- **Wait 2-5 minutes** for it to finish

**If it says `True`:**
- Dependencies are installed ✅
- Continue to Step 4

---

## Step 4: Check if .env.local Exists

**Type this and press Enter:**

```powershell
Test-Path ".env.local"
```

**If it says `False`:**
- You need to create `.env.local` file
- **See Step 5 below**

**If it says `True`:**
- File exists ✅
- Continue to Step 6

---

## Step 5: Create .env.local File (If Missing)

**If Step 4 said `False`, you need to create this file:**

1. **In PowerShell, type:**
   ```powershell
   notepad .env.local
   ```

2. **Notepad opens** - paste this:
   ```
   NEXT_PUBLIC_SUPABASE_URL=your_project_url_here
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key_here
   DATABASE_URL=your_database_connection_string_here
   ```

3. **Replace the placeholders** with your actual Supabase credentials

4. **Save** (Ctrl+S) and **close Notepad**

---

## Step 6: Try Starting the App

**Type this and press Enter:**

```powershell
npm run dev
```

**Watch for errors!**

### ✅ **If you see this:**
```
▲ Next.js 14.0.4
- Local:        http://localhost:3000
✓ Ready in 2.3s
```

**SUCCESS!** The app is running. Go to http://localhost:3000 in Chrome.

### ❌ **If you see errors, read below:**

---

## Common Errors and Fixes

### Error: "npm: command not found"
**Fix:**
- Node.js isn't installed
- Go to https://nodejs.org/ and install it
- Close and reopen PowerShell after installing

### Error: "Cannot find module" or "Missing dependencies"
**Fix:**
```powershell
npm install
```
Wait for it to finish, then try `npm run dev` again

### Error: "Port 3000 is already in use"
**Fix:**
- Something else is using port 3000
- **Option 1:** Close other applications
- **Option 2:** Use a different port:
  ```powershell
  npm run dev -- -p 3001
  ```
  Then go to: http://localhost:3001

### Error: "Cannot connect to database" or "DATABASE_URL"
**Fix:**
- Your `.env.local` file is missing or incorrect
- Go back to Step 5 and create/fix it

### Error: "Prisma Client not generated"
**Fix:**
```powershell
npm run db:generate
```
Then try `npm run dev` again

### Error: Red text with "Error:" or "Failed"
**Fix:**
- Read the error message carefully
- It usually tells you what's wrong
- Common issues:
  - Missing `.env.local` file
  - Wrong Supabase credentials
  - Database not set up

---

## Step 7: Check What's Running

**If the app seems to start but Chrome still can't connect:**

1. **Look at PowerShell** - is it still showing the "Ready" message?
2. **Check for error messages** in red
3. **Try opening Chrome** and going to: http://localhost:3000
4. **If it says "This site can't be reached":**
   - The app probably isn't running
   - Check PowerShell for errors
   - Make sure you see "Ready" or "Compiled" message

---

## Complete Start-from-Scratch Checklist

**If nothing works, start over:**

1. ✅ **Open PowerShell**
2. ✅ **Go to Whiskey Inventory folder:**
   ```powershell
   cd "C:\Users\PaulOhlms\Desktop\Whiskey Inventory"
   ```
3. ✅ **Install dependencies:**
   ```powershell
   npm install
   ```
4. ✅ **Create .env.local file:**
   ```powershell
   notepad .env.local
   ```
   (Add your Supabase credentials)
5. ✅ **Set up database:**
   ```powershell
   npm run db:generate
   npm run db:push
   ```
6. ✅ **Start the app:**
   ```powershell
   npm run dev
   ```
7. ✅ **Open Chrome:** http://localhost:3000

---

## Still Not Working?

**Tell me:**
1. What folder are you in? (run `pwd` and tell me the result)
2. What error message do you see? (copy the exact text)
3. Did `npm install` complete successfully?
4. Do you have a `.env.local` file?

**I'll help you fix it!**

---

## Quick Diagnostic Commands

**Run these one at a time and tell me the results:**

```powershell
# Check current folder
pwd

# Check if package.json exists
Test-Path "package.json"

# Check if node_modules exists
Test-Path "node_modules"

# Check if .env.local exists
Test-Path ".env.local"

# Check Node.js version
node --version

# Check npm version
npm --version
```

**Copy the results and I'll help you fix the issue!**

---

**Let's get this working! Start with Step 1 above.** 🚀

