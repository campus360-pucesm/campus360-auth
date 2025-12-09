"""
QR Access endpoints for CAMPUS360
Handles QR code scanning for access control and user credential retrieval
"""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.schemas import ScanRequest, ScanResponse, UserResponse
from app.utils.auth_utils import get_current_user, prisma

router = APIRouter(
    prefix="/qr",
    tags=["QR Access"]
)


@router.get("/me", response_model=UserResponse)
async def get_my_profile(current_user = Depends(get_current_user)):
    """
    Get current user's profile data for QR code generation
    
    This endpoint returns the authenticated user's information
    which can be used by the frontend to generate a digital credential QR code.
    
    **Authentication required**: Bearer token in Authorization header
    
    Returns user data including:
    - User ID
    - Email
    - Full name
    - Role
    - Account creation date
    """
    return current_user


@router.post("/scan", response_model=ScanResponse)
async def scan_location(
    scan_data: ScanRequest,
    current_user = Depends(get_current_user)
):
    """
    Record access to a location via QR code scan
    
    When a user scans a physical QR code at a location (e.g., "LAB-101"),
    this endpoint creates an access log entry in the database.
    
    **Authentication required**: Bearer token in Authorization header
    
    - **location_code**: The code from the scanned QR (e.g., "LAB-101", "AULA-302")
    
    Returns confirmation with:
    - Success message
    - Location code
    - Timestamp of access
    - User information
    """
    # Create access log entry
    access_log = await prisma.accesslog.create(
        data={
            "user_id": current_user.id,
            "location_code": scan_data.location_code,
        }
    )
    
    return {
        "message": "Access recorded successfully",
        "location_code": scan_data.location_code,
        "timestamp": access_log.timestamp,
        "user": current_user
    }


@router.get("/history", response_model=list[dict])
async def get_access_history(
    current_user = Depends(get_current_user),
    limit: int = 10
):
    """
    Get user's access history
    
    Returns the most recent access logs for the authenticated user.
    
    **Authentication required**: Bearer token in Authorization header
    
    - **limit**: Maximum number of records to return (default: 10, max: 100)
    """
    if limit > 100:
        limit = 100
    
    access_logs = await prisma.accesslog.find_many(
        where={"user_id": current_user.id},
        order={"timestamp": "desc"},
        take=limit
    )
    
    return [
        {
            "id": log.id,
            "location_code": log.location_code,
            "timestamp": log.timestamp
        }
        for log in access_logs
    ]
