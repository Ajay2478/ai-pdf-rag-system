"""
Search Service
Handles semantic search business logic
"""

from sqlalchemy.orm import Session

from app.nlp.retrieval import search_similar_chunks


def semantic_search(
    db: Session,
    query: str,
    document_id: int,
):
    """
    Run semantic vector search
    """

    results = search_similar_chunks(
        db=db,
        query=query,
        document_id=document_id,
    )

    return results