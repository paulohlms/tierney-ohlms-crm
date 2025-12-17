# Fix PowerShell Execution Policy Error

You're getting this error because Windows is blocking scripts from running. Here's how to fix it:

---

## Quick Fix (30 seconds)

**In the same PowerShell window**, type this command and press Enter:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**You'll be asked to confirm** - type `Y` and press Enter.

**Then try again:**
```powershell
npm install
```

**That's it!** It should work now.

---

## What This Does

- **RemoteSigned**: Allows local scripts to run, but requires downloaded scripts to be signed
- **CurrentUser**: Only affects your user account (safe)
- This is a common, safe setting for developers

---

## Alternative: If That Doesn't Work

If you still get an error, try this instead:

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

Then try `npm install` again.

---

## After Fixing

Once you run the command above, you should be able to:
- Run `npm install` ✅
- Run `npm run dev` ✅
- Run all other npm commands ✅

---

## Still Having Issues?

If you're still getting errors:

1. **Close PowerShell completely**
2. **Right-click on PowerShell** → **"Run as Administrator"**
3. **Run the command again:**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
4. **Close PowerShell**
5. **Open a new PowerShell** (normal, not admin)
6. **Try `npm install` again**

---

**After running the fix command, go back to Step 4 in RUN_IN_CHROME_STEPS.md and continue!** 🚀

