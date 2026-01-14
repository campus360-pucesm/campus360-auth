"""
Attendance validation utilities for time-based QR code scanning
Determines attendance status based on scan time relative to class schedule
"""

from datetime import datetime, timedelta
from enum import Enum


class AttendanceStatus(str, Enum):
    """Possible attendance statuses"""
    ON_TIME = "ON_TIME"
    LATE = "LATE"
    ABSENT = "ABSENT"
    INVALID_LOCATION = "INVALID_LOCATION"
    EXPIRED = "EXPIRED"


def calculate_attendance_status(
    scan_time: datetime,
    class_start: datetime,
    class_end: datetime,
    grace_period_minutes: int,
    is_location_valid: bool
) -> AttendanceStatus:
    """
    Determine attendance status based on scan time and location validity.
    
    Logic:
    - INVALID_LOCATION: User is more than 100m from the classroom
    - EXPIRED: QR scanned more than 24h after class end
    - ON_TIME: Scanned before class_start + grace_period
    - LATE: Scanned after grace period but before class_end
    - ABSENT: Scanned after class_end
    
    Args:
        scan_time: When the QR was scanned
        class_start: Scheduled class start time
        class_end: Scheduled class end time
        grace_period_minutes: Minutes of tolerance after class start
        is_location_valid: Whether user is within 100m radius
    
    Returns:
        AttendanceStatus enum value
    """
    # First check location validity
    if not is_location_valid:
        return AttendanceStatus.INVALID_LOCATION
    
    # Check if QR is expired (more than 24h after class end)
    expiration_time = class_end + timedelta(hours=24)
    if scan_time > expiration_time:
        return AttendanceStatus.EXPIRED
    
    # Calculate grace period end time
    grace_end = class_start + timedelta(minutes=grace_period_minutes)
    
    # Determine status based on scan time
    if scan_time <= grace_end:
        return AttendanceStatus.ON_TIME
    elif scan_time <= class_end:
        return AttendanceStatus.LATE
    else:
        return AttendanceStatus.ABSENT


def get_status_message(status: AttendanceStatus, distance_meters: float = None) -> str:
    """
    Get user-friendly message for attendance status.
    
    Args:
        status: AttendanceStatus enum value
        distance_meters: Optional distance from location
    
    Returns:
        User-friendly status message
    """
    messages = {
        AttendanceStatus.ON_TIME: "✅ Asistencia registrada - A tiempo",
        AttendanceStatus.LATE: "⚠️ Asistencia registrada - Retraso",
        AttendanceStatus.ABSENT: "❌ Falta - Llegaste después de que terminó la clase",
        AttendanceStatus.INVALID_LOCATION: f"📍 Ubicación inválida - Debes estar en el aula (estás a {int(distance_meters)}m)" if distance_meters else "📍 Ubicación inválida - Debes estar en el aula",
        AttendanceStatus.EXPIRED: "⏰ QR expirado - Ya no es válido",
    }
    return messages.get(status, "Estado desconocido")


def get_status_color(status: AttendanceStatus) -> str:
    """
    Get color code for status display.
    
    Args:
        status: AttendanceStatus enum value
    
    Returns:
        Hex color code
    """
    colors = {
        AttendanceStatus.ON_TIME: "#10b981",      # Green
        AttendanceStatus.LATE: "#f59e0b",         # Orange
        AttendanceStatus.ABSENT: "#ef4444",       # Red
        AttendanceStatus.INVALID_LOCATION: "#ef4444",  # Red
        AttendanceStatus.EXPIRED: "#6b7280",      # Gray
    }
    return colors.get(status, "#6b7280")
