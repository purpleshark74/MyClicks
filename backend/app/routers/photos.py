from fastapi import APIRouter, UploadFile , File, Depends
from sqlalchemy.orm import Session
from pathlib import Path
import os

from app.database import get_db
from app.models.photo import Photo

router = APIRouter(
    prefix="/photos",
    tags=["photos"]
)

UPLOAD_DIR = Path("app/static/photos")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.get("/")
def list_photos(db: Session = Depends(get_db)):
    photos = db.query(Photo).all()
    return [
        {
            "id": p.id,
            "filename": p.filename, 
            "url": f"/static/photos/{p.filename}"
        }
        for p in photos
    ]

@router.get("/{photo_id}")
def get_photo(photo_id: int, db: Session = Depends(get_db)):
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if not photo:
        return {"error": "photo not found"}
    return {
        "id": photo.id,
        "filename": photo.filename, 
        "url": f"/static/photos/{photo.filename}"
    }

@router.post("/upload")
async def upload_photo(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_location = UPLOAD_DIR/file.filename

    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())
    
    photo = Photo(
        filename = file.filename,
        filepath = str(file_location)
    )

    db.add(photo)
    db.commit()
    db.refresh(photo)

    return {
        "id": photo.id,
        "filename": photo.filename, 
        "path": photo.filepath
    }
