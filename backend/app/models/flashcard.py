from sqlalchemy import Column, Integer, Text, ForeignKey
from app.db.base import Base


class Flashcard(Base):
    __tablename__ = "flashcards"

    id = Column(Integer, primary_key=True, index=True)

    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"))

    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)