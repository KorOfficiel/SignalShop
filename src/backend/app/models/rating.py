import uuid
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base
from datetime import datetime

class Rating(Base):
    __tablename__ = "ratings"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1 à 5
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)