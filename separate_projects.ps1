# PowerShell Script to Safely Separate CRM Tool and Whiskey Inventory Projects
# Run this script from the CRM Tool directory

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Project Separation Script" -ForegroundColor Cyan
Write-Host "CRM Tool vs Whiskey Inventory" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Set paths
$desktopPath = [Environment]::GetFolderPath("Desktop")
$sourceFolder = "C:\Users\PaulOhlms\Desktop\CRM Tool"
$backupFolder = Join-Path $desktopPath "CRM Tool BACKUP"
$whiskeyFolder = Join-Path $desktopPath "Whiskey Inventory"

# Step 1: Create Backup
Write-Host "Step 1: Creating backup..." -ForegroundColor Yellow
if (-not (Test-Path $backupFolder)) {
    New-Item -ItemType Directory -Path $backupFolder | Out-Null
    Write-Host "  Created backup folder: $backupFolder" -ForegroundColor Green
} else {
    Write-Host "  Backup folder already exists: $backupFolder" -ForegroundColor Yellow
    $overwrite = Read-Host "  Overwrite existing backup? (y/n)"
    if ($overwrite -ne "y") {
        Write-Host "  Backup skipped. Exiting for safety." -ForegroundColor Red
        exit
    }
}

Write-Host "  Copying files to backup..." -ForegroundColor Yellow
Copy-Item -Path "$sourceFolder\*" -Destination $backupFolder -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "  ✓ Backup complete!" -ForegroundColor Green
Write-Host ""

# Step 2: Create Whiskey Inventory Folder
Write-Host "Step 2: Creating Whiskey Inventory folder..." -ForegroundColor Yellow
if (-not (Test-Path $whiskeyFolder)) {
    New-Item -ItemType Directory -Path $whiskeyFolder | Out-Null
    Write-Host "  ✓ Created: $whiskeyFolder" -ForegroundColor Green
} else {
    Write-Host "  Folder already exists: $whiskeyFolder" -ForegroundColor Yellow
    $overwrite = Read-Host "  Continue anyway? (y/n)"
    if ($overwrite -ne "y") {
        Write-Host "  Exiting." -ForegroundColor Red
        exit
    }
}
Write-Host ""

# Step 3: Move Whiskey Inventory Application Folders
Write-Host "Step 3: Moving Whiskey Inventory application folders..." -ForegroundColor Yellow
$foldersToMove = @("app", "components", "hooks", "lib", "prisma")

foreach ($folder in $foldersToMove) {
    $sourcePath = Join-Path $sourceFolder $folder
    $destPath = Join-Path $whiskeyFolder $folder
    
    if (Test-Path $sourcePath) {
        Move-Item -Path $sourcePath -Destination $destPath -Force
        Write-Host "  ✓ Moved: $folder" -ForegroundColor Green
    } else {
        Write-Host "  ⊘ Not found: $folder" -ForegroundColor Yellow
    }
}
Write-Host ""

# Step 4: Move Whiskey Inventory Configuration Files
Write-Host "Step 4: Moving Whiskey Inventory configuration files..." -ForegroundColor Yellow
$configFiles = @(
    "package.json",
    "tsconfig.json",
    "next.config.js",
    "tailwind.config.ts",
    "postcss.config.js"
)

foreach ($file in $configFiles) {
    $sourcePath = Join-Path $sourceFolder $file
    $destPath = Join-Path $whiskeyFolder $file
    
    if (Test-Path $sourcePath) {
        Move-Item -Path $sourcePath -Destination $destPath -Force
        Write-Host "  ✓ Moved: $file" -ForegroundColor Green
    } else {
        Write-Host "  ⊘ Not found: $file" -ForegroundColor Yellow
    }
}
Write-Host ""

# Step 5: Move Whiskey Inventory Documentation
Write-Host "Step 5: Moving Whiskey Inventory documentation..." -ForegroundColor Yellow
$docsToMove = @(
    "LOCAL_SETUP_ONLY.md",
    "SETUP_GUIDE_FOR_ACCOUNTANTS.md",
    "DEPLOY_TO_PRODUCTION.md",
    "DEPLOYMENT.md",
    "QUICK_START_CHECKLIST.md",
    "QUICK_START.md",
    "RUN_IN_CHROME_STEPS.md",
    "FIX_POWERSHELL_ERROR.md",
    "UI_IMPROVEMENTS.md",
    "WHERE_ARE_MY_FILES.md",
    "ORGANIZE_FILES_INSTRUCTIONS.md",
    "organize_files.ps1",
    "README.md"
)

foreach ($doc in $docsToMove) {
    $sourcePath = Join-Path $sourceFolder $doc
    $destPath = Join-Path $whiskeyFolder $doc
    
    if (Test-Path $sourcePath) {
        Move-Item -Path $sourcePath -Destination $destPath -Force
        Write-Host "  ✓ Moved: $doc" -ForegroundColor Green
    } else {
        Write-Host "  ⊘ Not found: $doc" -ForegroundColor Yellow
    }
}
Write-Host ""

# Step 6: Create .gitignore for Whiskey Inventory
Write-Host "Step 6: Creating .gitignore for Whiskey Inventory..." -ForegroundColor Yellow
$whiskeyGitignore = @"
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
"@

$whiskeyGitignore | Out-File -FilePath (Join-Path $whiskeyFolder ".gitignore") -Encoding UTF8 -NoNewline
Write-Host "  ✓ Created .gitignore" -ForegroundColor Green
Write-Host ""

# Step 7: Create .gitignore for CRM Tool
Write-Host "Step 7: Creating .gitignore for CRM Tool..." -ForegroundColor Yellow
$crmGitignore = @"
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
"@

$crmGitignore | Out-File -FilePath (Join-Path $sourceFolder ".gitignore") -Encoding UTF8 -NoNewline
Write-Host "  ✓ Created .gitignore" -ForegroundColor Green
Write-Host ""

# Step 8: Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Separation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backup location:" -ForegroundColor Yellow
Write-Host "  $backupFolder" -ForegroundColor White
Write-Host ""
Write-Host "CRM Tool location:" -ForegroundColor Yellow
Write-Host "  $sourceFolder" -ForegroundColor White
Write-Host ""
Write-Host "Whiskey Inventory location:" -ForegroundColor Yellow
Write-Host "  $whiskeyFolder" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Verify both folders contain the correct files" -ForegroundColor White
Write-Host "2. Test Whiskey Inventory: cd '$whiskeyFolder' then npm install" -ForegroundColor White
Write-Host "3. Initialize git repos in each folder if needed" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to open both folders..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Open both folders
Start-Process explorer.exe -ArgumentList $sourceFolder
Start-Sleep -Seconds 1
Start-Process explorer.exe -ArgumentList $whiskeyFolder

Write-Host ""
Write-Host "Done! Both folders have been opened." -ForegroundColor Green

