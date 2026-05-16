"""
Context Service

Handles:
- Context construction for RAG
- Chat history formatting
- Prompt size management
"""

from typing import List
from sqlalchemy.orm import Session

from app.models.chat_message import ChatMessage


# =========================================================
# CONTEXT BUILDER
# =========================================================

def build_context(
    chunks: List[dict],
    max_chars: int = 4000,
) -> str:
    """
    Build structured LLM context from retrieved chunks.

    Args:
        chunks: Retrieved semantic chunks
        max_chars: Maximum context size

    Returns:
        str
    """

    if not chunks:
        return ""

    context_parts = []
    total_chars = 0

    for i, chunk in enumerate(chunks, start=1):

        chunk_text = chunk["content"].strip()

        similarity = chunk.get("similarity", 0)

        formatted_chunk = f"""
[Context Chunk {i}]
Similarity Score: {similarity}

{chunk_text}
"""

        # Token budget control
        if total_chars + len(formatted_chunk) > max_chars:
            break

        context_parts.append(formatted_chunk)

        total_chars += len(formatted_chunk)

    return "\n\n".join(context_parts)


# =========================================================
# CHAT HISTORY FETCHER
# =========================================================

def get_chat_history(
    db: Session,
    session_id: int,
    limit: int = 6,
):
    """
    Fetch latest chat history
    """

    messages = (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.id.desc())
        .limit(limit)
        .all()
    )

    # Convert to chronological order
    return list(reversed(messages))


# =========================================================
# CHAT HISTORY FORMATTER
# =========================================================

def build_chat_history_text(messages: list) -> str:
    """
    Convert chat history into LLM-readable format
    """

    if not messages:
        return ""

    history_parts = []

    for msg in messages:

        role = (
            "User"
            if msg.role == "user"
            else "Assistant"
        )

        history_parts.append(
            f"{role}: {msg.content}"
        )

    return "\n".join(history_parts)