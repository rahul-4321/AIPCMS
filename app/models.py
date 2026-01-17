from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from datetime import datetime
from app.database import Base

class ModerationLog(Base):
    __tablename__ = "moderation_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    content_type = Column(String(5)) #holds value text or image
    original_content = Column(String)
    is_safe = Column(Integer) #1 and 0
    scores = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


class BlockedUser(Base):
    __tablename__="blocked_users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    reason = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)