"""
QR Access endpoints for CAMPUS360
Handles QR code scanning for access control and user credential retrieval
"""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.schemas import (
    ScanRequest, ScanResponse, UserResponse,
    ScanRequestAdvanced, ScanResponseAdvanced
)
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
            "user_id": log.user_id,
            "location_id": log.location_id,
            "location_code": log.location_code,
            "timestamp": log.timestamp,
            "status": log.status,
            "user_latitude": log.user_latitude,
            "user_longitude": log.user_longitude,
            "distance_meters": log.distance_meters
        }
        for log in access_logs
    ]


@router.post("/scan-advanced", response_model=ScanResponseAdvanced)
async def scan_location_advanced(
    scan_data: ScanRequestAdvanced,
    current_user = Depends(get_current_user)
):
    """
    Scan QR code with geolocation and time validation
    
    **Authentication required**: Bearer token
    
    This endpoint validates:
    - User is within 100m of the location
    - Scan time is within class schedule
    - Determines attendance status (on-time, late, absent)
    
    Returns detailed validation results
    """
    from datetime import datetime, timezone
    from app.utils.geolocation import is_within_radius
    from app.utils.attendance import calculate_attendance_status, get_status_message
    
    try:
        # Get location data
        location = await prisma.location.find_unique(
            where={"id": scan_data.location_id}
        )
        
        if not location:
            raise HTTPException(
                status_code=404,
                detail="Location not found"
            )
        
        # Use timezone-aware datetime
        scan_time = datetime.now(timezone.utc)
        
        # Make sure location times are timezone-aware
        class_start = location.class_start
        class_end = location.class_end
        
        # If times are naive, make them UTC
        if class_start.tzinfo is None:
            class_start = class_start.replace(tzinfo=timezone.utc)
        if class_end.tzinfo is None:
            class_end = class_end.replace(tzinfo=timezone.utc)
        
        # Validate geolocation
        is_valid_location, distance = is_within_radius(
            scan_data.user_latitude,
            scan_data.user_longitude,
            location.latitude,
            location.longitude,
            radius_meters=100
        )
        
        # Calculate attendance status
        status = calculate_attendance_status(
            scan_time=scan_time,
            class_start=class_start,
            class_end=class_end,
            grace_period_minutes=location.grace_period,
            is_location_valid=is_valid_location
        )
        
        # Create access log
        access_log = await prisma.accesslog.create(
            data={
                "user_id": current_user.id,
                "location_id": location.id,
                "location_code": location.location_code,
                "status": status,
                "user_latitude": scan_data.user_latitude,
                "user_longitude": scan_data.user_longitude,
                "distance_meters": distance
            }
        )
        
        return {
            "message": get_status_message(status, distance),
            "status": status,
            "location_code": location.location_code,
            "location_name": location.location_name,
            "distance_meters": round(distance, 2),
            "timestamp": access_log.timestamp,
            "user": current_user
        }
        
    except HTTPException:
        raise
    except Exception as e:
        # Log the full error for debugging
        import traceback
        print(f"Error in scan_location_advanced: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Error processing scan: {str(e)}"
        )

