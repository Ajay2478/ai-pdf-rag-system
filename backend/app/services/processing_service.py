from sqlalchemy.orm import Session

from app.utils.pdf_parser import extract_text_from_pdf
from app.nlp.chunking import chunk_text
from app.models.document_chunk import DocumentChunk


def process_document(db: Session, document_id: int, file_path: str):
    """
    Full processing pipeline:

    1. Extract text
    2. Chunk text
    3. Store chunks in DB
    """

    # Step 1: Extract text
    text = extract_text_from_pdf(file_path)

    if not text:
        raise ValueError("Failed to extract text from PDF")

    # Step 2: Chunk text
    chunks = chunk_text(text)

    # Step 3: Store chunks
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

    return len(db_chunks)