from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User
class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Emergency Contact
class ContactBase(BaseModel):
    name: str
    phone: str
    email: Optional[EmailStr] = None
    relationship: Optional[str] = None

class ContactCreate(ContactBase):
    pass

class ContactOut(ContactBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

# SOS Alert
class SOSCreate(BaseModel):
    latitude: float
    longitude: float

class SOSOut(BaseModel):
    id: int
    user_id: int
    timestamp: datetime
    latitude: float
    longitude: float
    status: str

# Crime Data (for seeding)
class CrimeDataCreate(BaseModel):
    latitude: float
    longitude: float
    crime_type: str
    severity: int
    timestamp: datetime
    description: Optional[str] = None

# Danger Zone (response)
class DangerZoneOut(BaseModel):
    id: int
    center_lat: float
    center_lon: float
    radius: float
    risk_level: str
    updated_at: datetime

# Safe Route Request
class RouteRequest(BaseModel):
    start_lat: float
    start_lon: float
    end_lat: float
    end_lon: float

# Safe Route Response
class RouteResponse(BaseModel):
    points: List[List[float]]   # list of [lat, lon]
    danger_zones_avoided: List[int]  # IDs of avoided zones