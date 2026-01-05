"""
Authentication and authorization utilities.

Rebuilt with:
- Deterministic state transitions
- Explicit error handling
- No hidden side effects
"""
import bcrypt
import logging
from typing import Optional, Dict, Tuple
from fastapi import Request
from fastapi.responses import RedirectResponse
from sqlalchemy import func
from sqlalchemy.orm import Session
from models import User
from database import SessionLocal

logger = logging.getLogger(__name__)


# ============================================================================
# Password Utilities
# ============================================================================

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    Returns the hashed password as a string.
    """
    if not password:
        raise ValueError("Password cannot be empty")
    
    # Truncate to 72 bytes to avoid bcrypt errors
    password_bytes = password[:72].encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.
    Returns True if password matches, False otherwise.
    """
    if not plain_password or not hashed_password:
        return False
    
    try:
        password_bytes = plain_password[:72].encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception:
        return False


# ============================================================================
# User Authentication
# ============================================================================

def verify_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Verify user credentials and return the user if valid.
    
    State transitions:
    1. Lookup user by email (case-insensitive)
    2. Check if user exists → return None if not found
    3. Check if user is active → return None if inactive
    4. Verify password → return None if invalid
    5. Return user if all checks pass
    
    Returns:
        User object if credentials are valid, None otherwise
    
    Raises:
        Exception: If database error occurs (logged with context)
    """
    if not email or not password:
        return None
    
    email_clean = email.strip() if email else ""
    
    try:
        # Case-insensitive email lookup
        user = db.query(User).filter(
            func.lower(User.email) == func.lower(email_clean)
        ).first()
        
        if not user:
            return None
        
        if not user.active:
            return None
        
        # Verify password
        if not verify_password(password, user.hashed_password):
            return None
        
        return user
    except Exception as e:
        # Log error with full context for debugging
        import traceback
        error_context = {
            "function": "verify_user",
            "email": email_clean,
            "error_type": type(e).__name__,
            "error_message": str(e),
            "traceback": traceback.format_exc()
        }
        print(f"[AUTH ERROR] {error_context}")
        # Re-raise to allow caller to handle with specific error messages
        raise


# ============================================================================
# Session Management
# ============================================================================

def get_current_user(request: Request) -> Optional[User]:
    """
    Get the current user from the session.
    
    State transitions:
    1. Check session for user_id → return None if missing
    2. Query database for user → return None if not found
    3. Clear session if user doesn't exist (prevent redirect loops)
    4. Return user if found
    
    Side effects:
    - Clears session if user_id exists but user not found in database
    - Creates and closes database session (explicit resource management)
    
    Returns:
        User object if authenticated, None otherwise
    """
    # Check if session exists and has user_id
    if not hasattr(request, 'session'):
        return None
    
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            # User doesn't exist - clear session to prevent redirect loops
            _clear_session_safe(request)
            return None
        
        if not user.active:
            # User is inactive - clear session
            _clear_session_safe(request)
            return None
        
        return user
    except Exception as e:
        # Database error - clear session and return None
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error getting current user: {e}", exc_info=True)
        _clear_session_safe(request)
        return None
    finally:
        db.close()


def set_user_session(request: Request, user: User) -> None:
    """
    Set user session after successful login.
    
    State transition:
    1. Store user_id in session
    
    Preconditions:
    - user must exist and have an id
    
    Returns:
        None on success
    
    Raises:
        ValueError: If user object is invalid (logged with context)
        RuntimeError: If session cannot be set (logged with context)
    """
    if not user:
        error_context = {
            "function": "set_user_session",
            "error_type": "ValueError",
            "error_message": "User object is required",
            "user": None
        }
        print(f"[AUTH ERROR] {error_context}")
        raise ValueError("User object is required")
    
    user_id = getattr(user, 'id', None)
    if not hasattr(user, 'id') or user_id is None:
        error_context = {
            "function": "set_user_session",
            "error_type": "ValueError",
            "error_message": "User object missing id attribute",
            "user_type": str(type(user)),
            "user_id": user_id,
            "user_email": getattr(user, 'email', 'unknown')
        }
        print(f"[AUTH ERROR] {error_context}")
        raise ValueError(f"User object missing id attribute. User type: {type(user)}, User ID: {user_id}")
    
    try:
        request.session["user_id"] = user_id
        # Force session to be saved by marking it as modified
        # This ensures the cookie is set before redirect
        if hasattr(request.session, '_modified'):
            request.session._modified = True
        logger.info(f"[AUTH] Session set for user_id={user_id}, session keys: {list(request.session.keys())}")
    except AttributeError as e:
        error_context = {
            "function": "set_user_session",
            "error_type": "AttributeError",
            "error_message": "Session middleware not configured",
            "user_id": user_id,
            "user_email": getattr(user, 'email', 'unknown'),
            "has_session": hasattr(request, 'session')
        }
        print(f"[AUTH ERROR] {error_context}")
        raise RuntimeError("Session middleware not configured. Please contact support.")
    except Exception as e:
        error_context = {
            "function": "set_user_session",
            "error_type": type(e).__name__,
            "error_message": str(e),
            "user_id": user_id,
            "user_email": getattr(user, 'email', 'unknown')
        }
        print(f"[AUTH ERROR] {error_context}")
        raise RuntimeError(f"Failed to set session: {e}")


def clear_user_session(request: Request) -> None:
    """
    Clear user session on logout.
    
    State transition:
    1. Clear all session data
    """
    _clear_session_safe(request)


def _clear_session_safe(request: Request) -> None:
    """Safely clear session, ignoring any errors."""
    try:
        request.session.clear()
    except Exception:
        pass  # Ignore session errors


# ============================================================================
# Authorization
# ============================================================================

def has_permission(user: Optional[User], permission: str) -> bool:
    """
    Check if user has a specific permission.
    
    State transitions:
    1. Check if user exists → return False if None
    2. Check if user has permissions → return False if None
    3. Parse JSON permissions → return False if invalid
    4. Check permission value → return True/False
    
    Returns:
        True if user has permission, False otherwise
    """
    if not user:
        return False
    
    if not user.permissions:
        return False
    
    try:
        import json
        permissions = json.loads(user.permissions)
        return bool(permissions.get(permission, False))
    except Exception:
        return False


def require_permission(user: Optional[User], permission: str) -> Optional[RedirectResponse]:
    """
    Check if user has permission. Returns redirect if denied.
    
    State transitions:
    1. Check if user exists → redirect if None
    2. Check permission → redirect if denied
    3. Return None if allowed
    
    Returns:
        RedirectResponse if permission denied, None if allowed
    """
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    if not has_permission(user, permission):
        return RedirectResponse(url="/login", status_code=303)
    
    return None


# ============================================================================
# Permission Definitions
# ============================================================================

def get_default_permissions(role: str) -> Dict[str, bool]:
    """
    Get default permissions for a role.
    
    Returns a dictionary of permission names to boolean values.
    """
    if role == "Admin":
        return {
            "view_dashboard": True,
            "view_clients": True,
            "create_clients": True,
            "edit_clients": True,
            "delete_clients": True,
            "view_services": True,
            "create_services": True,
            "edit_services": True,
            "delete_services": True,
            "view_tasks": True,
            "create_tasks": True,
            "edit_tasks": True,
            "delete_tasks": True,
            "view_notes": True,
            "create_notes": True,
            "delete_notes": True,
            "view_own_timesheets": True,
            "view_all_timesheets": True,
            "create_timesheets": True,
            "edit_own_timesheets": True,
            "edit_all_timesheets": True,
            "delete_own_timesheets": True,
            "delete_all_timesheets": True,
            "view_settings": True,
            "manage_users": True,
            "manage_permissions": True,
        }
    elif role == "Manager":
        return {
            "view_dashboard": True,
            "view_clients": True,
            "create_clients": True,
            "edit_clients": True,
            "delete_clients": False,
            "view_services": True,
            "create_services": True,
            "edit_services": True,
            "delete_services": False,
            "view_tasks": True,
            "create_tasks": True,
            "edit_tasks": True,
            "delete_tasks": True,
            "view_notes": True,
            "create_notes": True,
            "delete_notes": True,
            "view_own_timesheets": True,
            "view_all_timesheets": True,
            "create_timesheets": True,
            "edit_own_timesheets": True,
            "edit_all_timesheets": True,
            "delete_own_timesheets": True,
            "delete_all_timesheets": False,
            "view_settings": False,
            "manage_users": False,
            "manage_permissions": False,
        }
    else:  # Staff
        return {
            "view_dashboard": True,
            "view_clients": True,
            "create_clients": False,
            "edit_clients": False,
            "delete_clients": False,
            "view_services": True,
            "create_services": False,
            "edit_services": False,
            "delete_services": False,
            "view_tasks": True,
            "create_tasks": True,
            "edit_tasks": True,
            "delete_tasks": True,
            "view_notes": True,
            "create_notes": True,
            "delete_notes": True,
            "view_own_timesheets": True,
            "view_all_timesheets": False,
            "create_timesheets": True,
            "edit_own_timesheets": True,
            "edit_all_timesheets": False,
            "delete_own_timesheets": True,
            "delete_all_timesheets": False,
            "view_settings": False,
            "manage_users": False,
            "manage_permissions": False,
        }


def can_edit_timesheet(user: Optional[User], staff_member: Optional[User]) -> bool:
    """
    Check if user can edit a timesheet entry.
    
    Rules:
    - Users can always edit their own timesheets
    - Users can edit all timesheets if they have edit_all_timesheets permission
    """
    if not user:
        return False
    
    if not staff_member:
        return has_permission(user, "edit_all_timesheets")
    
    # Can edit own timesheets
    if user.id == staff_member.id:
        return True
    
    # Can edit all if has permission
    return has_permission(user, "edit_all_timesheets")


def can_delete_timesheet(user: Optional[User], staff_member: Optional[User]) -> bool:
    """
    Check if user can delete a timesheet entry.
    
    Rules:
    - Users can always delete their own timesheets
    - Users can delete all timesheets if they have delete_all_timesheets permission
    """
    if not user:
        return False
    
    if not staff_member:
        return has_permission(user, "delete_all_timesheets")
    
    # Can delete own timesheets
    if user.id == staff_member.id:
        return True
    
    # Can delete all if has permission
    return has_permission(user, "delete_all_timesheets")
