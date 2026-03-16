from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas, utils
from app.database import SessionLocal
from typing import List

router = APIRouter(prefix="/navigation", tags=["navigation"])

@router.post("/safe-route", response_model=schemas.RouteResponse)
def safe_route(request: schemas.RouteRequest, db: Session = Depends(SessionLocal)):
    zones = db.query(models.DangerZone).all()  
    start = (request.start_lat, request.start_lon)
    end = (request.end_lat, request.end_lon)
    points = utils.routing.get_safe_route(start, end, zones)
    avoided = [z.id for z in zones if utils.routing._segment_intersects_circle(
        start[0], start[1], end[0], end[1], z.center_lat, z.center_lon, z.radius/1000.0
    )]
    return schemas.RouteResponse(points=points, danger_zones_avoided=avoided)