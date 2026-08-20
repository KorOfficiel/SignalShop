from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import date

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    category_id: Optional[UUID] = None
    base_price: int  # en centimes
    unit: str = "unité"
    stock_mode: str = "illimited"  # illimited, limited, unavailable
    stock_quantity: Optional[int] = None
    alert_threshold: Optional[int] = None
    active: bool = True
    position: int = 0
    availability_start: Optional[date] = None
    availability_end: Optional[date] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    category_id: Optional[UUID] = None
    base_price: Optional[int] = None
    unit: Optional[str] = None
    stock_mode: Optional[str] = None
    stock_quantity: Optional[int] = None
    alert_threshold: Optional[int] = None
    active: Optional[bool] = None
    position: Optional[int] = None
    availability_start: Optional[date] = None
    availability_end: Optional[date] = None

class ProductRead(ProductBase):
    id: UUID
    tenant_id: UUID

    class Config:
        from_attributes = True