# app/models/document.py

"""
Document Model (Production-Grade, Multi-User Ready)

Responsibilities:
- Store uploaded file metadata
- Track processing lifecycle
- Maintain ownership (user_id)
"""

from datetime import datetime

from sqlalchemy import String, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Document(Base):
    __tablename__ = "documents"

    # Primary Key
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    # MULTI-USER CORE (Ownership)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # File Information
    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    # Processing Status
    status: Mapped[str] = mapped_column(
        String(50),
        default="uploaded",
        nullable=False
    )
    # Possible values:
    # uploaded → processing → completed → failed

    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        default=datetime.utcnow,
        nullable=False
    )