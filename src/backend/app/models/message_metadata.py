import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base
from datetime import datetime

class MessageMetadata(Base):
    __tablename__ = "message_metadata"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    sender = Column(String, nullable=False)  # customer, professional, system, ai
    timestamp = Column(DateTime, default=datetime.utcnow)
    content_hash = Column(String)
    content_length = Column(Integer)
    content = Column(Text)