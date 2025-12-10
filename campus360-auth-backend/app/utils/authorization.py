"""
Authorization utilities for role-based access control
"""
from functools import wraps
from typing import List

from fastapi import HTTPException, status

from app.utils.auth_utils import get_current_user


def require_role(*allowed_roles: str):
    """
    Decorator to require specific roles for endpoint access
    
    Usage:
        @require_role("admin")
        @require_role("admin", "teacher")
    
    Args:
        allowed_roles: Roles that are allowed to access the endpoint
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get current user from dependency injection
            # This assumes get_current_user is already injected
            current_user = None
            for arg in args:
                if hasattr(arg, 'role'):
                    current_user = arg
                    break
            
            if not current_user:
                for value in kwargs.values():
                    if hasattr(value, 'role'):
                        current_user = value
                        break
            
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            if current_user.role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Access denied. Required roles: {', '.join(allowed_roles)}"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def check_role(user, *allowed_roles: str) -> bool:
    """
    Check if user has one of the allowed roles
    
    Args:
        user: User object with role attribute
        allowed_roles: Roles to check against
        
    Returns:
        True if user has allowed role, False otherwise
    """
    return user.role in allowed_roles


def require_admin(user):
    """
    Raise exception if user is not admin
    
    Args:
        user: User object with role attribute
        
    Raises:
        HTTPException: If user is not admin
    """
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )


def require_admin_or_teacher(user):
    """
    Raise exception if user is not admin or teacher
    
    Args:
        user: User object with role attribute
        
    Raises:
        HTTPException: If user is not admin or teacher
    """
    if user.role not in ["admin", "teacher"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin or teacher access required"
        )
