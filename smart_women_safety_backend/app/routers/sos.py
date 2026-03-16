from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, auth
from app.database import SessionLocal
from datetime import datetime

router = APIRouter(prefix="/sos", tags=["sos"])

@router.post("/trigger", response_model=schemas.SOSOut)
def trigger_sos(alert: schemas.SOSCreate, db: Session = Depends(SessionLocal),
                current_user: models.User = Depends(auth.get_current_user)):
    db_alert = models.SOSAlert(
        user_id=current_user.id,
        latitude=alert.latitude,
        longitude=alert.longitude,
        status="active"
    )
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    contacts = db.query(models.EmergencyContact).filter(models.EmergencyContact.user_id == current_user.id).all()
    for c in contacts:
        print(f"Alert sent to {c.name} at {c.phone} (location: {alert.latitude},{alert.longitude})")
    return db_alert

@router.get("/history", response_model=list[schemas.SOSOut])
def get_history(db: Session = Depends(SessionLocal),
                current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.SOSAlert).filter(models.SOSAlert.user_id == current_user.id).order_by(models.SOSAlert.timestamp.desc()).all()