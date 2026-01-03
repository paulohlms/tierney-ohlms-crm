# Diagnostic: Login 500 Internal Server Error

## Failure Analysis

### Request Flow
```
POST /login
  ↓
1. Extract form data: email, password
  ↓
2. Import locally: `from auth import verify_user, set_user_session`
  ↓
3. Bootstrap users if none exist
  ↓
4. Call: `verify_user(db, email, password)`
  ↓
5. If user found: Call `set_user_session(request, user)`
  ↓
6. Redirect to /dashboard
```

## Potential Failure Points

### Failure Point 1: Import Error
**Location:** `main.py:280`
```python
from auth import verify_user, set_user_session
```

**Possible Error:**
- `set_user_session` not found in `auth` module
- Circular import issue
- Module not properly loaded

**Runtime Values:**
- `auth` module: Should be loaded
- `verify_user`: Function exists at `auth.py:58`
- `set_user_session`: Function exists at `auth.py:147`

### Failure Point 2: verify_user() Call
**Location:** `main.py:292`
```python
user = verify_user(db, email, password)
```

**Function Signature:** `verify_user(db: Session, email: str, password: str) -> Optional[User]`

**Possible Errors:**
- `db` is None or invalid Session object
- `email` or `password` is None/empty
- Database query fails in `verify_user()`
- `User` model import issue

**Runtime Values to Check:**
- `db`: Should be SQLAlchemy Session from `Depends(get_db)`
- `email`: String from form data
- `password`: String from form data
- `User` model: Should be importable from `models`

### Failure Point 3: set_user_session() Call
**Location:** `main.py:303`
```python
set_user_session(request, user)
```

**Function Signature:** `set_user_session(request: Request, user: User) -> None`

**Possible Errors:**
- `user` is None (shouldn't happen, checked above)
- `user.id` is None
- `request.session` is not available
- `ValueError` raised if user is invalid

**Runtime Values to Check:**
- `user`: Should be User object (not None)
- `user.id`: Should be integer
- `request.session`: Should be dict-like object

### Failure Point 4: Database Query in verify_user()
**Location:** `auth.py:77`
```python
user = db.query(User).filter(
    func.lower(User.email) == func.lower(email.strip())
).first()
```

**Possible Errors:**
- `User` model not imported correctly
- `db` session is invalid
- Database connection error
- `users` table doesn't exist
- `users` table missing columns

**Runtime Values to Check:**
- `db`: Session object
- `User`: Model class from `models`
- `email.strip()`: Processed email string

## Exact Error Stack Trace Location

The error will appear in one of these locations:

### If Import Error:
```python
Traceback (most recent call last):
  File "main.py", line 280, in login
    from auth import verify_user, set_user_session
ImportError: cannot import name 'set_user_session' from 'auth'
```

### If verify_user() Fails:
```python
Traceback (most recent call last):
  File "main.py", line 292, in login
    user = verify_user(db, email, password)
  File "auth.py", line 77, in verify_user
    user = db.query(User).filter(...).first()
sqlalchemy.exc.ProgrammingError: ...
```

### If set_user_session() Fails:
```python
Traceback (most recent call last):
  File "main.py", line 303, in login
    set_user_session(request, user)
  File "auth.py", line 158, in set_user_session
    raise ValueError("Invalid user object")
ValueError: Invalid user object
```

## Diagnostic Steps

### Step 1: Check Server Logs
Look for the exact stack trace in Render logs. The error will show:
- The failing line number
- The exception type
- The exception message

### Step 2: Check Function Existence
Verify these functions exist in `auth.py`:
- `verify_user` at line 58
- `set_user_session` at line 147
- `clear_user_session` at line 163

### Step 3: Check Import Chain
Verify imports work:
```python
# In Python shell or test:
from auth import verify_user, set_user_session
# Should not raise ImportError
```

### Step 4: Check Database State
Verify:
- `users` table exists
- `users` table has required columns
- Database connection works

## Most Likely Failure

Based on the rebuild, the most likely failure is:

**Import Error:** `set_user_session` not found
- The function exists in `auth.py` at line 147
- But it might not be exported or there's a syntax error preventing the module from loading

**OR**

**Database Error in verify_user():**
- The `users` table might be missing columns
- The database query fails with `UndefinedColumn` error
- This would happen at `auth.py:77`

## Required Information to Diagnose

To identify the exact failure, we need:

1. **Full stack trace from Render logs**
   - Shows exact line number
   - Shows exception type and message
   - Shows the call chain

2. **Runtime values at failure:**
   - `email` value
   - `password` value (length only, not actual password)
   - `db` session state
   - `user` object state (if it gets that far)

3. **Import verification:**
   - Can `from auth import set_user_session` succeed?
   - Are there any syntax errors in `auth.py`?

## Next Steps

1. Check Render deployment logs for the exact stack trace
2. Verify `auth.py` has no syntax errors
3. Test imports locally if possible
4. Check database schema matches model expectations

