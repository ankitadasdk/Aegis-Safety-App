from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm   # <-- Correct import
from sqlalchemy.orm import Session
from app import models, schemas, auth
from app.database import SessionLocal

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(SessionLocal)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, full_name=user.full_name, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(SessionLocal)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserOut)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user