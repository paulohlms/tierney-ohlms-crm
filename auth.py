"""
Authentication and authorization utilities.
"""
import bcrypt
from typing import Optional, Dict
from fastapi import Request
from sqlalchemy import func
from models import User
from database import SessionLocal


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    Truncates password to 72 bytes (bcrypt limit) to avoid errors.
    """
    # Truncate to 72 bytes to avoid bcrypt errors
    password_bytes = password[:72].encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.
    """
    try:
        password_bytes = plain_password[:72].encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception:
        return False


def get_current_user(request: Request) -> Optional[User]:
    """
    Get the current user from the session.
    Clears the session if the user doesn't exist in the database or if there's an error.
<<<<<<< HEAD
    Always returns None if user doesn't exist or there's an error.
=======
>>>>>>> 6629e0d10665c3ac17c6ce3f04ff3cc905866943
    """
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            # User doesn't exist - clear the session to prevent redirect loops
            try:
                request.session.clear()
            except:
                pass  # Ignore session errors
<<<<<<< HEAD
            return None  # Explicitly return None
=======
>>>>>>> 6629e0d10665c3ac17c6ce3f04ff3cc905866943
        return user
    except Exception as e:
        # If there's any error querying the database, clear the session to prevent loops
        print(f"Error getting current user: {e}")
        try:
            request.session.clear()
        except:
            pass
        return None
    finally:
        db.close()


def has_permission(user: Optional[User], permission: str) -> bool:
    """
    Check if user has a specific permission.
    """
    if not user:
        return False
    
    if not user.permissions:
        return False
    
    import json
    try:
        permissions = json.loads(user.permissions)
        return permissions.get(permission, False)
    except:
        return False


def require_permission(user: Optional[User], permission: str):
    """
    Check if user has permission. Redirects to login if not authenticated or lacks permission.
    Can be used as a function call: require_permission(current_user, "view_clients")
    Returns RedirectResponse if permission denied, None if allowed.
    """
    from fastapi.responses import RedirectResponse
    
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    if not has_permission(user, permission):
        return RedirectResponse(url="/login", status_code=303)
    
    return None


def require_permission_decorator(permission: str):
    """
    Decorator to require a permission for a route.
    Usage: @require_permission_decorator("view_clients")
    """
    def decorator(func):
        async def wrapper(request: Request, *args, **kwargs):
            user = get_current_user(request)
            if not user or not has_permission(user, permission):
                from fastapi.responses import RedirectResponse
                return RedirectResponse(url="/login", status_code=303)
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator


def verify_user(db, email: str, password: str) -> Optional[User]:
    """
    Verify user credentials and return the user if valid.
    Email comparison is case-insensitive.
    """
    # Case-insensitive email lookup
    user = db.query(User).filter(func.lower(User.email) == func.lower(email)).first()
    if not user:
        print(f"User not found for email: {email}")
        return None
    
    if not user.active:
        print(f"User {email} is not active")
        return None
    
    # Debug: Check if password verification works
    password_valid = verify_password(password, user.hashed_password)
    if not password_valid:
        print(f"Password verification failed for {email}")
        # Try to verify the hash format
        try:
            test_hash = hash_password(password)
            print(f"Test hash generated, but verification still failed")
        except Exception as e:
            print(f"Error testing password hash: {e}")
        return None
    
    print(f"Login successful for {email}")
    return user


def get_default_permissions(role: str) -> Dict[str, bool]:
    """
    Get default permissions for a role.
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
    Users can edit their own timesheets, or if they have edit_all_timesheets permission.
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
    Users can delete their own timesheets, or if they have delete_all_timesheets permission.
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

