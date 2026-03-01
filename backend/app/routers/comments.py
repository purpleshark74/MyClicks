from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

from app.database import get_db
from app.models.comment import Comment

router = APIRouter(
    prefix="/comments",
    tags=["comments"]
)

@router.post("/add/{photo_id}")
def add_comment(photo_id: int, request: Request, text: str, db: Session = Depends(get_db)):
    ip = request.client.host

    ten_seconds_ago = datetime.now(timezone.utc) - timedelta(seconds=10)
    recent_comment = (
        db.query(Comment)
        .filter(Comment.ip_address == ip)
        .filter(Comment.created_at < ten_seconds_ago)
        .first()
    )

    if recent_comment:
        raise HTTPException(status_code=429, detail="You are commenting too fast. Please wait a moment")

    one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
    hourly_count = (
        db.query(Comment)
        .filter(Comment.ip_address == ip)
        .filter(Comment.created_at < one_hour_ago)
        .count()
    )

    if hourly_count >= 20 :
        raise HTTPException(status_code=429, detail="Too many comments from this IP. Try again later.")

    comment = Comment(
        photo_id = photo_id,
        text = text,
        ip_address = ip
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return {"message": "comment added", "id": comment.id}

@router.get("/{photo_id}")
def get_comments(photo_id: int, db: Session = Depends(get_db)):
    comments = (
        db.query(Comment)
        .filter(Comment.photo_id == photo_id)
        .order_by(Comment.created_at.desc())
        .all()
        )

    return [
        {
            "id": c.id,
            "text": c.text,
            "created_at": c.created_at
        }
        for c in comments
    ]