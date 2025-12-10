"""
Admin endpoints for user management
Only accessible by users with admin role
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.schemas import UserCreate, UserResponse, UserUpdate
from app.utils.auth_utils import get_current_user, hash_password, prisma
from app.utils.authorization import require_admin

router = APIRouter(
    prefix="/admin/users",
    tags=["Admin - User Management"]
)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    current_user = Depends(get_current_user)
):
    """
    Create a new user (admin, teacher, or student)
    
    **Only accessible by admin users**
    
    - **email**: Valid email address (must be unique)
    - **password**: Password (minimum 6 characters)
    - **full_name**: User's full name
    - **role**: User role (admin, teacher, or student)
    
    Returns the created user data (excluding password)
    """
    # Check if current user is admin
    require_admin(current_user)
    
    # Check if user already exists
    existing_user = await prisma.user.find_unique(where={"email": user_data.email})
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Validate role
    if user_data.role not in ["admin", "teacher", "student"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role. Must be: admin, teacher, or student"
        )
    
    # Hash the password
    hashed_password = hash_password(user_data.password)
    
    # Create new user in database
    new_user = await prisma.user.create(
        data={
            "email": user_data.email,
            "password_hash": hashed_password,
            "full_name": user_data.full_name,
            "role": user_data.role,
        }
    )
    
    return new_user


@router.get("", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    role: Optional[str] = None,
    current_user = Depends(get_current_user)
):
    """
    List all users with optional filtering
    
    **Only accessible by admin users**
    
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    - **role**: Optional filter by role (admin, teacher, student)
    
    Returns list of users (excluding passwords)
    """
    # Check if current user is admin
    require_admin(current_user)
    
    # Build query
    where_clause = {}
    if role:
        if role not in ["admin", "teacher", "student"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid role filter"
            )
        where_clause["role"] = role
    
    # Fetch users
    users = await prisma.user.find_many(
        where=where_clause,
        skip=skip,
        take=limit,
        order={"created_at": "desc"}
    )
    
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    current_user = Depends(get_current_user)
):
    """
    Get details of a specific user
    
    **Only accessible by admin users**
    
    - **user_id**: UUID of the user
    
    Returns user data (excluding password)
    """
    # Check if current user is admin
    require_admin(current_user)
    
    # Fetch user
    user = await prisma.user.find_unique(where={"id": user_id})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    current_user = Depends(get_current_user)
):
    """
    Update user information
    
    **Only accessible by admin users**
    
    - **user_id**: UUID of the user to update
    - **email**: New email (optional)
    - **full_name**: New full name (optional)
    - **role**: New role (optional)
    - **password**: New password (optional)
    
    Returns updated user data (excluding password)
    """
    # Check if current user is admin
    require_admin(current_user)
    
    # Check if user exists
    user = await prisma.user.find_unique(where={"id": user_id})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prepare update data
    update_data = {}
    
    if user_data.email is not None:
        # Check if email is already taken by another user
        existing_user = await prisma.user.find_unique(where={"email": user_data.email})
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )
        update_data["email"] = user_data.email
    
    if user_data.full_name is not None:
        update_data["full_name"] = user_data.full_name
    
    if user_data.role is not None:
        if user_data.role not in ["admin", "teacher", "student"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid role"
            )
        update_data["role"] = user_data.role
    
    if user_data.password is not None:
        update_data["password_hash"] = hash_password(user_data.password)
    
    # Update user
    updated_user = await prisma.user.update(
        where={"id": user_id},
        data=update_data
    )
    
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    current_user = Depends(get_current_user)
):
    """
    Delete a user
    
    **Only accessible by admin users**
    
    - **user_id**: UUID of the user to delete
    
    Returns no content on success
    """
    # Check if current user is admin
    require_admin(current_user)
    
    # Prevent admin from deleting themselves
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    # Check if user exists
    user = await prisma.user.find_unique(where={"id": user_id})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Delete user (cascade will delete related access logs)
    await prisma.user.delete(where={"id": user_id})
    
    return None
