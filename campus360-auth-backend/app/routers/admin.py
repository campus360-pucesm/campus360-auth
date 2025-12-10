"""
Admin endpoints for CAMPUS360
Handles administrative tasks like generating location QR codes
"""
from io import BytesIO

import qrcode
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.utils.auth_utils import get_current_user
from app.utils.authorization import require_admin_or_teacher

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
