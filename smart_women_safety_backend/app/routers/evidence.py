import os
import aiofiles
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from datetime import datetime, timezone
from app import auth, models
from app.config import settings

UPLOAD_DIR = "data/evidence"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/evidence", tags=["evidence"])

@router.post("/upload")
async def upload_evidence(file: UploadFile = File(...), current_user: models.User = Depends(auth.get_current_user)):
    # Save file with user ID and timestamp
    ext = os.path.splitext(file.filename)[1]
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    filename = f"user_{current_user.id}_{now.strftime('%Y%m%d_%H%M%S')}{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    return {"filename": filename, "path": file_path}