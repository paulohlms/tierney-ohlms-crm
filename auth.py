"""
User authentication and permission system.

Uses database-backed users with role-based permissions.
"""
from fastapi import Request, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import json
from typing import Optional, Dict

from models import User

# Password hashing context
try:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
except Exception:
    pwd_context = CryptContext(schemes=["bcrypt"])


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    import bcrypt as bcrypt_lib
    
    # Python 3.14 compatibility: use bcrypt directly instead of passlib
    # Truncate to 72 bytes (bcrypt limit) if needed
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    # Generate salt and hash
    salt = bcrypt_lib.gensalt()
    hashed = bcrypt_lib.hashpw(password_bytes, salt)
    
    # Return as string (passlib format: $2b$...)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    import bcrypt as bcrypt_lib
    
    try:
        # Try direct bcrypt first (Python 3.14 compatible)
        password_bytes = plain_password.encode('utf-8')
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
        hash_bytes = hashed_password.encode('utf-8')
        return bcrypt_lib.checkpw(password_bytes, hash_bytes)
    except Exception:
        # Fallback to passlib if bcrypt fails
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception:
            return False


def verify_user(db: Session, email: str, password: str) -> Optional[Dict]:
    """
    Verify user credentials and return user info if valid.
    Returns None if invalid.
    """
    try:
        user = db.query(User).filter(User.email == email, User.active == True).first()
    except Exception as e:
        # Table might not exist yet - will be created by Base.metadata.create_all
        print(f"Error querying users table: {e}")
        return None
    
    if not user:
        return None
    
    try:
        if not verify_password(password, user.hashed_password):
            return None
    except Exception as e:
        print(f"Error verifying password: {e}")
        return None
    
    # Parse permissions JSON
    permissions = {}
    if user.permissions:
        try:
            permissions = json.loads(user.permissions)
        except:
            permissions = {}
    
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "role": user.role,
        "permissions": permissions
    }


def get_current_user(request: Request) -> Optional[Dict]:
    """
    Get current user from session.
    Returns user dict if authenticated, None otherwise.
    """
    return request.session.get("user")


def get_user_permissions(user: Optional[Dict]) -> Dict[str, bool]:
    """
    Get user permissions dictionary.
    Returns empty dict if no user or no permissions.
    """
    if not user or "permissions" not in user:
        return {}
    return user.get("permissions", {})


def has_permission(user: Optional[Dict], permission: str) -> bool:
    """
    Check if user has a specific permission.
    Admins have all permissions by default.
    """
    if not user:
        return False
    
    # Admins have all permissions
    if user.get("role") == "Admin":
        return True
    
    permissions = get_user_permissions(user)
    return permissions.get(permission, False)


def require_permission(user: Optional[Dict], permission: str):
    """
    Require a permission or raise HTTPException.
    Use in routes to enforce permissions.
    """
    if not has_permission(user, permission):
        raise HTTPException(
            status_code=403,
            detail=f"Permission denied: {permission}"
        )


def get_default_permissions(role: str = "Staff") -> Dict[str, bool]:
    """
    Get default permissions for a role.
    """
    defaults = {
        "view_own_timesheets": True,
        "create_timesheets": True,
        "edit_own_timesheets": True,
        "delete_own_timesheets": True,
    }
    
    if role == "Admin":
        # Admins get all permissions
        return {
            "view_dashboard": True,
            "view_clients": True,
            "create_clients": True,
            "edit_clients": True,
            "delete_clients": True,
            "export_clients": True,
            "create_contacts": True,
            "delete_contacts": True,
            "create_services": True,
            "edit_services": True,
            "delete_services": True,
            "create_tasks": True,
            "edit_tasks": True,
            "delete_tasks": True,
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
    
    return defaults


def can_edit_timesheet(user: Optional[Dict], timesheet_staff_member: str) -> bool:
    """
    Check if user can edit a specific timesheet.
    Users can edit their own, or if they have edit_all_timesheets permission.
    """
    if not user:
        return False
    
    if user.get("role") == "Admin":
        return True
    
    if has_permission(user, "edit_all_timesheets"):
        return True
    
    if has_permission(user, "edit_own_timesheets") and user.get("name") == timesheet_staff_member:
        return True
    
    return False


def can_delete_timesheet(user: Optional[Dict], timesheet_staff_member: str) -> bool:
    """
    Check if user can delete a specific timesheet.
    Users can delete their own, or if they have delete_all_timesheets permission.
    """
    if not user:
        return False
    
    if user.get("role") == "Admin":
        return True
    
    if has_permission(user, "delete_all_timesheets"):
        return True
    
    if has_permission(user, "delete_own_timesheets") and user.get("name") == timesheet_staff_member:
        return True
    
    return False
