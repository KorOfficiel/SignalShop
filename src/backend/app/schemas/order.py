from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from app.schemas.order_item import OrderItemRead

class OrderBase(BaseModel):
    customer_id: UUID
    status: str = "DRAFT"
    delivery_zone_id: Optional[UUID] = None
    delivery_address: Optional[Dict[str, Any]] = None
    delivery_instructions: Optional[str] = None
    scheduled_slot_id: Optional[UUID] = None

class OrderCreate(BaseModel):
    cart_id: Optional[UUID] = None
    delivery_zone_id: Optional[UUID] = None
    delivery_address: Optional[Dict[str, Any]] = None
    delivery_instructions: Optional[str] = None
    scheduled_slot_id: Optional[UUID] = None
    status: str = "DRAFT"

class DirectOrderItem(BaseModel):
    product_id: UUID
    variant_id: Optional[UUID] = None
    quantity: int = 1
    options: Optional[Dict[str, Any]] = None

class DirectOrderCreate(BaseModel):
    customer_id: UUID
    items: List[DirectOrderItem]
    delivery_zone_id: Optional[UUID] = None
    delivery_address: Optional[Dict[str, Any]] = None
    delivery_instructions: Optional[str] = None
    scheduled_slot_id: Optional[UUID] = None
    status: str = "CONFIRMED"

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    delivery_address: Optional[Dict[str, Any]] = None
    delivery_instructions: Optional[str] = None
    scheduled_slot_id: Optional[UUID] = None

class OrderRead(OrderBase):
    id: UUID
    tenant_id: UUID
    total_amount: int
    delivery_fee: int
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemRead] = []

    class Config:
        from_attributes = True