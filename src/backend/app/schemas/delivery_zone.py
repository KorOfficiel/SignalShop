from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class DeliveryZoneBase(BaseModel):
    name: str
    fee: int = 0
    min_order: int = 0
    active: bool = True

class DeliveryZoneCreate(DeliveryZoneBase):
    pass

class DeliveryZoneUpdate(BaseModel):
    name: Optional[str] = None
    fee: Optional[int] = None
    min_order: Optional[int] = None
    active: Optional[bool] = None

class DeliveryZoneRead(DeliveryZoneBase):
    id: UUID
    tenant_id: UUID

    class Config:
        from_attributes = True