# Project Separation Plan - CRM Tool vs Whiskey Inventory

## Analysis Complete

Based on the file analysis, here's what I found:

---

## File Categorization

### ✅ **Project 1: CRM Tool (Python/FastAPI)**
**Clear CRM files:**
- `crm.db` - SQLite database
- `templates/` folder - HTML templates (clients_list.html)
- `static/` folder - Static files (currently empty)
- `__pycache__/` folder - Python cache

**Note:** Python source files (`.py`) appear to have been removed or are elsewhere, but the database and templates indicate this was a Python CRM system.

### ✅ **Project 2: Whiskey Inventory (Next.js/React/TypeScript)**
**Clear Whiskey Inventory files:**
- `app/` folder - Next.js app directory (all TypeScript/React)
- `components/` folder - React components
- `hooks/` folder - React hooks
- `lib/` folder - TypeScript utilities
- `prisma/` folder - Database schema
- `package.json` - Node.js dependencies
- `tsconfig.json` - TypeScript config
- `next.config.js` - Next.js config
- `tailwind.config.ts` - Tailwind CSS config
- `postcss.config.js` - PostCSS config

### ⚠️ **Ambiguous/Shared Files:**
- `.gitignore` - Contains patterns for both projects
- `README.md` - Currently describes Whiskey Inventory
- Documentation files (`.md`) - Mixed between both projects

### 📄 **Documentation Files:**
**Whiskey Inventory docs:**
- `LOCAL_SETUP_ONLY.md`
- `SETUP_GUIDE_FOR_ACCOUNTANTS.md`
- `DEPLOY_TO_PRODUCTION.md`
- `DEPLOYMENT.md`
- `QUICK_START_CHECKLIST.md`
- `QUICK_START.md`
- `RUN_IN_CHROME_STEPS.md`
- `FIX_POWERSHELL_ERROR.md`
- `UI_IMPROVEMENTS.md`
- `WHERE_ARE_MY_FILES.md`
- `ORGANIZE_FILES_INSTRUCTIONS.md`
- `organize_files.ps1`

**CRM Tool docs (likely):**
- Any files mentioning "CRM", "clients", "timesheets", "prospects" (if they exist)

---

## Proposed Folder Structure

```
C:\Users\PaulOhlms\Desktop\
├── CRM Tool\              (Original - will be cleaned)
└── Whiskey Inventory\     (New - Whiskey project)
```

---

## Safe Separation Steps

### Step 1: Create Backup (CRITICAL!)

**Before doing anything, create a backup:**

```powershell
# Create backup folder
New-Item -ItemType Directory -Path "C:\Users\PaulOhlms\Desktop\CRM Tool BACKUP" -Force

# Copy everything to backup
Copy-Item -Path "C:\Users\PaulOhlms\Desktop\CRM Tool\*" -Destination "C:\Users\PaulOhlms\Desktop\CRM Tool BACKUP\" -Recurse -Force
```

### Step 2: Create New Whiskey Inventory Folder

```powershell
# Create new folder on Desktop
New-Item -ItemType Directory -Path "C:\Users\PaulOhlms\Desktop\Whiskey Inventory" -Force
```

### Step 3: Move Whiskey Inventory Files

**Move application folders:**
```powershell
cd "C:\Users\PaulOhlms\Desktop\CRM Tool"

# Move application folders
Move-Item -Path "app" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\app"
Move-Item -Path "components" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\components"
Move-Item -Path "hooks" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\hooks"
Move-Item -Path "lib" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\lib"
Move-Item -Path "prisma" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\prisma"
```

**Move configuration files:**
```powershell
Move-Item -Path "package.json" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\package.json"
Move-Item -Path "tsconfig.json" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\tsconfig.json"
Move-Item -Path "next.config.js" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\next.config.js"
Move-Item -Path "tailwind.config.ts" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\tailwind.config.ts"
Move-Item -Path "postcss.config.js" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\postcss.config.js"
```

**Move Whiskey Inventory documentation:**
```powershell
Move-Item -Path "LOCAL_SETUP_ONLY.md" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\LOCAL_SETUP_ONLY.md"
Move-Item -Path "SETUP_GUIDE_FOR_ACCOUNTANTS.md" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\SETUP_GUIDE_FOR_ACCOUNTANTS.md"
Move-Item -Path "DEPLOY_TO_PRODUCTION.md" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\DEPLOY_TO_PRODUCTION.md"
Move-Item -Path "DEPLOYMENT.md" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\DEPLOYMENT.md"
Move-Item -Path "QUICK_START_CHECKLIST.md" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\QUICK_START_CHECKLIST.md"
Move-Item -Path "QUICK_START.md" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\QUICK_START.md"
Move-Item -Path "RUN_IN_CHROME_STEPS.md" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\RUN_IN_CHROME_STEPS.md"
Move-Item -Path "FIX_POWERSHELL_ERROR.md" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\FIX_POWERSHELL_ERROR.md"
Move-Item -Path "UI_IMPROVEMENTS.md" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\UI_IMPROVEMENTS.md"
Move-Item -Path "WHERE_ARE_MY_FILES.md" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\WHERE_ARE_MY_FILES.md"
Move-Item -Path "ORGANIZE_FILES_INSTRUCTIONS.md" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\ORGANIZE_FILES_INSTRUCTIONS.md"
Move-Item -Path "organize_files.ps1" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\organize_files.ps1"
Move-Item -Path "README.md" -Destination "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\README.md"
```

### Step 4: Handle Shared Files

**Create separate .gitignore files:**

**For Whiskey Inventory:**
```powershell
# Create .gitignore for Whiskey Inventory
@"
# Dependencies
node_modules/
/.pnp
.pnp.js

# Testing
/coverage

# Next.js
/.next/
/out/

# Production
/build

# Misc
.DS_Store
*.pem

# Debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Local env files
.env*.local
.env

# Vercel
.vercel

# TypeScript
*.tsbuildinfo
next-env.d.ts

# Prisma
/prisma/migrations
"@ | Out-File -FilePath "C:\Users\PaulOhlms\Desktop\Whiskey Inventory\.gitignore" -Encoding UTF8
```

**For CRM Tool (keep existing or create new):**
```powershell
# Create .gitignore for CRM Tool
@"
# Database
*.db
*.sqlite
*.sqlite3
crm.db

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv

# Environment variables
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
"@ | Out-File -FilePath "C:\Users\PaulOhlms\Desktop\CRM Tool\.gitignore" -Encoding UTF8
```

### Step 5: Clean Up CRM Tool Folder

**Remove Whiskey Inventory leftovers from CRM Tool:**
```powershell
cd "C:\Users\PaulOhlms\Desktop\CRM Tool"

# Remove Whiskey Inventory folders (if they still exist)
Remove-Item -Path "app" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "components" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "hooks" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "lib" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "prisma" -Recurse -Force -ErrorAction SilentlyContinue

# Remove Whiskey Inventory config files
Remove-Item -Path "package.json" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "tsconfig.json" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "next.config.js" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "tailwind.config.ts" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "postcss.config.js" -Force -ErrorAction SilentlyContinue
```

---

## Complete Separation Script

I'll create a PowerShell script that does all of this safely. Would you like me to create it?

---

## After Separation

### For Whiskey Inventory:
1. Navigate to: `C:\Users\PaulOhlms\Desktop\Whiskey Inventory`
2. Run: `npm install`
3. Create `.env.local` with Supabase credentials
4. Run: `npm run dev`

### For CRM Tool:
1. Navigate to: `C:\Users\PaulOhlms\Desktop\CRM Tool`
2. Continue using as before (Python/FastAPI setup)

---

## Git Repositories

After separation, you can initialize separate git repos:

**Whiskey Inventory:**
```powershell
cd "C:\Users\PaulOhlms\Desktop\Whiskey Inventory"
git init
git add .
git commit -m "Initial commit - Whiskey Inventory Management System"
```

**CRM Tool:**
```powershell
cd "C:\Users\PaulOhlms\Desktop\CRM Tool"
git init
git add .
git commit -m "Initial commit - CRM Tool"
```

---

## Safety Checklist

- [ ] Backup created
- [ ] Verified backup contains all files
- [ ] Run separation script
- [ ] Verify both projects work independently
- [ ] Initialize git repos
- [ ] Test both projects

---

**Ready to proceed? I'll create the automated script next!**

