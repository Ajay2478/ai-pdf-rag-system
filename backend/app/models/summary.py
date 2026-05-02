from sqlalchemy import Column, Integer, Text, ForeignKey, String
from app.db.base import Base


class Summary(Base):
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True, index=True)

    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"))

    # AI output
    content = Column(Text, nullable=False)

    # summary type
    summary_type = Column(String(50), default="short")
    # short | detailed | bullets