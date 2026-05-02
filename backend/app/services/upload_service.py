from sqlalchemy.orm import Session
from app.storage.local_storage import save_file
from app.services.document_service import create_document
from app.services.processing_service import process_document

def handle_file_upload(db: Session, user_id: int, file):
    """
    Full upload flow:
    - Save file
    - Create DB record
    Upload + Process
    """

    # Save file locally
    file_path = save_file(file)

    # Create document record
    document = create_document(
        db=db,
        user_id=user_id,
        filename=file.filename,
        file_path=file_path,
    )
     # NEW: Process document immediately
    process_document(
        db=db,
        document_id=int(document.id),          # Fix typing
        file_path=str(document.file_path),     # Fix typing
   )
    return document