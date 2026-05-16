"""
Processing Service
Handles full document processing pipeline
"""

from sqlalchemy.orm import Session
from datetime import datetime

from app.models.document import Document
from app.utils.pdf_parser import extract_text_from_pdf
from app.nlp.chunking import chunk_text
from app.models.document_chunk import DocumentChunk
from app.services.embedding_service import embed_document_chunks


def process_document_pipeline(db: Session, document_id: int) -> int:
    """
    Orchestrates full document processing lifecycle

    Steps:
    - Validate document
    - Update status → processing
    - Run pipeline
    - Update status → completed / failed
    """

    # ==============================
    # 1. FETCH DOCUMENT
    # ==============================
    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        raise ValueError(f"Document {document_id} not found")

    try:
        # ==============================
        # 2. UPDATE STATUS → PROCESSING
        # ==============================
        document.status = "processing"
        document.error_message = None
        db.commit()

        # ==============================
        # 3. RUN CORE PIPELINE
        # ==============================
        chunk_count = process_document(
            db=db,
            document_id=document.id,
            file_path=document.file_path
        )

        # ==============================
        # 4. UPDATE STATUS → COMPLETED
        # ==============================
        document.status = "completed"
        document.processed_at = datetime.utcnow()
        db.commit()

        return chunk_count

    except Exception as e:
        # ==============================
        # 5. HANDLE FAILURE
        # ==============================
        document.status = "failed"
        document.error_message = str(e)
        db.commit()

        # Important: re-raise for Celery retry
        raise


def process_document(db: Session, document_id: int, file_path: str) -> int:
    """
    Core processing pipeline:

    1. Extract text
    2. Chunk text
    3. Store chunks
    4. Generate embeddings
    """

    # ==============================
    # 1. EXTRACT TEXT
    # ==============================
    text = extract_text_from_pdf(file_path)

    if not text:
        raise ValueError("Failed to extract text from PDF")

    # ==============================
    # 2. CHUNK TEXT
    # ==============================
    chunks = chunk_text(text)

    if not chunks:
        raise ValueError("Chunking produced no output")

    # ==============================
    # 3. STORE CHUNKS (IDEMPOTENT)
    # ==============================
    # Prevent duplicate chunks if reprocessed
    db.query(DocumentChunk).filter(
        DocumentChunk.document_id == document_id
    ).delete()

    db_chunks = []

    for idx, chunk in enumerate(chunks):
        db_chunk = DocumentChunk(
            document_id=document_id,
            content=chunk,
            chunk_index=idx,
        )
        db_chunks.append(db_chunk)

    db.add_all(db_chunks)
    db.commit()

    # ==============================
    # 4. GENERATE EMBEDDINGS
    # ==============================
    embed_document_chunks(db, document_id)

    return len(db_chunks)