# Live Editing Guide - Edit Files and See Changes Instantly

**Good news!** Your Whiskey Inventory app already updates automatically when you edit files - just like your CRM!

---

## How It Works

When you run `npm run dev`, the app watches for file changes and automatically:
- ✅ Detects when you save a file
- ✅ Recompiles only what changed
- ✅ Refreshes your browser automatically
- ✅ Shows changes in 1-2 seconds

**No need to restart anything!**

---

## Quick Test - See It In Action

### Step 1: Make Sure App is Running

1. **Open PowerShell** in Whiskey Inventory folder
2. **Run:**
   ```powershell
   npm run dev
   ```
3. **Open Chrome** to http://localhost:3000
4. **Log in** to see the dashboard

### Step 2: Make a Test Edit

1. **Open the dashboard file:**
   - Go to: `C:\Users\PaulOhlms\Desktop\Whiskey Inventory\app\page.tsx`
   - Open it in Notepad or any text editor

2. **Find this line** (around line 36):
   ```tsx
   <h1 className="mb-8 text-4xl font-bold">Dashboard</h1>
   ```

3. **Change it to:**
   ```tsx
   <h1 className="mb-8 text-4xl font-bold">My Whiskey Dashboard</h1>
   ```

4. **Save the file** (Ctrl+S)

5. **Look at your Chrome browser** - it should automatically refresh and show "My Whiskey Dashboard"!

**That's it!** Changes appear instantly.

---

## What Files Can You Edit?

### ✅ **Pages** (What users see)
- `app/page.tsx` - Dashboard
- `app/barrel-batches/page.tsx` - Barrel Batches page
- `app/barrels/page.tsx` - Barrels page
- `app/usage-logs/page.tsx` - Usage Logs page
- `app/bottling-runs/page.tsx` - Bottling Runs page
- `app/shipments/page.tsx` - Shipments page
- `app/reports/page.tsx` - Reports page
- `app/login/page.tsx` - Login page

### ✅ **Components** (Reusable UI pieces)
- `components/nav.tsx` - Navigation bar
- `components/data-table.tsx` - Data table component
- `components/barrel-batch-dialog.tsx` - Create batch form
- `components/barrel-dialog.tsx` - Edit barrel form
- All files in `components/ui/` - Button, Input, etc.

### ✅ **Styling**
- `app/globals.css` - Global styles
- Individual component files (they have styling built-in)

### ✅ **API Routes** (Backend logic)
- `app/api/dashboard/stats/route.ts` - Dashboard data
- `app/api/barrel-batches/route.ts` - Barrel batch operations
- `app/api/barrels/route.ts` - Barrel operations
- All files in `app/api/` folder

---

## Editing Workflow

### 1. Start the App (Once Per Session)

```powershell
cd "C:\Users\PaulOhlms\Desktop\Whiskey Inventory"
npm run dev
```

**Keep PowerShell open!**

### 2. Open Chrome

- Go to: http://localhost:3000
- Log in

### 3. Edit Files

- Open any file in Notepad, VS Code, or any editor
- Make your changes
- **Save the file** (Ctrl+S)

### 4. See Changes Instantly

- Browser refreshes automatically
- Changes appear in 1-2 seconds
- **No restart needed!**

---

## Common Edits You Might Want to Make

### Change Page Titles

**File:** `app/page.tsx`
**Find:** `Dashboard`
**Change to:** Whatever you want

### Change Button Text

**File:** `app/barrel-batches/page.tsx`
**Find:** `Create New Batch`
**Change to:** `Add Barrel Batch` (or whatever you want)

### Change Colors/Styling

**File:** `app/globals.css`
**Add custom styles here**

### Change Form Labels

**File:** `components/barrel-batch-dialog.tsx`
**Find:** `Batch Name (Optional)`
**Change to:** Whatever label you want

---

## Tips for Editing

### ✅ **DO:**
- Save files frequently (Ctrl+S)
- Keep `npm run dev` running
- Keep Chrome open
- Make small changes and test

### ❌ **DON'T:**
- Don't close PowerShell while editing
- Don't edit files while the app isn't running
- Don't delete important files
- Don't change file names without updating imports

---

## If Changes Don't Appear

### Check 1: Is the app running?
- Look at PowerShell - should show "Ready" or "Compiled"
- If not, restart: `npm run dev`

### Check 2: Did you save the file?
- Make sure you pressed Ctrl+S
- Check the file timestamp changed

### Check 3: Check for errors
- Look at PowerShell for red error messages
- Fix any errors shown

### Check 4: Hard refresh browser
- Press Ctrl+F5 in Chrome
- Or close and reopen Chrome

---

## Example: Change Dashboard Welcome Message

1. **Open:** `app/page.tsx`
2. **Find this section** (around line 36):
   ```tsx
   <div className="mb-8">
     <h1 className="text-4xl font-bold mb-2">Dashboard</h1>
     <p className="text-muted-foreground text-lg">Overview of your whiskey inventory and operations</p>
   </div>
   ```

3. **Change it to:**
   ```tsx
   <div className="mb-8">
     <h1 className="text-4xl font-bold mb-2">Whiskey Inventory Dashboard</h1>
     <p className="text-muted-foreground text-lg">Welcome! Manage your barrels, bottling runs, and shipments here.</p>
   </div>
   ```

4. **Save** (Ctrl+S)
5. **Look at Chrome** - it updates automatically!

---

## Example: Change a Button Label

1. **Open:** `app/barrel-batches/page.tsx`
2. **Find this line** (around line 100):
   ```tsx
   <Button onClick={() => setDialogOpen(true)} size="lg" className="h-12 px-6">
     <Plus className="mr-2 h-5 w-5" />
     Create New Batch
   </Button>
   ```

3. **Change "Create New Batch" to:**
   ```tsx
   Add Barrel Purchase
   ```

4. **Save** (Ctrl+S)
5. **Look at Chrome** - button text updates!

---

## File Structure Reference

```
Whiskey Inventory/
├── app/                    ← Pages (what users see)
│   ├── page.tsx           ← Dashboard
│   ├── barrel-batches/    ← Barrel batches page
│   ├── barrels/           ← Barrels page
│   └── api/               ← Backend API
├── components/             ← Reusable components
│   ├── nav.tsx            ← Navigation bar
│   ├── data-table.tsx     ← Table component
│   └── ui/                ← UI components (buttons, inputs)
├── lib/                    ← Utilities
└── app/globals.css         ← Global styles
```

---

## Advanced: Edit API Logic

**Example: Change how dashboard stats are calculated**

1. **Open:** `app/api/dashboard/stats/route.ts`
2. **Make your changes**
3. **Save**
4. **Refresh the dashboard page** in Chrome
5. **Changes apply!**

---

## Restarting When Needed

**You only need to restart if:**
- You add new dependencies (run `npm install` first)
- You change environment variables (`.env.local`)
- You change database schema (run `npm run db:push`)
- Something breaks and you need a fresh start

**To restart:**
1. Press `Ctrl + C` in PowerShell
2. Run `npm run dev` again

---

## Quick Reference

**Start editing:**
1. `npm run dev` (running)
2. Chrome open to http://localhost:3000
3. Edit any file
4. Save (Ctrl+S)
5. See changes instantly!

**No restart needed for most edits!**

---

**That's it! Edit files, save, and see changes instantly - just like your CRM!** 🎉

