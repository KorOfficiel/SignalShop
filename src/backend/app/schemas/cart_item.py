from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID

class CartItemBase(BaseModel):
    product_id: UUID
    variant_id: Optional[UUID] = None
    quantity: int = 1
    options: Optional[Dict[str, Any]] = None

class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(BaseModel):
    quantity: Optional[int] = None
    variant_id: Optional[UUID] = None
    options: Optional[Dict[str, Any]] = None

class CartItemRead(CartItemBase):
    id: UUID
    cart_id: UUID
    unit_price: int
    total_price: int

    class Config:
        from_attributes = True