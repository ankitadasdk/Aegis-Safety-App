from typing import List, Tuple
from app import models
from math import radians, cos, sin, asin, sqrt, atan2

def haversine(lon1, lat1, lon2, lat2):
    """Calculate great-circle distance between two points in km."""
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)*2 + cos(lat1) * cos(lat2) * sin(dlon/2)*2
    c = 2 * asin(sqrt(a))
    r = 6371 
    return c * r

def point_in_circle(lat, lon, center_lat, center_lon, radius_km):
    """Check if point lies within circle of given radius (km)."""
    return haversine(lon, lat, center_lon, center_lat) <= radius_km

def get_safe_route(start: Tuple[float, float], end: Tuple[float, float], danger_zones: List[models.DangerZone]):
    """
    Return a list of (lat, lon) points representing a safe route.
    Simple implementation: if direct line intersects a danger zone, add a detour point.
    """
    lat1, lon1 = start
    lat2, lon2 = end
    points = [(lat1, lon1), (lat2, lon2)]
    for zone in danger_zones:
        if _segment_intersects_circle(lat1, lon1, lat2, lon2, zone.center_lat, zone.center_lon, zone.radius/1000.0):
            import math
            dx = lon2 - lon1
            dy = lat2 - lat1
            perp = (-dy, dx) if dx != 0 or dy != 0 else (1, 0)
            norm = math.hypot(perp[0], perp[1])
            perp = (perp[0]/norm, perp[1]/norm)
            detour_km = 0.5
            detour_lat = (lat1+lat2)/2 + perp[1] * detour_km / 111.0  
            detour_lon = (lon1+lon2)/2 + perp[0] * detour_km / (111.0 * math.cos(math.radians((lat1+lat2)/2)))
            points.insert(1, (detour_lat, detour_lon))
            break  
    return points

def _segment_intersects_circle(lat1, lon1, lat2, lon2, cx, cy, radius_km):
    """Check if line segment (p1,p2) intersects circle center (cx,cy) radius r."""
    if point_in_circle(lat1, lon1, cx, cy, radius_km) or point_in_circle(lat2, lon2, cx, cy, radius_km):
        return True
    mid_lat = (lat1+lat2)/2
    mid_lon = (lon1+lon2)/2
    if point_in_circle(mid_lat, mid_lon, cx, cy, radius_km):
        return True
    return False
