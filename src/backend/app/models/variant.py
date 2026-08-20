import uuid
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base

class Variant(Base):
    __tablename__ = "variants"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    price_modifier = Column(Integer, default=0)  # supplément en centimes
    price_override = Column(Integer)  # prix fixe alternatif en centimes
    stock_quantity = Column(Integer)
    reference = Column(String)
    image_url = Column(String)
    active = Column(Boolean, default=True)