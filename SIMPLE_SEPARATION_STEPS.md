# Simple Step-by-Step: Separate Your Two Projects

**Follow these steps exactly. Copy and paste the commands.**

---

## Step 1: Open PowerShell (2 minutes)

1. **Press the Windows key** on your keyboard
2. **Type:** `powershell`
3. **Press Enter**
4. **A blue window opens** - that's PowerShell!

---

## Step 2: Go to Your Project Folder (30 seconds)

**Copy this entire line and paste it into PowerShell (right-click to paste), then press Enter:**

```powershell
cd "C:\Users\PaulOhlms\Desktop\CRM Tool"
```

**You should see:** `PS C:\Users\PaulOhlms\Desktop\CRM Tool>`

---

## Step 3: Create a Backup (2 minutes)

**Copy and paste this command, press Enter:**

```powershell
Copy-Item -Path "C:\Users\PaulOhlms\Desktop\CRM Tool" -Destination "C:\Users\PaulOhlms\Desktop\CRM Tool BACKUP" -Recurse
```

**Wait for it to finish** (you'll see your cursor again when it's done).

**This creates a backup so nothing gets lost!**

---

## Step 4: Create the New Whiskey Inventory Folder (30 seconds)

**Copy and paste this command, press Enter:**

```powershell
New-Item -ItemType Directory -Path "C:\Users\PaulOhlms\Desktop\Whiskey Inventory"
```

**You should see:** `Directory: C:\Users\PaulOhlms\Desktop\Whiskey Inventory`

**OR if you see an error saying "already exists":**
- ✅ **That's fine!** The folder already exists, so skip to Step 5.

---

## Step 5: Move the App Folder (30 seconds)

**Copy and paste this command, press Enter:**

```powershell
Move-Item -Path "C:\Users\PaulOhlms\Desktop\CRM Tool\app" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\app"
```

---

## Step 6: Move the Components Folder (30 seconds)

**Copy and paste this command, press Enter:**

```powershell
Move-Item -Path "C:\Users\PaulOhlms\Desktop\CRM Tool\components" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\components"
```

---

## Step 7: Move the Hooks Folder (30 seconds)

**Copy and paste this command, press Enter:**

```powershell
Move-Item -Path "C:\Users\PaulOhlms\Desktop\CRM Tool\hooks" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\hooks"
```

---

## Step 8: Move the Lib Folder (30 seconds)

**Copy and paste this command, press Enter:**

```powershell
Move-Item -Path "C:\Users\PaulOhlms\Desktop\CRM Tool\lib" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\lib"
```

---

## Step 9: Move the Prisma Folder (30 seconds)

**Copy and paste this command, press Enter:**

```powershell
Move-Item -Path "C:\Users\PaulOhlms\Desktop\CRM Tool\prisma" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\prisma"
```

---

## Step 10: Move Package.json (30 seconds)

**Copy and paste this command, press Enter:**

```powershell
Move-Item -Path "C:\Users\PaulOhlms\Desktop\CRM Tool\package.json" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\package.json"
```

---

## Step 11: Move tsconfig.json (30 seconds)

**Copy and paste this command, press Enter:**

```powershell
Move-Item -Path "C:\Users\PaulOhlms\Desktop\CRM Tool\tsconfig.json" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\tsconfig.json"
```

---

## Step 12: Move next.config.js (30 seconds)

**Copy and paste this command, press Enter:**

```powershell
Move-Item -Path "C:\Users\PaulOhlms\Desktop\CRM Tool\next.config.js" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\next.config.js"
```

---

## Step 13: Move tailwind.config.ts (30 seconds)

**Copy and paste this command, press Enter:**

```powershell
Move-Item -Path "C:\Users\PaulOhlms\Desktop\CRM Tool\tailwind.config.ts" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\tailwind.config.ts"
```

---

## Step 14: Move postcss.config.js (30 seconds)

**Copy and paste this command, press Enter:**

```powershell
Move-Item -Path "C:\Users\PaulOhlms\Desktop\CRM Tool\postcss.config.js" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\postcss.config.js"
```

---

## Step 15: Move README.md (30 seconds)

**Copy and paste this command, press Enter:**

```powershell
Move-Item -Path "C:\Users\PaulOhlms\Desktop\CRM Tool\README.md" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\README.md"
```

---

## Step 16: Move Setup Guides (2 minutes)

**Copy and paste these commands one at a time, pressing Enter after each:**

```powershell
Move-Item -Path "C:\Users\PaulOhlms\Desktop\CRM Tool\LOCAL_SETUP_ONLY.md" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\LOCAL_SETUP_ONLY.md"
```

```powershell
Move-Item -Path "C:\Users\PaulOhlms\Desktop\CRM Tool\SETUP_GUIDE_FOR_ACCOUNTANTS.md" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\SETUP_GUIDE_FOR_ACCOUNTANTS.md"
```

```powershell
Move-Item -Path "C:\Users\PaulOhlms\Desktop\CRM Tool\DEPLOY_TO_PRODUCTION.md" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\DEPLOY_TO_PRODUCTION.md"
```

```powershell
Move-Item -Path "C:\Users\PaulOhlms\Desktop\CRM Tool\DEPLOYMENT.md" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\DEPLOYMENT.md"
```

```powershell
Move-Item -Path "C:\Users\PaulOhlms\Desktop\CRM Tool\RUN_IN_CHROME_STEPS.md" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\RUN_IN_CHROME_STEPS.md"
```

```powershell
Move-Item -Path "C:\Users\PaulOhlms\Desktop\CRM Tool\FIX_POWERSHELL_ERROR.md" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\FIX_POWERSHELL_ERROR.md"
```

```powershell
Move-Item -Path "C:\Users\PaulOhlms\Desktop\CRM Tool\UI_IMPROVEMENTS.md" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\UI_IMPROVEMENTS.md"
```

```powershell
Move-Item -Path "C:\Users\PaulOhlms\Desktop\CRM Tool\QUICK_START_CHECKLIST.md" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\QUICK_START_CHECKLIST.md"
```

```powershell
Move-Item -Path "C:\Users\PaulOhlms\Desktop\CRM Tool\QUICK_START.md" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\QUICK_START.md"
```

```powershell
Move-Item -Path "C:\Users\PaulOhlms\Desktop\CRM Tool\WHERE_ARE_MY_FILES.md" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\WHERE_ARE_MY_FILES.md"
```

---

## ✅ You're Done!

**Your projects are now separated!**

---

## Check Your Work

1. **Open File Explorer**
2. **Go to your Desktop**
3. **You should see:**
   - `CRM Tool` folder (your original CRM)
   - `Whiskey Inventory` folder (your new inventory system)
   - `CRM Tool BACKUP` folder (your safety backup)

---

## Next Steps for Whiskey Inventory

1. **Open PowerShell**
2. **Copy and paste this:**
   ```powershell
   cd "C:\Users\PaulOhlms\Desktop\Whiskey Inventory"
   ```
3. **Press Enter**
4. **Follow the setup guide:** `RUN_IN_CHROME_STEPS.md`

---

## If Something Goes Wrong

**Don't panic!** Your backup is here:
- `C:\Users\PaulOhlms\Desktop\CRM Tool BACKUP`

**To restore everything:**
1. Delete the `CRM Tool` folder
2. Copy the `CRM Tool BACKUP` folder
3. Rename it to `CRM Tool`

---

**That's it! Just copy and paste each command, one at a time.** 🎉

