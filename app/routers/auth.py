"""
Authentication endpoints for CAMPUS360
Handles user registration and login with JWT token generation
"""
from datetime import timedelta

from fastapi import APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends

from app.config import settings
from app.schemas.schemas import Token, UserRegister, UserResponse
from app.utils.auth_utils import (
    create_access_token,
    hash_password,
    prisma,
    verify_password,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):
    """
    Register a new user
    
    - **email**: Valid email address (must be unique)
    - **password**: Password (minimum 6 characters)
    - **full_name**: User's full name
    - **role**: User role (default: student)
    
    Returns the created user data (excluding password)
    """
    # Check if user already exists
    existing_user = await prisma.user.find_unique(where={"email": user_data.email})
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
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


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login with email and password to receive JWT access token
    
    - **username**: User's email address
    - **password**: User's password
    
    Returns JWT access token for authenticated requests
    """
    # Find user by email
    user = await prisma.user.find_unique(where={"email": form_data.username})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
