# PowerShell script for deploying encoding fixes to Render

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Deploying Encoding Fixes to Render" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Verify encoding
Write-Host "[1] Verifying template encoding..." -ForegroundColor Yellow
python fix_all_templates_encoding.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Template encoding check failed!" -ForegroundColor Red
    exit 1
}

# Step 2: Check git status
Write-Host ""
Write-Host "[2] Checking git status..." -ForegroundColor Yellow
git status

# Step 3: Add files
Write-Host ""
Write-Host "[3] Adding encoding fix files..." -ForegroundColor Yellow
git add templates/*.html
git add fix_all_templates_encoding.py
git add main.py 2>$null
git add render.yaml 2>$null

# Step 4: Commit
Write-Host ""
Write-Host "[4] Committing changes..." -ForegroundColor Yellow
$commitMessage = @"
Fix template encoding: Convert all HTML templates to UTF-8

- Fixed UnicodeDecodeError in templates
- Converted all .html files to clean UTF-8 without BOM
- Updated Jinja2 environment for UTF-8 handling
- Added render.yaml with UTF-8 environment variables
"@

git commit -m $commitMessage

# Step 5: Push
Write-Host ""
Write-Host "[5] Pushing to GitHub..." -ForegroundColor Yellow
git push origin main

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "Deployment Steps:" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host "1. Go to Render Dashboard" -ForegroundColor White
Write-Host "2. Click your service" -ForegroundColor White
Write-Host "3. Click 'Manual Deploy'" -ForegroundColor White
Write-Host "4. Select 'Clear build cache & deploy'" -ForegroundColor White
Write-Host "5. Monitor logs for encoding errors" -ForegroundColor White
Write-Host ""
Write-Host "Next: Monitor Render logs for 'UnicodeDecodeError'" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Green

