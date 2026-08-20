from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class CartBase(BaseModel):
    customer_id: UUID
    status: str = "ACTIVE"

class CartCreate(CartBase):
    pass

class CartRead(CartBase):
    id: UUID
    tenant_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True