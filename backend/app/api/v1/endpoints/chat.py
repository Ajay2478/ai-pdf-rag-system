from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.services.chat_service import chat_stream_with_document

router = APIRouter()


@router.post("/stream")
def chat_stream(
    document_id: int,
    question: str,
    session_id: int | None = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """
    Server-Sent Events (SSE) streaming endpoint
    """
    generator = chat_stream_with_document(
        db=db,
        user_id=current_user.id,
        document_id=document_id,
        question=question,
        session_id=session_id
    )

    return StreamingResponse(
        generator,
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )