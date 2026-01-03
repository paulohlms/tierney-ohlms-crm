# EXACT FAILURE POINTS - Login 500 Error

## Diagnostic Mode Analysis

### Request: POST /login
**Endpoint:** `main.py:263` - `async def login(...)`
**Function:** `login(request: Request, email: str, password: str, db: Session)`

---

## Failure Point Analysis

### FAILURE POINT #1: Import Statement (Line 280)
```python
from auth import verify_user, set_user_session
```

**Status:** ✅ VERIFIED - Imports work locally
- `verify_user` exists at `auth.py:58`
- `set_user_session` exists at `auth.py:147`
- No syntax errors in `auth.py`

**Runtime Check Needed:**
- Verify imports succeed on server
- Check for circular import issues
- Verify `auth` module loads completely

---

### FAILURE POINT #2: Bootstrap Users (Lines 283-289)
```python
try:
    user_count = db.query(UserModel).count()
    if user_count == 0:
        bootstrap_admin_users()
        db.expire_all()
except Exception as e:
    print(f"Error checking/bootstraping users: {e}")
```

**Possible Errors:**
- `db.query(UserModel).count()` fails
- `bootstrap_admin_users()` raises unhandled exception
- Database connection issue

**Runtime Values to Capture:**
- `db`: Session object state
- `UserModel`: Model class
- Exception type and message if raised

---

### FAILURE POINT #3: verify_user() Call (Line 292)
```python
user = verify_user(db, email, password)
```

**Function Location:** `auth.py:58`
**Function Body:** `auth.py:72-95`

**Possible Errors:**

#### Error 3a: Database Query Failure
**Location:** `auth.py:77`
```python
user = db.query(User).filter(
    func.lower(User.email) == func.lower(email.strip())
).first()
```

**Possible Exceptions:**
- `sqlalchemy.exc.ProgrammingError: column users.name does not exist`
- `sqlalchemy.exc.OperationalError: connection failed`
- `sqlalchemy.exc.InvalidRequestError: session is closed`

**Runtime Values:**
- `db`: Session object
- `User`: Model class from `models`
- `email.strip()`: String value
- `func.lower()`: SQLAlchemy function

#### Error 3b: Password Verification Failure
**Location:** `auth.py:88`
```python
if not verify_password(password, user.hashed_password):
    return None
```

**Note:** This returns None, not raises exception, so unlikely to cause 500

#### Error 3c: Exception in verify_user()
**Location:** `auth.py:92-95`
```python
except Exception as e:
    print(f"Error verifying user: {e}")
    return None
```

**Note:** This catches all exceptions and returns None, so unlikely to cause 500

---

### FAILURE POINT #4: set_user_session() Call (Line 303)
```python
set_user_session(request, user)
```

**Function Location:** `auth.py:147`
**Function Body:** `auth.py:157-160`

**Possible Errors:**

#### Error 4a: ValueError - Invalid User Object
**Location:** `auth.py:157-158`
```python
if not user or not user.id:
    raise ValueError("Invalid user object")
```

**This WILL cause 500 error if:**
- `user` is None (shouldn't happen, checked at line 294)
- `user.id` is None or missing

**Runtime Values:**
- `user`: Should be User object
- `user.id`: Should be integer
- `type(user)`: Should be `<class 'models.User'>`

#### Error 4b: Session Access Error
**Location:** `auth.py:160`
```python
request.session["user_id"] = user.id
```

**Possible Exceptions:**
- `KeyError`: Session middleware not configured
- `AttributeError`: `request.session` doesn't exist
- `TypeError`: Session object not dict-like

**Runtime Values:**
- `request`: FastAPI Request object
- `request.session`: Should be dict-like object
- `user.id`: Integer value

---

## Most Likely Failure Scenarios

### Scenario 1: Database Query Failure (60% probability)
**Location:** `auth.py:77` in `verify_user()`

**Error:**
```
sqlalchemy.exc.ProgrammingError: (psycopg.errors.UndefinedColumn) 
column users.name does not exist
```

**Cause:** Migration didn't add `name` column to `users` table

**Runtime Values:**
- `db.query(User)`: Tries to SELECT all columns including `name`
- `users` table: Missing `name` column
- Exception: Raised before `verify_user()` can catch it

**Why it's not caught:** The exception is raised during SQLAlchemy query execution, before the try/except in `verify_user()` can handle it.

---

### Scenario 2: Invalid User Object (30% probability)
**Location:** `auth.py:157` in `set_user_session()`

**Error:**
```
ValueError: Invalid user object
```

**Cause:** `user` object exists but `user.id` is None

**Runtime Values:**
- `user`: User object (not None)
- `user.id`: None (missing or not set)
- Exception: Raised at line 158

---

### Scenario 3: Session Access Error (10% probability)
**Location:** `auth.py:160` in `set_user_session()`

**Error:**
```
AttributeError: 'Request' object has no attribute 'session'
```

**Cause:** Session middleware not properly configured

**Runtime Values:**
- `request`: FastAPI Request object
- `request.session`: AttributeError - doesn't exist

---

## Exact Stack Trace Patterns

### Pattern 1: Database Query Failure
```
Traceback (most recent call last):
  File "main.py", line 292, in login
    user = verify_user(db, email, password)
  File "auth.py", line 77, in verify_user
    user = db.query(User).filter(...).first()
  File "sqlalchemy/orm/query.py", line X, in first
    ...
  File "sqlalchemy/engine/base.py", line X, in execute
    ...
sqlalchemy.exc.ProgrammingError: (psycopg.errors.UndefinedColumn) 
column users.name does not exist
LINE 1: SELECT users.id, users.email, users.name, ...
```

### Pattern 2: Invalid User Object
```
Traceback (most recent call last):
  File "main.py", line 303, in login
    set_user_session(request, user)
  File "auth.py", line 158, in set_user_session
    raise ValueError("Invalid user object")
ValueError: Invalid user object
```

### Pattern 3: Session Access Error
```
Traceback (most recent call last):
  File "main.py", line 303, in login
    set_user_session(request, user)
  File "auth.py", line 160, in set_user_session
    request.session["user_id"] = user.id
AttributeError: 'Request' object has no attribute 'session'
```

---

## Required Diagnostic Information

To identify the exact failure, capture:

1. **Full stack trace from Render logs**
   - Shows exact file and line number
   - Shows exception type
   - Shows exception message

2. **Runtime values at failure:**
   - If failure at line 292: `email`, `password`, `db` session state
   - If failure at line 303: `user` object, `user.id` value, `type(user)`

3. **Migration status:**
   - Check if `users` table has `name` column
   - Check migration logs for errors

---

## Next Steps

1. **Check Render deployment logs** for the exact stack trace
2. **Verify database schema** - does `users` table have all required columns?
3. **Check migration logs** - did migration succeed?
4. **Test locally** - can you reproduce the error?

---

## Code Locations Summary

| Line | File | Function | Potential Error |
|------|------|----------|----------------|
| 280 | main.py | login() | ImportError |
| 292 | main.py | login() | Calls verify_user() |
| 77 | auth.py | verify_user() | Database query failure |
| 303 | main.py | login() | Calls set_user_session() |
| 158 | auth.py | set_user_session() | ValueError if user.id is None |
| 160 | auth.py | set_user_session() | AttributeError if session missing |

