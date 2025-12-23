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

