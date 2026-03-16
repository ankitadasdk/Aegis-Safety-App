from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, auth
from app.database import SessionLocal
router = APIRouter(prefix="/contacts", tags=["contacts"])
@router.get("/", response_model=list[schemas.ContactOut])
def get_contacts(db: Session = Depends(SessionLocal), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.EmergencyContact).filter(models.EmergencyContact.user_id == current_user.id).all()
@router.post("/", response_model=schemas.ContactOut)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(SessionLocal),
                   current_user: models.User = Depends(auth.get_current_user)):
    db_contact = models.EmergencyContact(**contact.dict(), user_id=current_user.id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact
@router.delete("/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(SessionLocal),
                   current_user: models.User = Depends(auth.get_current_user)):
    contact = db.query(models.EmergencyContact).filter(models.EmergencyContact.id == contact_id,
                                                       models.EmergencyContact.user_id == current_user.id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return {"ok": True}