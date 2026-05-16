# app/models/document_chunk.py

"""
DocumentChunk Model
-------------------
Stores processed text chunks from documents along with embeddings.

This is the core table for RAG:
- content → text
- embedding → semantic vector
- metadata → retrieval context
"""

from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector

from app.db.base import Base


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    # Primary Key
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    # Foreign Key (MULTI-USER SAFE via document ownership)
    document_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Actual chunk content
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    # Chunk ordering (important for reconstruction)
    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    # Optional metadata (useful for UI + traceability)
    page_number: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    # VECTOR EMBEDDING (CORE OF RAG)
    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(384),   # all-MiniLM-L6-v2 → 384 dims
        nullable=True
    )