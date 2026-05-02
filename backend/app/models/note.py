from sqlalchemy import Column, Integer, Text, ForeignKey
from app.db.base import Base


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)

    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"))

    content = Column(Text, nullable=False)