from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    photo_id = Column(Integer, ForeignKey("photos.id"), index=True)
    text = Column(String(500))
    ip_address = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())