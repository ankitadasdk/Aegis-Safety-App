# seed_crime.py
from app.database import SessionLocal, engine, Base
from app.models import CrimeData
from datetime import datetime, timedelta, timezone
import random

# Create tables if they don't exist (optional, but safe)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Clear existing crime data (optional)
db.query(CrimeData).delete()

# Generate random crimes near a central location (e.g., Delhi)
center_lat, center_lon = 28.6139, 77.2090
crime_types = ["theft", "assault", "harassment", "robbery", "vandalism"]

for _ in range(100):
    lat = center_lat + random.uniform(-0.05, 0.05)
    lon = center_lon + random.uniform(-0.05, 0.05)
    days_ago = random.randint(0, 60)
    crime = CrimeData(
        latitude=lat,
        longitude=lon,
        crime_type=random.choice(crime_types),
        severity=random.randint(1, 5),
        # Use timezone-aware datetime, then make naive if needed
        timestamp=datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=days_ago),
        description="Mock crime data for testing"
    )
    db.add(crime)

db.commit()
db.close()

print(" 100 mock crime records added to the database.")