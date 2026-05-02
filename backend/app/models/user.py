from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from datetime import datetime

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    # Primary identifier
    id = Column(Integer, primary_key=True, index=True)

    # Auth fields
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)

    # Profile
    full_name = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    # Metadata
    created_at = Column(TIMESTAMP, default=datetime.utcnow)