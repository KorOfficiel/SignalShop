import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base
from datetime import datetime

class AIState(Base):
    __tablename__ = "ai_states"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    state = Column(String)  # état interne de l'IA (ex: MENU, AWAITING_PRODUCT, etc.)
    context = Column(JSON)  # contexte récent, historique minimal
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)