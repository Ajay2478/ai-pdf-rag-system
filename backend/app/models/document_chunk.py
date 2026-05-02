from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY, FLOAT

from app.db.base import Base


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)

    # Link to document
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"))

    # Actual chunk text
    content = Column(Text, nullable=False)

    # Embedding vector (for RAG)
    embedding = Column(ARRAY(FLOAT))

    # Optional metadata
    page_number = Column(Integer)
    chunk_index = Column(Integer)