from app import models
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import math

def compute_danger_zones(db: Session, center_lat: float, center_lon: float, radius_km: float = 2.0):
    """
    For a given center point, compute danger zones based on crime data.
    Returns a list of DangerZone objects (already saved to DB).
    """
    time_threshold = datetime.utcnow() - timedelta(days=30)
    crimes = db.query(models.CrimeData).filter(
        models.CrimeData.timestamp >= time_threshold
    ).all()
    grid_size = 0.002  
    zones = {}
    for crime in crimes:
        gx = round(crime.latitude / grid_size)
        gy = round(crime.longitude / grid_size)
        key = (gx, gy)
        if key not in zones:
            zones[key] = []
        zones[key].append(crime)
    new_zones = []
    for (gx, gy), crimes_list in zones.items():
        if len(crimes_list) < 3:
            continue
        center = (gx * grid_size, gy * grid_size)
        total_severity = sum(c.severity for c in crimes_list)
        avg_severity = total_severity / len(crimes_list)
        if avg_severity >= 4 or len(crimes_list) > 10:
            risk = "high"
        elif avg_severity >= 2 or len(crimes_list) > 5:
            risk = "medium"
        else:
            risk = "low"

        zone = models.DangerZone(
            center_lat=center[0],
            center_lon=center[1],
            radius=200,  
            risk_level=risk
        )
        db.add(zone)
        new_zones.append(zone)
    db.commit()
    return new_zones