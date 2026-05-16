"""
Document Processing Tasks

Handles:
- PDF extraction
- Chunking
- Embedding generation
- Vector storage
"""

from celery.utils.log import get_task_logger

from app.worker.celery_app import celery_app
from app.db.session import SessionLocal

from app.services.processing_service import process_document_pipeline
from app.models.document import Document

logger = get_task_logger(__name__)


@celery_app.task(
    name="app.tasks.document_tasks.process_document_task",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
    retry_kwargs={"max_retries": 5},
)
def process_document_task(self, document_id: int):
    """
    Background document processing pipeline

    Steps:
    1. Mark document as processing
    2. Extract PDF text
    3. Chunk document
    4. Generate embeddings
    5. Store vectors
    6. Mark document as processed
    """

    db = SessionLocal()

    try:
        logger.info(f"Starting processing for document_id={document_id}")

        # ---------------------------------------------------
        # Fetch document
        # ---------------------------------------------------
        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if not document:
            raise ValueError(f"Document {document_id} not found")

        # ---------------------------------------------------
        # Update status -> processing
        # ---------------------------------------------------
        document.status = "processing"
        db.commit()

        # ---------------------------------------------------
        # Run processing pipeline
        # ---------------------------------------------------
        process_document_pipeline(
            db=db,
            document_id=document_id,
        )

        # ---------------------------------------------------
        # Update status -> processed
        # ---------------------------------------------------
        document.status = "processed"
        db.commit()

        logger.info(
            f"Document processed successfully: document_id={document_id}"
        )

        return {
            "status": "success",
            "document_id": document_id,
        }

    except Exception as e:
        logger.exception(
            f"Document processing failed for document_id={document_id}"
        )

        # ---------------------------------------------------
        # Update DB status -> failed
        # ---------------------------------------------------
        try:
            document = (
                db.query(Document)
                .filter(Document.id == document_id)
                .first()
            )

            if document:
                document.status = "failed"
                db.commit()

        except Exception:
            logger.exception("Failed to update document status")

        raise self.retry(exc=e)

    finally:
        db.close()