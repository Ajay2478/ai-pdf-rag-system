from sqlalchemy import Column, Integer, ForeignKey, String, TIMESTAMP
from datetime import datetime

from app.db.base import Base


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)

    # Ownership (MULTI-USER)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    # Context (VERY IMPORTANT)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"))

    # Optional title (generated later)
    title = Column(String(255), nullable=True)

    created_at = Column(TIMESTAMP, default=datetime.utcnow)