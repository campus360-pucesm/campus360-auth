"""
Geolocation utilities for QR code validation
Includes Haversine distance calculation for location verification
"""

from math import radians, sin, cos, sqrt, atan2


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great-circle distance between two points on Earth
    using the Haversine formula.
    
    Args:
        lat1: Latitude of point 1 in degrees
        lon1: Longitude of point 1 in degrees
        lat2: Latitude of point 2 in degrees
        lon2: Longitude of point 2 in degrees
    
    Returns:
        Distance in meters
    """
    # Earth's radius in meters
    R = 6371000
    
    # Convert degrees to radians
    lat1_rad = radians(lat1)
    lat2_rad = radians(lat2)
    delta_lat = radians(lat2 - lat1)
    delta_lon = radians(lon2 - lon1)
    
    # Haversine formula
    a = sin(delta_lat/2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    distance = R * c
    return distance


def is_within_radius(
    user_lat: float,
    user_lon: float,
    location_lat: float,
    location_lon: float,
    radius_meters: float = 100
) -> tuple[bool, float]:
    """
    Check if user is within allowed radius of a location.
    
    Args:
        user_lat: User's latitude
        user_lon: User's longitude
        location_lat: Location's latitude
        location_lon: Location's longitude
        radius_meters: Maximum allowed distance in meters (default: 100)
    
    Returns:
        Tuple of (is_valid, distance_in_meters)
    """
    distance = haversine_distance(user_lat, user_lon, location_lat, location_lon)
    is_valid = distance <= radius_meters
    return (is_valid, distance)


def format_distance(distance_meters: float) -> str:
    """
    Format distance for display.
    
    Args:
        distance_meters: Distance in meters
    
    Returns:
        Formatted string (e.g., "45m" or "1.2km")
    """
    if distance_meters < 1000:
        return f"{int(distance_meters)}m"
    else:
        return f"{distance_meters/1000:.1f}km"
