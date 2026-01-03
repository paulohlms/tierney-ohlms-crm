# Debugging Dashboard Endpoint - Complete Guide

## Quick Test Commands

### Python Requests Script (Recommended)
```bash
python test_dashboard_endpoint.py
```

### cURL Command (Alternative)
```bash
# Windows (PowerShell)
bash test_dashboard_curl.sh

# Or manual curl:
curl -c cookies.txt -b cookies.txt -X POST -d "email=admin@tierneyohlms.com" -d "password=ChangeMe123!" http://localhost:8000/login
curl -b cookies.txt http://localhost:8000/dashboard
```

## VS Code Debugger Setup

### 1. Configuration File
The `.vscode/launch.json` file includes three debug configurations:

#### Configuration 1: FastAPI Server
- **Name:** "Python: FastAPI (uvicorn)"
- **Purpose:** Debug the FastAPI server while it's running
- **How to use:**
  1. Set breakpoints in `main.py` (e.g., in the `/dashboard` route)
  2. Start debugging (F5)
  3. Server will start with debugger attached
  4. Make requests to trigger breakpoints

#### Configuration 2: Test Script
- **Name:** "Python: Test Dashboard Endpoint"
- **Purpose:** Debug the test script itself
- **How to use:**
  1. Set breakpoints in `test_dashboard_endpoint.py`
  2. Select this configuration
  3. Start debugging (F5)

#### Configuration 3: Current File
- **Name:** "Python: Current File"
- **Purpose:** Debug any Python file you have open
- **How to use:**
  1. Open any Python file
  2. Set breakpoints
  3. Start debugging (F5)

### 2. Key Breakpoints to Set

#### In `main.py` - Dashboard Route
```python
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    # SET BREAKPOINT HERE
    current_user = get_current_user(request)
    # ... rest of function
```

#### In `main.py` - Template Rendering
```python
return templates.TemplateResponse(
    "dashboard.html",  # SET BREAKPOINT HERE
    {
        "request": request,
        # ... template variables
    }
)
```

#### In `auth.py` - Session Handling
```python
def get_current_user(request: Request) -> Optional[User]:
    # SET BREAKPOINT HERE
    user_id = request.session.get("user_id")
    # ... rest of function
```

### 3. Debugging Steps

#### Step 1: Start Server with Debugger
1. Open VS Code
2. Go to Run and Debug (Ctrl+Shift+D)
3. Select "Python: FastAPI (uvicorn)"
4. Press F5 or click "Start Debugging"
5. Server starts on `http://localhost:8000`

#### Step 2: Set Breakpoints
1. Open `main.py`
2. Find the `/dashboard` route (around line 1330)
3. Click in the gutter to set a breakpoint (red dot)
4. Set breakpoints at:
   - Line with `current_user = get_current_user(request)`
   - Line with `templates.TemplateResponse(...)`

#### Step 3: Trigger the Request
**Option A: Use Test Script**
```bash
# In a separate terminal
python test_dashboard_endpoint.py
```

**Option B: Use Browser**
1. Open browser to `http://localhost:8000/login`
2. Login with: `admin@tierneyohlms.com` / `ChangeMe123!`
3. Navigate to dashboard

**Option C: Use cURL**
```bash
curl -c cookies.txt -b cookies.txt -X POST -d "email=admin@tierneyohlms.com" -d "password=ChangeMe123!" http://localhost:8000/login
curl -b cookies.txt http://localhost:8000/dashboard
```

#### Step 4: Inspect Variables
When breakpoint hits:
- **Variables Panel:** See all local variables
- **Watch Panel:** Add expressions to watch
- **Call Stack:** See function call chain
- **Debug Console:** Execute Python expressions

**Key Variables to Inspect:**
- `current_user` - Should be a User object, not None
- `request.session` - Should contain `{"user_id": <number>}`
- `all_clients` - Should be a list
- Template variables passed to `TemplateResponse`

#### Step 5: Step Through Code
- **F10** - Step Over (next line)
- **F11** - Step Into (enter function)
- **Shift+F11** - Step Out (exit function)
- **F5** - Continue (run to next breakpoint)

### 4. Common Issues and Debug Steps

#### Issue: "UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff"

**Debug Steps:**
1. Set breakpoint at `templates.TemplateResponse(...)`
2. When breakpoint hits, check:
   ```python
   # In Debug Console:
   import os
   template_path = "templates/dashboard.html"
   with open(template_path, 'rb') as f:
       content = f.read()
   print(f"Has BOM: {content.startswith(b'\\xef\\xbb\\xbf')}")
   print(f"Has FF: {b'\\xff' in content[:100]}")
   print(f"First 50 bytes: {content[:50]}")
   ```

3. **Fix:**
   ```bash
   python fix_all_templates_encoding.py
   ```

#### Issue: "Redirected to /login" (Session not working)

**Debug Steps:**
1. Set breakpoint in `get_current_user()` in `auth.py`
2. Check `request.session`:
   ```python
   # In Debug Console:
   print(request.session)
   print(request.session.get("user_id"))
   ```

3. **Check:**
   - Is `SECRET_KEY` set correctly?
   - Is `SessionMiddleware` added to app?
   - Are cookies being sent in requests?

#### Issue: "Internal Server Error (500)"

**Debug Steps:**
1. Check server logs in VS Code Debug Console
2. Look for full traceback
3. Set breakpoint at start of `/dashboard` route
4. Step through each database query
5. Check for:
   - Database connection errors
   - Missing columns
   - Transaction errors

#### Issue: "Template not found"

**Debug Steps:**
1. Check template path:
   ```python
   # In Debug Console:
   import os
   print(os.path.exists("templates/dashboard.html"))
   print(os.listdir("templates"))
   ```

2. Check Jinja2 environment:
   ```python
   # In Debug Console:
   print(templates.env.loader.searchpath)
   ```

### 5. Advanced Debugging

#### Watch Expressions
Add these to the Watch panel:
- `request.session.get("user_id")`
- `current_user.id if current_user else None`
- `len(all_clients) if 'all_clients' in locals() else 'N/A'`
- `type(templates).__name__`

#### Conditional Breakpoints
Right-click on breakpoint → Edit Breakpoint → Add condition:
- `current_user is None` - Only break if user not authenticated
- `len(all_clients) == 0` - Only break if no clients
- `'error' in str(e).lower()` - Only break on errors

#### Logpoints
Right-click on breakpoint → Add Logpoint:
- Message: `User ID: {request.session.get('user_id')}`
- This logs without stopping execution

### 6. Debugging Template Rendering

If template rendering fails:

1. **Check template file encoding:**
   ```python
   # In Debug Console at TemplateResponse breakpoint:
   template_file = "templates/dashboard.html"
   with open(template_file, 'rb') as f:
       content = f.read()
   try:
       text = content.decode('utf-8')
       print("Template is valid UTF-8")
   except UnicodeDecodeError as e:
       print(f"Template encoding error: {e}")
   ```

2. **Check Jinja2 environment:**
   ```python
   # In Debug Console:
   print(templates.env.auto_reload)
   print(templates.env.loader)
   ```

3. **Try rendering manually:**
   ```python
   # In Debug Console:
   template = templates.env.get_template("dashboard.html")
   # This will fail if template has encoding issues
   ```

### 7. Quick Debug Checklist

When dashboard fails, check in this order:

- [ ] Server is running (`uvicorn main:app --reload`)
- [ ] Login works (test with `test_dashboard_endpoint.py`)
- [ ] Session cookie is set (check browser DevTools → Application → Cookies)
- [ ] `current_user` is not None (set breakpoint in dashboard route)
- [ ] Template files are UTF-8 (run `python fix_all_templates_encoding.py`)
- [ ] Database connection works (check server logs)
- [ ] No encoding errors in server logs
- [ ] Template extends base.html correctly

### 8. Example Debug Session

```
1. Start debugger (F5) → Server starts
2. Set breakpoint at line 1330 in main.py (dashboard route)
3. Run: python test_dashboard_endpoint.py
4. Breakpoint hits → Inspect:
   - request.session = {'user_id': 1}
   - current_user = <User object>
5. Step through (F10) to template rendering
6. Check template variables in Variables panel
7. Continue (F5) → Request completes
8. Check test script output for success/failure
```

## Troubleshooting

If debugger doesn't work:
1. Install Python extension in VS Code
2. Check Python interpreter: `Ctrl+Shift+P` → "Python: Select Interpreter"
3. Verify `debugpy` is installed: `pip install debugpy`
4. Check `.vscode/launch.json` syntax is valid JSON

