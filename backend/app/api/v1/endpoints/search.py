"""
Search Endpoint (Semantic Search)
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.search_service import semantic_search

router = APIRouter()


@router.post("/")
def search_documents(
    query: str,
    document_id: int,
    db: Session = Depends(get_db),
):
    """
    Semantic vector search endpoint
    """

    results = semantic_search(
        db=db,
        query=query,
        document_id=document_id,
    )

    return {
        "query": query,
        "document_id": document_id,
        "total_results": len(results),
        "results": results,
    }