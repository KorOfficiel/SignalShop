from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class CustomerBase(BaseModel):
    signal_phone_hash: str

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    signal_phone_hash: Optional[str] = None

class CustomerRead(CustomerBase):
    id: UUID
    tenant_id: UUID

    class Config:
        from_attributes = True