from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP
from datetime import datetime

from app.db.base import Base


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"))

    created_at = Column(TIMESTAMP, default=datetime.utcnow)