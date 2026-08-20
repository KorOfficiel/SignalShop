import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base

class OptionDefinition(Base):
    __tablename__ = "option_definitions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # single_choice, multiple_choice, text, number, boolean
    required = Column(Boolean, default=False)
    choices = Column(JSON)  # liste de choix pour single/multiple