from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class TimeSlotBase(BaseModel):
    start_time: datetime
    end_time: datetime
    capacity: int = 1
    active: bool = True

class TimeSlotCreate(TimeSlotBase):
    pass

class TimeSlotUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    capacity: Optional[int] = None
    active: Optional[bool] = None

class TimeSlotRead(TimeSlotBase):
    id: UUID
    tenant_id: UUID
    booked_count: int

    class Config:
        from_attributes = True