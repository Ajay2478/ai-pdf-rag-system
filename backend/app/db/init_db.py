from app.db.base import Base
from app.db.session import engine

# Core models
from app.models.user import User
from app.models.document import Document
from app.models.document_chunk import DocumentChunk

from app.models.summary import Summary
from app.models.note import Note
from app.models.flashcard import Flashcard

from app.models.chat import ChatSession
from app.models.message import ChatMessage
from app.models.audit_log import AuditLog

def init_db():
    Base.metadata.create_all(bind=engine)