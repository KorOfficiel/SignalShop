import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base
from datetime import datetime

class Order(Base):
    __tablename__ = "orders"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    status = Column(String, nullable=False, default="DRAFT")  # DRAFT, PENDING_CONFIRMATION, CONFIRMED, etc.
    total_amount = Column(Integer, nullable=False)  # en centimes
    delivery_fee = Column(Integer, default=0)  # en centimes
    delivery_zone_id = Column(UUID(as_uuid=True), ForeignKey("delivery_zones.id"), nullable=True)
    delivery_address = Column(JSON)  # adresse complète
    delivery_instructions = Column(String)
    scheduled_slot_id = Column(UUID(as_uuid=True), ForeignKey("time_slots.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)