# Testing Dashboard Endpoint

## Quick Start

### Option 1: Simple Test (No Dependencies)
```bash
# Uses only built-in Python libraries
python test_dashboard_simple.py
```

### Option 2: Full Test (Requires requests)
```bash
# Install requests if needed
pip install requests

# Run test
python test_dashboard_simple.py
```

### Option 3: cURL (Bash/Unix)
```bash
bash test_dashboard_curl.sh
```

## Prerequisites

1. **Start your FastAPI server:**
   ```bash
   uvicorn main:app --reload
   ```

2. **Verify server is running:**
   - Open browser to `http://localhost:8000/login`
   - Should see login page

## Test Scripts

### `test_dashboard_simple.py`
- ✅ No external dependencies
- ✅ Uses built-in `urllib` library
- ✅ Works on any Python 3.x installation
- ✅ Full session handling

### `test_dashboard_endpoint.py`
- ⚠️ Requires `pip install requests`
- ✅ More detailed output
- ✅ Better error messages
- ✅ Full session handling

### `test_dashboard_curl.sh`
- ✅ Bash script using curl
- ✅ Works on Linux/Mac/Git Bash
- ✅ No Python required

## Expected Output

### Success:
```
======================================================================
Testing /dashboard Endpoint
======================================================================

[1] Logging in as admin@tierneyohlms.com...
    Status Code: 303
    Redirect Location: http://localhost:8000/dashboard
    [OK] Login successful - redirected to dashboard
    Session Cookies: {'session': '...'}

[2] Accessing /dashboard endpoint...
    Status Code: 200
    Content-Type: text/html; charset=utf-8
    Content Length: 12345 bytes
    [OK] Dashboard loaded successfully
    [OK] Dashboard content appears valid
    [OK] Base template structure found

======================================================================
[SUCCESS] Dashboard endpoint test passed!
======================================================================
```

### Failure:
```
[ERROR] Dashboard request failed: ...
Next steps:
1. Check server logs for errors
2. Verify template encoding (run: python fix_all_templates_encoding.py)
3. Use VS Code debugger (see DEBUG_DASHBOARD.md)
```

## Debugging

See `DEBUG_DASHBOARD.md` for complete VS Code debugger setup and troubleshooting guide.

## Manual Testing

### Using Browser:
1. Go to `http://localhost:8000/login`
2. Login with: `admin@tierneyohlms.com` / `ChangeMe123!`
3. Should redirect to `/dashboard`
4. Check browser console (F12) for errors

### Using cURL (Manual):
```bash
# Login
curl -c cookies.txt -b cookies.txt \
  -X POST \
  -d "email=admin@tierneyohlms.com" \
  -d "password=ChangeMe123!" \
  http://localhost:8000/login

# Access dashboard
curl -b cookies.txt http://localhost:8000/dashboard
```

## Troubleshooting

### "Connection refused"
- Server not running: `uvicorn main:app --reload`

### "Login failed"
- Check credentials: `admin@tierneyohlms.com` / `ChangeMe123!`
- Check server logs for errors
- Verify database is accessible

### "UnicodeDecodeError"
- Run: `python fix_all_templates_encoding.py`
- Check template files are UTF-8

### "Redirected to login"
- Session not working
- Check `SECRET_KEY` in environment
- Verify `SessionMiddleware` is configured

