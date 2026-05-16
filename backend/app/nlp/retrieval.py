"""
Semantic Retrieval Engine
"""

from sqlalchemy.orm import Session

from app.nlp.embeddings import generate_embedding
from app.nlp.vector_store import search_vectors


SIMILARITY_THRESHOLD = 0.30


def search_similar_chunks(
    db: Session,
    query: str,
    document_id: int,
    top_k: int = 5,
):
    """
    Retrieve semantically similar chunks
    """

    # ---------------------------------------------------
    # Generate embedding
    # ---------------------------------------------------
    query_embedding = generate_embedding(query)

    if not query_embedding:
        return []

    # ---------------------------------------------------
    # Search vector store
    # ---------------------------------------------------
    results = search_vectors(
        db=db,
        query_embedding=query_embedding,
        document_id=document_id,
        top_k=top_k,
    )

    # ---------------------------------------------------
    # Filter results
    # ---------------------------------------------------
    final_results = []

    for chunk, distance in results:

        similarity = 1 - distance

        print("=" * 50)
        print("CHUNK:", chunk.id)
        print("SIMILARITY:", similarity)
        print(chunk.content[:200])
        print("=" * 50)

        if similarity >= SIMILARITY_THRESHOLD:

            final_results.append({
                "chunk_id": chunk.id,
                "content": chunk.content,
                "chunk_index": chunk.chunk_index,
                "similarity": round(similarity, 4),
            })

    return final_results