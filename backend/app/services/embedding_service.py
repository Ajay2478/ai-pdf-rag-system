"""
Embedding Pipeline Service

Responsible for:
- Fetching chunks
- Generating embeddings
- Storing vectors in DB
"""

from sqlalchemy.orm import Session
from app.models.document_chunk import DocumentChunk
from app.nlp.embeddings import generate_batch_embeddings


def embed_document_chunks(db: Session, document_id: int):
    """
    Generate embeddings for all chunks of a document
    """

    # Fetch chunks without embeddings
    chunks = (
        db.query(DocumentChunk)
        .filter(
            DocumentChunk.document_id == document_id,
            DocumentChunk.embedding.is_(None)
        )
        .order_by(DocumentChunk.chunk_index)
        .all()
    )

    if not chunks:
        return 0

    texts = [chunk.content for chunk in chunks]

    # Batch embedding (important for speed)
    embeddings = generate_batch_embeddings(texts)

    for chunk, emb in zip(chunks, embeddings):
        chunk.embedding = emb

    db.commit()

    return len(chunks)