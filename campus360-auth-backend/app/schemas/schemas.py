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


# ==================== Geolocation QR Schemas ====================

class LocationQRCreate(BaseModel):
    """Schema for creating a location QR with geolocation and time constraints"""
    location_code: str = Field(..., description="Unique location code (e.g., 'LAB-101')")
    location_name: Optional[str] = Field(None, description="Descriptive name of the location")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude of the location")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude of the location")
    class_start: datetime = Field(..., description="Class start time")
    class_end: datetime = Field(..., description="Class end time")
    grace_period: int = Field(15, ge=0, le=60, description="Grace period in minutes (default: 15)")


class ScanRequestAdvanced(BaseModel):
    """Schema for QR code scan with geolocation validation"""
    location_id: str = Field(..., description="Location ID from scanned QR")
    user_latitude: float = Field(..., ge=-90, le=90, description="User's current latitude")
    user_longitude: float = Field(..., ge=-180, le=180, description="User's current longitude")


class ScanResponseAdvanced(BaseModel):
    """Schema for advanced scan response with validation status"""
    message: str
    status: str  # ON_TIME, LATE, ABSENT, INVALID_LOCATION, EXPIRED
    location_code: str
    location_name: Optional[str] = None
    distance_meters: float
    timestamp: datetime
    user: UserResponse


class LocationResponse(BaseModel):
    """Schema for location data response"""
    id: str
    location_code: str
    location_name: Optional[str] = None
    latitude: float
    longitude: float
    class_start: datetime
    class_end: datetime
    grace_period: int
    created_by: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class AccessLogResponseAdvanced(BaseModel):
    """Schema for enhanced access log with validation data"""
    id: int
    user_id: str
    location_id: Optional[str] = None
    location_code: str
    timestamp: datetime
    status: Optional[str] = None
    user_latitude: Optional[float] = None
    user_longitude: Optional[float] = None
    distance_meters: Optional[float] = None
    
    class Config:
        from_attributes = True

