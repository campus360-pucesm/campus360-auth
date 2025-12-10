"""
Pydantic schemas for request/response validation
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# ==================== User Schemas ====================

class UserCreate(BaseModel):
    """Schema for creating a new user (admin only)"""
    email: EmailStr
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters")
    full_name: str = Field(..., min_length=2, description="Full name of the user")
    role: str = Field(..., description="User role (admin, teacher, or student)")


class UserUpdate(BaseModel):
    """Schema for updating user information (admin only)"""
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6, description="New password (optional)")
    full_name: Optional[str] = Field(None, min_length=2, description="New full name (optional)")
    role: Optional[str] = Field(None, description="New role (optional)")


class UserLogin(BaseModel):
    """Schema for user login"""
    username: EmailStr  # OAuth2PasswordRequestForm uses 'username' field
    password: str


class UserResponse(BaseModel):
    """Schema for user data response (excludes password)"""
    id: str
    email: str
    full_name: str
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Authentication Schemas ====================

class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for decoded token data"""
    user_id: Optional[str] = None


# ==================== QR Access Schemas ====================

class ScanRequest(BaseModel):
    """Schema for QR code scan request"""
    location_code: str = Field(..., description="Location code from scanned QR (e.g., 'LAB-101')")


class AccessLogResponse(BaseModel):
    """Schema for access log response"""
    id: int
    user_id: str
    location_code: str
    timestamp: datetime
    
    class Config:
        from_attributes = True


class ScanResponse(BaseModel):
    """Schema for scan confirmation response"""
    message: str
    location_code: str
    timestamp: datetime
    user: UserResponse
