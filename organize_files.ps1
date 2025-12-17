# PowerShell Script to Organize Whiskey Inventory Files
# This will create a new folder on your desktop and copy all Whiskey Inventory files

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Whiskey Inventory File Organizer" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Set paths
$desktopPath = [Environment]::GetFolderPath("Desktop")
$sourceFolder = "C:\Users\PaulOhlms\Desktop\CRM Tool"
$destinationFolder = Join-Path $desktopPath "Whiskey Inventory"

Write-Host "Source: $sourceFolder" -ForegroundColor Yellow
Write-Host "Destination: $destinationFolder" -ForegroundColor Yellow
Write-Host ""

# Create destination folder if it doesn't exist
if (-not (Test-Path $destinationFolder)) {
    New-Item -ItemType Directory -Path $destinationFolder | Out-Null
    Write-Host "Created folder: $destinationFolder" -ForegroundColor Green
} else {
    Write-Host "Folder already exists: $destinationFolder" -ForegroundColor Yellow
}

# Define files and folders to copy (Whiskey Inventory project)
$itemsToCopy = @(
    # Application folders
    "app",
    "components",
    "hooks",
    "lib",
    "prisma",
    
    # Configuration files
    "package.json",
    "tsconfig.json",
    "next.config.js",
    "tailwind.config.ts",
    "postcss.config.js",
    ".gitignore",
    
    # Documentation files
    "LOCAL_SETUP_ONLY.md",
    "SETUP_GUIDE_FOR_ACCOUNTANTS.md",
    "DEPLOY_TO_PRODUCTION.md",
    "DEPLOYMENT.md",
    "README.md",
    "UI_IMPROVEMENTS.md",
    "QUICK_START_CHECKLIST.md",
    "QUICK_START.md",
    "WHERE_ARE_MY_FILES.md"
)

Write-Host "Copying files and folders..." -ForegroundColor Cyan
Write-Host ""

$copiedCount = 0
$skippedCount = 0

foreach ($item in $itemsToCopy) {
    $sourcePath = Join-Path $sourceFolder $item
    $destPath = Join-Path $destinationFolder $item
    
    if (Test-Path $sourcePath) {
        try {
            Copy-Item -Path $sourcePath -Destination $destPath -Recurse -Force
            Write-Host "  ✓ Copied: $item" -ForegroundColor Green
            $copiedCount++
        } catch {
            Write-Host "  ✗ Error copying: $item - $($_.Exception.Message)" -ForegroundColor Red
        }
    } else {
        Write-Host "  ⊘ Not found: $item" -ForegroundColor Yellow
        $skippedCount++
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Copied: $copiedCount items" -ForegroundColor Green
Write-Host "Skipped: $skippedCount items" -ForegroundColor Yellow
Write-Host ""
Write-Host "Your Whiskey Inventory project is now in:" -ForegroundColor Cyan
Write-Host "$destinationFolder" -ForegroundColor White -BackgroundColor DarkBlue
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Open the new folder: $destinationFolder" -ForegroundColor White
Write-Host "2. Open PowerShell in that folder" -ForegroundColor White
Write-Host "3. Follow LOCAL_SETUP_ONLY.md to get started" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to open the folder..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Open the destination folder in File Explorer
Start-Process explorer.exe -ArgumentList $destinationFolder

Write-Host ""
Write-Host "Done! The folder has been opened for you." -ForegroundColor Green

