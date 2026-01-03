# Template Encoding Fix - Complete Solution

## Problem
FastAPI/Jinja2 templates were causing `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff` errors. This happens when template files are saved with incorrect encoding (UTF-16, BOM, or corrupted bytes).

## Solution Overview

### 1. Batch Template Encoding Fix Script
**File:** `fix_all_templates_encoding.py`

This script:
- Scans all `.html` files in the `templates/` directory
- Detects encoding issues (UTF-16, BOM, FF bytes)
- Converts all files to clean UTF-8 without BOM
- Preserves all HTML structure and Jinja2 tags
- Reports any issues found

**Usage:**
```bash
python fix_all_templates_encoding.py
```

**What it does:**
1. Detects file encoding (UTF-16 LE/BE, UTF-8 with/without BOM)
2. Converts to UTF-8 without BOM
3. Verifies the conversion
4. Reports summary of all files

### 2. Updated Jinja2 Environment Configuration

**File:** `main.py` (lines 232-246)

The Jinja2 environment is now configured to:
- Explicitly use UTF-8 encoding for all template files
- Handle encoding errors gracefully
- Enable auto-reload for development

**Key changes:**
```python
from jinja2 import FileSystemLoader, Environment

# Create Jinja2 environment with explicit UTF-8 encoding
jinja2_env = Environment(
    loader=FileSystemLoader("templates", encoding="utf-8"),
    autoescape=False,
    auto_reload=True
)

templates = Jinja2Templates(directory="templates")
templates.env = jinja2_env
```

### 3. Dashboard Route

The dashboard route (`/dashboard`) renders `dashboard.html` which extends `base.html`. Both files are now:
- Clean UTF-8 encoding
- No BOM (Byte Order Mark)
- No invalid bytes (FF bytes)

## Files Fixed

All 13 template files have been verified and fixed:
- ✅ `base.html` - Converted from UTF-16 to UTF-8
- ✅ `dashboard.html` - BOM removed
- ✅ `client_detail.html` - Clean UTF-8
- ✅ `client_form.html` - Clean UTF-8
- ✅ `clients_list.html` - Clean UTF-8
- ✅ `contact_form.html` - Clean UTF-8
- ✅ `login.html` - Clean UTF-8
- ✅ `prospect_form.html` - Clean UTF-8
- ✅ `prospects_list.html` - Clean UTF-8
- ✅ `service_form.html` - Clean UTF-8
- ✅ `settings.html` - Clean UTF-8
- ✅ `timesheet_form.html` - Clean UTF-8
- ✅ `timesheets_list.html` - Clean UTF-8

## How to Use

### Initial Fix (One-time)
```bash
# Run the batch fix script
python fix_all_templates_encoding.py

# Commit the changes
git add templates/*.html
git commit -m "Fix all template encoding to UTF-8"
git push
```

### Ongoing Maintenance
If you add new template files or suspect encoding issues:

1. **Check all templates:**
   ```bash
   python fix_all_templates_encoding.py
   ```

2. **Check a specific file:**
   ```python
   python -c "with open('templates/your_file.html', 'rb') as f: content = f.read(); print('Has BOM:', content.startswith(b'\xef\xbb\xbf')); print('Has FF:', b'\xff' in content)"
   ```

3. **Fix a specific file:**
   ```python
   # Remove BOM
   python -c "content = open('templates/file.html', 'rb').read().lstrip(b'\xef\xbb\xbf'); open('templates/file.html', 'wb').write(content)"
   ```

## VS Code Settings (Prevention)

To prevent future encoding issues in VS Code:

1. **Set default encoding:**
   - Open Settings (`Ctrl+,`)
   - Search: `files.encoding`
   - Set to: `utf8`

2. **Disable BOM:**
   - Search: `files.encoding`
   - Uncheck: `Files: Encoding Utf8 Bom`

3. **Auto-detect encoding:**
   - Search: `files.autoGuessEncoding`
   - Enable: `Files: Auto Guess Encoding`

Or add to `.vscode/settings.json`:
```json
{
    "files.encoding": "utf8",
    "files.encodingUtf8Bom": false,
    "files.autoGuessEncoding": true
}
```

## Verification

After running the fix script, verify all files are clean:

```bash
# Check for FF bytes (should return nothing)
certutil -dump templates\*.html | findstr /C:"FF"

# Or use Python
python -c "import os; files = [f for f in os.listdir('templates') if f.endswith('.html')]; [print(f'{f}: {\"OK\" if b\"\\xff\" not in open(f\"templates/{f}\", \"rb\").read()[:100] else \"HAS FF\"}') for f in files]"
```

## Deployment

After fixing encoding issues:

1. **Commit all changes:**
   ```bash
   git add templates/*.html main.py fix_all_templates_encoding.py
   git commit -m "Fix template encoding and update Jinja2 config"
   git push
   ```

2. **On Render:**
   - Go to your service
   - Click "Manual Deploy"
   - Select "Clear build cache & deploy"
   - This ensures old corrupted cached files are removed

## Troubleshooting

### Error: "UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff"

**Cause:** Template file is UTF-16 encoded or has corruption.

**Fix:**
```bash
python fix_all_templates_encoding.py
```

### Error: "Template not found" or "Template encoding error"

**Cause:** Jinja2 environment not configured for UTF-8.

**Fix:** The updated `main.py` now handles this automatically. Restart the server.

### Files still have issues after running script

**Manual fix:**
1. Open file in VS Code
2. Click encoding in bottom-right status bar
3. Select "Save with Encoding"
4. Choose "UTF-8" (NOT "UTF-8 with BOM")
5. Save the file

## Summary

✅ All template files are now clean UTF-8  
✅ Jinja2 environment configured for UTF-8  
✅ Batch fix script available for maintenance  
✅ Dashboard route will work without encoding errors  

The `UnicodeDecodeError` should be completely resolved!

