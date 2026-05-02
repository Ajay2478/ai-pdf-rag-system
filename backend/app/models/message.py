from sqlalchemy import Column, Integer, Text, ForeignKey, String, TIMESTAMP
from datetime import datetime

from app.db.base import Base


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(Integer, ForeignKey("chat_sessions.id", ondelete="CASCADE"))

    # Role: user / assistant
    role = Column(String(50), nullable=False)

    # Message content
    content = Column(Text, nullable=False)

    created_at = Column(TIMESTAMP, default=datetime.utcnow)