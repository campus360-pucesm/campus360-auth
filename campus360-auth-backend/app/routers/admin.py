"""
Admin endpoints for CAMPUS360
Handles administrative tasks like generating location QR codes
"""
from io import BytesIO

import qrcode
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.utils.auth_utils import get_current_user, prisma
from app.utils.authorization import require_admin_or_teacher
from app.schemas.schemas import LocationQRCreate, LocationResponse

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


class LocationQRRequest(BaseModel):
    """Schema for location QR generation request"""
    location_code: str
    location_name: str = ""


@router.post("/qr/generate-location")
async def generate_location_qr(
    request: LocationQRRequest,
    current_user = Depends(get_current_user)
):
    """
    Generate a QR code image for a physical location
    
    **Accessible by admin and teacher roles**
    
    This endpoint generates a QR code that can be printed and placed
    at physical locations (labs, classrooms, etc.). When students scan
    this QR, they'll send the location_code to POST /qr/scan.
    
    - **location_code**: Unique code for the location (e.g., "LAB-101", "AULA-302")
    - **location_name**: Optional friendly name for the location
    
    Returns a PNG image of the QR code
    """
    # Check if user is admin or teacher
    require_admin_or_teacher(current_user)
    
    try:
        # Create QR code instance
        qr = qrcode.QRCode(
            version=1,  # Size of QR code (1-40)
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        # Add data to QR code (just the location code)
        qr.add_data(request.location_code)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to BytesIO buffer
        buf = BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        
        # Return as streaming response
        return StreamingResponse(
            buf,
            media_type="image/png",
            headers={
                "Content-Disposition": f"attachment; filename={request.location_code}.png"
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating QR code: {str(e)}"
        )


@router.get("/qr/generate-credential/{user_id}")
async def generate_user_credential_qr(user_id: str):
    """
    Generate a QR code for a user's digital credential
    
    This generates a QR code containing the user's ID that can be
    used as a digital credential/ID card.
    
    - **user_id**: UUID of the user
    
    Returns a PNG image of the QR code
    """
    try:
        # Create QR code instance
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        
        # Add user ID to QR code
        qr.add_data(user_id)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to BytesIO buffer
        buf = BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        
        # Return as streaming response
        return StreamingResponse(
            buf,
            media_type="image/png",
            headers={
                "Content-Disposition": f"attachment; filename=credential_{user_id}.png"
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating QR code: {str(e)}"
        )


@router.post("/qr/generate-location-advanced", response_model=LocationResponse)
async def generate_location_qr_advanced(
    request: LocationQRCreate,
    current_user = Depends(get_current_user)
):
    """
    Generate a QR code with geolocation and time validation
    
    **Accessible by admin and teacher roles**
    
    This endpoint creates a location record with coordinates and class schedule.
    Returns the location data including ID which can be used to generate QR image.
    """
    require_admin_or_teacher(current_user)
    
    try:
        # Validate that class_end is after class_start
        if request.class_end <= request.class_start:
            raise HTTPException(
                status_code=400,
                detail="class_end must be after class_start"
            )
        
        # Create location record in database
        location = await prisma.location.create(
            data={
                "location_code": request.location_code,
                "location_name": request.location_name,
                "latitude": request.latitude,
                "longitude": request.longitude,
                "class_start": request.class_start,
                "class_end": request.class_end,
                "grace_period": request.grace_period,
                "created_by": current_user.id
            }
        )
        
        return location
        
    except Exception as e:
        if "unique" in str(e).lower():
            raise HTTPException(
                status_code=400,
                detail=f"Location code '{request.location_code}' already exists"
            )
        raise HTTPException(
            status_code=500,
            detail=f"Error creating location: {str(e)}"
        )


@router.get("/qr/location/{location_id}/image")
async def get_location_qr_image(
    location_id: str,
    current_user = Depends(get_current_user)
):
    """
    Get QR code image for a specific location
    
    **Accessible by admin and teacher roles**
    
    Returns a PNG image of the QR code containing the location ID
    """
    require_admin_or_teacher(current_user)
    
    try:
        # Verify location exists
        location = await prisma.location.find_unique(
            where={"id": location_id}
        )
        
        if not location:
            raise HTTPException(
                status_code=404,
                detail="Location not found"
            )
        
        # Create QR code with location ID
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        qr.add_data(location_id)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        buf = BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        
        return StreamingResponse(
            buf,
            media_type="image/png",
            headers={
                "Content-Disposition": f"attachment; filename={location.location_code}.png"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating QR image: {str(e)}"
        )
