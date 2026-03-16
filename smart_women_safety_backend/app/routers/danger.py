from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas, utils
from app.database import SessionLocal
from typing import List

router = APIRouter(prefix="/danger", tags=["danger"])

@router.get("/zones", response_model=List[schemas.DangerZoneOut])
def get_danger_zones(lat: float, lon: float, radius: float = 2.0, db: Session = Depends(SessionLocal)):
    zones = db.query(models.DangerZone).all()
    result = []
    for z in zones:
        if utils.danger_zone.haversine(lon, lat, z.center_lon, z.center_lat) <= radius:
            result.append(z)
    return result
@router.post("/compute")
def compute_zones(lat: float, lon: float, db: Session = Depends(SessionLocal)):
    zones = utils.danger_zone.compute_danger_zones(db, lat, lon)
    return {"message": f"Computed {len(zones)} zones"}