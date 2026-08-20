import uuid
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Date, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base
from datetime import datetime

class Product(Base):
    __tablename__ = "products"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    image_url = Column(String)
    base_price = Column(Integer, nullable=False)  # en centimes
    unit = Column(String, default="unité")
    stock_mode = Column(String, default="illimited")  # illimited, limited, unavailable
    stock_quantity = Column(Integer)
    alert_threshold = Column(Integer)
    active = Column(Boolean, default=True)
    position = Column(Integer, default=0)
    availability_start = Column(Date)
    availability_end = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)