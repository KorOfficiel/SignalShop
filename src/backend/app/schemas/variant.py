from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class VariantBase(BaseModel):
    product_id: UUID
    name: str
    description: Optional[str] = None
    price_modifier: int = 0
    price_override: Optional[int] = None
    stock_quantity: Optional[int] = None
    reference: Optional[str] = None
    image_url: Optional[str] = None
    active: bool = True

class VariantCreate(VariantBase):
    pass

class VariantUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price_modifier: Optional[int] = None
    price_override: Optional[int] = None
    stock_quantity: Optional[int] = None
    reference: Optional[str] = None
    image_url: Optional[str] = None
    active: Optional[bool] = None

class VariantRead(VariantBase):
    id: UUID

    class Config:
        from_attributes = True