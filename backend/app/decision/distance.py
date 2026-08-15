import math

def haversine(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Calculate distance in km between two lat/lng points using the Haversine formula."""
    R = 6371.0  # Earth radius in km
    
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlng / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

def estimate_eta(distance_km: float, speed_kmh: float = 40.0) -> float:
    """Estimate travel time in minutes given distance and average speed."""
    if speed_kmh <= 0:
        return 999.0
    return (distance_km / speed_kmh) * 60.0
