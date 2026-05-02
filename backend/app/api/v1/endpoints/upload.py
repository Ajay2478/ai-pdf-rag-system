from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import cast

from app.api.deps import get_db, get_current_user
from app.services.upload_service import handle_file_upload
from app.models.user import User

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("/")
def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Upload PDF and store it
    """

    # Validate file type
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    # Fix typing issue properly
    user_id = cast(int, current_user.id)

    document = handle_file_upload(
        db=db,
        user_id=user_id,
        file=file,
    )

    return {
        "message": "File uploaded successfully",
        "document_id": document.id,
        "filename": document.filename,
    }