# Quick Test - See Live Editing Work

**Test that live editing works in 30 seconds!**

---

## The Test

### Step 1: Make Sure App is Running

**In PowerShell** (Whiskey Inventory folder):
```powershell
npm run dev
```

**In Chrome:**
- Go to: http://localhost:3000
- Log in
- You should see the dashboard

### Step 2: Make a Quick Edit

1. **Open this file:**
   - `C:\Users\PaulOhlms\Desktop\Whiskey Inventory\app\page.tsx`
   - Open in Notepad

2. **Find line 36** (look for "Dashboard"):
   ```tsx
   <h1 className="mb-8 text-4xl font-bold">Dashboard</h1>
   ```

3. **Change it to:**
   ```tsx
   <h1 className="mb-8 text-4xl font-bold">My Whiskey System</h1>
   ```

4. **Save** (Ctrl+S)

5. **Look at Chrome** - the title should change automatically!

---

## ✅ If It Works

**You'll see:**
- Chrome refreshes automatically
- Title changes from "Dashboard" to "My Whiskey System"
- Happens in 1-2 seconds

**This means live editing is working!**

---

## ❌ If It Doesn't Work

**Check:**
1. Is `npm run dev` still running in PowerShell?
2. Did you save the file? (Ctrl+S)
3. Try refreshing Chrome manually (F5)
4. Check PowerShell for error messages

---

**That's the test! If the title changes, live editing works!** 🎉

