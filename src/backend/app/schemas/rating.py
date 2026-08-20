from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class RatingBase(BaseModel):
    customer_id: UUID
    rating: int  # 1 à 5
    comment: Optional[str] = None

class RatingCreate(RatingBase):
    pass

class RatingRead(RatingBase):
    id: UUID
    tenant_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True