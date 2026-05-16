"""
Vector Store Layer (pgvector)

Handles:
- similarity search
- vector querying
- future hybrid retrieval
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk


def search_vectors(
    db: Session,
    query_embedding: list[float],
    document_id: int,
    top_k: int = 5,
):
    """
    Search similar vectors using cosine distance
    """

    stmt = (
        select(
            DocumentChunk,
            DocumentChunk.embedding.cosine_distance(
                query_embedding
            ).label("distance")
        )
        .where(
            DocumentChunk.document_id == document_id
        )
        .order_by("distance")
        .limit(top_k)
    )

    results = db.execute(stmt).all()

    return results