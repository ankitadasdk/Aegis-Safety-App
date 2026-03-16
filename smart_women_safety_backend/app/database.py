from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Creates the connection to your SQLite file
engine = create_engine(
    settings.database_url, 
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)

# This handles individual database transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# The base class that your models (User, CrimeData) will inherit from
Base = declarative_base()

# --- ADD THIS PART ---
def get_db():
    """
    Dependency that creates a new database session for a single request 
    and closes it once the request is done.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()