from fastapi import FastAPI, Request
from app.routers import users, contacts, sos, danger, navigation, evidence
from app.database import engine, Base
import uvicorn
import logging # Added this
from datetime import datetime # Added this

# --- NEW SEPARATE SPACE LOGGING ---
# This creates a file named 'sos_alerts.log' in your backend folder
logging.basicConfig(
    filename='sos_alerts.log', 
    level=logging.INFO,
    format='%(message)s'
)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Women Safety API")

# --- SOS MONITORING MIDDLEWARE ---
# This catches every SOS request and saves it to a text file automatically
@app.middleware("http")
async def monitor_sos(request: Request, call_next):
    response = await call_next(request)
    if request.url.path == "/sos/trigger" and request.method == "POST":
        log_entry = f"[{datetime.now()}] 🚨 SOS RECEIVED from IP: {request.client.host}"
        
        # Save to the log file
        logging.info(log_entry)
        
        # Also save to a simple text file for you to look at later
        with open("emergency_history.txt", "a") as f:
            f.write(f"{log_entry}\n")
            
    return response

app.include_router(users.router)
app.include_router(contacts.router)
app.include_router(sos.router)
app.include_router(danger.router)
app.include_router(navigation.router)
app.include_router(evidence.router)

@app.get("/")
def root():
    return {"message": "Smart Women Safety API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)