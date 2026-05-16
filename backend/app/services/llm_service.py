"""
LLM Service
Groq-powered RAG generation layer

Features:
- Streaming responses
- Context-aware prompting
- Conversational memory
- Hallucination control
"""

from typing import Generator, Optional

from groq import Groq

from app.core.config import settings


# =========================================================
# GROQ CLIENT
# =========================================================

client = Groq(
    api_key=settings.GROQ_API_KEY
)


# =========================================================
# PROMPT BUILDER
# =========================================================

def _build_prompt(
    context: str,
    question: str,
    history: str = "",
) -> str:
    """
    Construct grounded RAG prompt
    """

    return f"""
You are an enterprise AI assistant for government and regulatory documents.

Your responsibilities:
- Answer ONLY using the retrieved document context
- Be factual and precise
- Summarize clearly
- Explain policy and regulatory language simply when needed
- Use chat history for conversational continuity
- If information is missing, explicitly say:
  "I could not find this information in the document."

RULES:
- Never invent information
- Never hallucinate
- Never use outside knowledge
- Prefer concise but complete answers

==================================================
CHAT HISTORY
==================================================

{history}

==================================================
RETRIEVED DOCUMENT CONTEXT
==================================================

{context}

==================================================
USER QUESTION
==================================================

{question}

==================================================
ANSWER
==================================================
"""


# =========================================================
# NON-STREAMING RESPONSE
# =========================================================

def generate_answer(
    context: str,
    question: str,
    history: str = "",
) -> str:
    """
    Generate complete answer
    """

    prompt = _build_prompt(
        context=context,
        question=question,
        history=history,
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a factual document AI assistant."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.1,
        max_tokens=1024,
    )

    content: Optional[str] = (
        response.choices[0].message.content
    )

    return (content or "").strip()


# =========================================================
# STREAMING RESPONSE
# =========================================================

def stream_answer(
    context: str,
    question: str,
    history: str = "",
) -> Generator[str, None, str]:
    """
    Stream LLM response token-by-token
    """

    prompt = _build_prompt(
        context=context,
        question=question,
        history=history,
    )

    stream = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a factual document AI assistant."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.1,
        max_tokens=1024,
        stream=True,
    )

    full_response_parts: list[str] = []

    for chunk in stream:

        delta = chunk.choices[0].delta.content

        if delta:

            full_response_parts.append(delta)

            yield delta

    return "".join(full_response_parts).strip()