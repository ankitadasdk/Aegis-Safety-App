from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    contacts = relationship("EmergencyContact", back_populates="user")
    sos_alerts = relationship("SOSAlert", back_populates="user")


class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    phone = Column(String)
    email = Column(String, nullable=True)
    # Renamed from 'relationship' to avoid conflict with the sqlalchemy.orm.relationship function
    contact_relation = Column(String, nullable=True)

    # This uses the imported 'relationship' function (not the column)
    user = relationship("User", back_populates="contacts")


class SOSAlert(Base):
    __tablename__ = "sos_alerts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    latitude = Column(Float)
    longitude = Column(Float)
    status = Column(String, default="active")

    user = relationship("User", back_populates="sos_alerts")


class CrimeData(Base):
    __tablename__ = "crime_data"
    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    crime_type = Column(String)
    severity = Column(Integer)
    timestamp = Column(DateTime)
    description = Column(Text, nullable=True)


class DangerZone(Base):
    __tablename__ = "danger_zones"
    id = Column(Integer, primary_key=True, index=True)
    center_lat = Column(Float)
    center_lon = Column(Float)
    radius = Column(Float)
    risk_level = Column(String)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))