from sqlalchemy import Column, Integer, String, TIMESTAMP
from datetime import datetime

from app.db.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer)
    action = Column(String(100))
    resource = Column(String(100))
    resource_id = Column(Integer)

    details = Column(String, nullable=True)

    created_at = Column(TIMESTAMP, default=datetime.utcnow)