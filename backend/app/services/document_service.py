from sqlalchemy.orm import Session
from app.models.document import Document


def create_document(
    db: Session,
    user_id: int,
    filename: str,
    file_path: str,
):
    """
    Create document record in DB
    """

    document = Document(
        user_id=user_id,
        filename=filename,
        file_path=file_path,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document