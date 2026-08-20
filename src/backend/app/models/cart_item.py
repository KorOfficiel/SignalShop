import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base

class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cart_id = Column(UUID(as_uuid=True), ForeignKey("carts.id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    variant_id = Column(UUID(as_uuid=True), ForeignKey("variants.id"), nullable=True)
    quantity = Column(Integer, nullable=False, default=1)
    options = Column(JSON)  # stocke les options choisies
    unit_price = Column(Integer, nullable=False)  # en centimes
    total_price = Column(Integer, nullable=False)  # en centimes