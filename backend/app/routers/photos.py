from fastapi import APIRouter, UploadFile , File
import os
from pathlib import Path

router = APIRouter(
    prefix="/photos",
    tags=["photos"]
)

UPLOAD_DIR = Path("app/static/photos")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.get("/")
def list_photos():
    return {"photos": ["photo1.jpg", "photo2.jpg"]}

@router.get("/{photo_id}")
def get_photo(photo_id: int):
    return {"photo": photo_id}

@router.post("/upload")
async def upload_photo(file: UploadFile = File(...)):
    file_location = UPLOAD_DIR/file.filename

    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())

    return {
        "filename": file.filename,
        "path": str(file_location),
        "message": "File Saved Succesfully"
    }
