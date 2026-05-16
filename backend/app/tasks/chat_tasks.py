"""
Chat Processing Tasks
Handles heavy LLM operations asynchronously
"""

from app.worker.celery_app import celery_app


@celery_app.task
def generate_chat_response_task(payload: dict):
    """
    Async chat response generation

    Future use:
    - Streaming
    - Long-running queries
    """
    # Placeholder for future scaling
    return {"status": "queued"}