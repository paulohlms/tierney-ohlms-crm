# How to Organize Files - Move Whiskey Inventory to Separate Folder

This will create a new folder on your desktop called "Whiskey Inventory" with all the project files.

## Quick Method (Recommended)

### Step 1: Run the PowerShell Script

1. **Open PowerShell** (Windows Key + X, then click "Windows PowerShell")
2. **Navigate to your CRM Tool folder:**
   ```powershell
   cd "C:\Users\PaulOhlms\Desktop\CRM Tool"
   ```
3. **Run the script:**
   ```powershell
   .\organize_files.ps1
   ```
4. **If you get an error about execution policy**, run this first:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
   Then try running the script again.

5. **The script will:**
   - Create a new folder: `C:\Users\PaulOhlms\Desktop\Whiskey Inventory`
   - Copy all Whiskey Inventory files to it
   - Open the new folder for you

---

## Manual Method (If Script Doesn't Work)

### Step 1: Create New Folder

1. **Go to your Desktop**
2. **Right-click** → **New** → **Folder**
3. **Name it:** `Whiskey Inventory`

### Step 2: Copy Files Manually

**Copy these folders:**
- `app` folder
- `components` folder
- `hooks` folder
- `lib` folder
- `prisma` folder

**Copy these files:**
- `package.json`
- `tsconfig.json`
- `next.config.js`
- `tailwind.config.ts`
- `postcss.config.js`
- `.gitignore`

**Copy these documentation files:**
- `LOCAL_SETUP_ONLY.md`
- `SETUP_GUIDE_FOR_ACCOUNTANTS.md`
- `DEPLOY_TO_PRODUCTION.md`
- `DEPLOYMENT.md`
- `README.md`
- `UI_IMPROVEMENTS.md`
- `QUICK_START_CHECKLIST.md`
- `QUICK_START.md`
- `WHERE_ARE_MY_FILES.md`

### Step 3: Verify

Your new folder structure should look like:
```
Whiskey Inventory/
├── app/
├── components/
├── hooks/
├── lib/
├── prisma/
├── package.json
├── tsconfig.json
├── next.config.js
├── tailwind.config.ts
├── postcss.config.js
├── .gitignore
├── LOCAL_SETUP_ONLY.md
├── SETUP_GUIDE_FOR_ACCOUNTANTS.md
├── DEPLOY_TO_PRODUCTION.md
├── README.md
└── (other .md files)
```

---

## After Organizing

1. **Open the new "Whiskey Inventory" folder**
2. **Open PowerShell in that folder** (type `powershell` in address bar)
3. **Follow `LOCAL_SETUP_ONLY.md`** to set up and run the project

---

## What Stays in CRM Tool Folder?

**These files stay in CRM Tool** (they're for your old Python CRM):
- All `.py` files (Python files)
- `templates/` folder (HTML templates)
- `static/` folder
- `crm.db` (database)
- `requirements.txt` (Python dependencies)
- All the old CRM documentation files

**These are now in Whiskey Inventory** (new Next.js project):
- All TypeScript/React files
- Next.js configuration
- Prisma database setup
- All Whiskey Inventory documentation

---

## Need Help?

If the script doesn't work:
1. Try the manual method above
2. Make sure you're in the right folder when running the script
3. Check that you have permission to create folders on your Desktop

---

**Your Whiskey Inventory project will be completely separate from your CRM Tool!** 🎯




