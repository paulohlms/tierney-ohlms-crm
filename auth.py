"""
Authentication and authorization utilities.
"""
import bcrypt
from typing import Optional, Dict
from fastapi import Request
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
    """
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        return user
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


def require_permission(permission: str):
    """
    Decorator to require a permission for a route.
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
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    
    if not user.active:
        return None
    
    if verify_password(password, user.hashed_password):
        return user
    
    return None


def get_default_permissions(role: str) -> Dict[str, bool]:
    """
    Get default permissions for a role.
    """
    if role == "Admin":
        return {
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

