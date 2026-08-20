from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID

class OrderItemBase(BaseModel):
    product_id: UUID
    variant_id: Optional[UUID] = None
    quantity: int
    options: Optional[Dict[str, Any]] = None
    unit_price: int
    total_price: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemRead(OrderItemBase):
    id: UUID
    order_id: UUID

    class Config:
        from_attributes = True