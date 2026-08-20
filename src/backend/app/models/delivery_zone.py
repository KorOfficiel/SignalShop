import uuid
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base

class DeliveryZone(Base):
    __tablename__ = "delivery_zones"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    name = Column(String, nullable=False)
    fee = Column(Integer, nullable=False, default=0)  # en centimes
    min_order = Column(Integer, default=0)  # en centimes
    active = Column(Boolean, default=True)