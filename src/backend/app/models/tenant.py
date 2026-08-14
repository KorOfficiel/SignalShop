import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base
from datetime import datetime

class Tenant(Base):
    __tablename__ = "tenants"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    timezone = Column(String, default="Europe/Paris")
    created_at = Column(DateTime, default=datetime.utcnow)