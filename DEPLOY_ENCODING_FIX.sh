#!/bin/bash
# Quick deployment script after encoding fixes

set -e

echo "============================================================"
echo "Deploying Encoding Fixes to Render"
echo "============================================================"
echo ""

# Step 1: Verify encoding
echo "[1] Verifying template encoding..."
python fix_all_templates_encoding.py

if [ $? -ne 0 ]; then
    echo "ERROR: Template encoding check failed!"
    exit 1
fi

# Step 2: Check git status
echo ""
echo "[2] Checking git status..."
git status

# Step 3: Add files
echo ""
echo "[3] Adding encoding fix files..."
git add templates/*.html
git add fix_all_templates_encoding.py
git add main.py 2>/dev/null || true
git add render.yaml 2>/dev/null || true

# Step 4: Commit
echo ""
echo "[4] Committing changes..."
git commit -m "Fix template encoding: Convert all HTML templates to UTF-8

- Fixed UnicodeDecodeError in templates
- Converted all .html files to clean UTF-8 without BOM
- Updated Jinja2 environment for UTF-8 handling
- Added render.yaml with UTF-8 environment variables"

# Step 5: Push
echo ""
echo "[5] Pushing to GitHub..."
git push origin main

echo ""
echo "============================================================"
echo "Deployment Steps:"
echo "============================================================"
echo "1. Go to Render Dashboard"
echo "2. Click your service"
echo "3. Click 'Manual Deploy'"
echo "4. Select 'Clear build cache & deploy'"
echo "5. Monitor logs for encoding errors"
echo ""
echo "Next: Monitor Render logs for 'UnicodeDecodeError'"
echo "============================================================"

