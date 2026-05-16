"""
Document Service
Handles document lifecycle
"""

from sqlalchemy.orm import Session
from celery.app.task import Task
from typing import cast

from app.models.document import Document
from app.tasks.document_tasks import process_document_task


# Proper typing for Celery task methods
celery_process_document_task = cast(Task, process_document_task)


def create_document(
    db: Session,
    user_id: int,
    filename: str,
    file_path: str,
):
    """
    Create document record and trigger async processing.
    """

    # Create document entry
    doc = Document(
        user_id=user_id,
        filename=filename,
        file_path=file_path,
        status="queued",
    )

    db.add(doc)
    db.commit()
    db.refresh(doc)

    # Trigger background processing task
    celery_process_document_task.apply_async(args=[doc.id])

    return doc