"""
Chat Service with Context Memory + Streaming
"""

from typing import Generator, cast
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.chat_session import ChatSession
from app.models.chat_message import ChatMessage

from app.nlp.retrieval import search_similar_chunks

from app.services.context_service import (
    build_context,
    get_chat_history,
    build_chat_history_text
)

from app.services.llm_service import stream_answer


def chat_stream_with_document(
    db: Session,
    user_id: int,
    document_id: int,
    question: str,
    session_id: int | None = None
) -> Generator[str, None, None]:
    """
    SSE-friendly generator:
    - yields JSON lines as 'data: ...\\n\\n'
    - saves user msg immediately
    - streams tokens
    - saves assistant msg at the end
    """

    # 1) Create / validate session
    if session_id is not None:
        session = db.query(ChatSession).filter_by(id=session_id).first()
        if session is None:
            raise HTTPException(404, "Chat session not found")

        if cast(int, session.user_id) != user_id:
            raise HTTPException(403, "Unauthorized session access")
    else:
        session = ChatSession(user_id=user_id, document_id=document_id)
        db.add(session)
        db.commit()
        db.refresh(session)

    sid = cast(int, session.id)

    # 2) Fetch history BEFORE adding new message
    history_msgs = get_chat_history(db, sid, limit=6)
    history_text = build_chat_history_text(history_msgs)

    # 3) Save user message
    db.add(ChatMessage(session_id=sid, role="user", content=question))
    db.commit()  # commit early so it's durable even if stream fails

    # 4) Retrieval
    chunks = search_similar_chunks(
        db=db,
        query=question,
        document_id=document_id,
        top_k=5
    )
    context = build_context(chunks)

    # 5) Start stream
    yield f"data: {{\"type\":\"meta\",\"session_id\":{sid}}}\n\n"

    accumulated: list[str] = []

    try:
        gen = stream_answer(context=context, question=question, history=history_text)

        while True:
            try:
                token = next(gen)
                accumulated.append(token)
                # send token
                # keep payload small; client concatenates
                safe = token.replace("\n", "\\n").replace("\"", "\\\"")
                yield f"data: {{\"type\":\"token\",\"content\":\"{safe}\"}}\n\n"
            except StopIteration as e:
                # final text from generator return
                final_text = (e.value or "").strip()
                break

    except Exception as e:
        # stream error to client
        msg = str(e).replace("\n", " ")
        yield f"data: {{\"type\":\"error\",\"message\":\"{msg}\"}}\n\n"
        return

    # 6) Persist assistant message
    if final_text:
        db.add(ChatMessage(session_id=sid, role="assistant", content=final_text))
        db.commit()

    # 7) Send sources once (end of stream)
    sources_payload = [
        {"chunk_id": int(c.id), "content": c.content[:200].replace("\n", " ")}
        for c in chunks
    ]
    # minimal JSON encoding (avoid import json to keep hot path lean)
    yield "data: {\"type\":\"done\",\"sources\":" + str(sources_payload).replace("'", "\"") + "}\n\n"