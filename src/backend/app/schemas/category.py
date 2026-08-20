from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    position: int = 0
    active: bool = True

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    position: Optional[int] = None
    active: Optional[bool] = None

class CategoryRead(CategoryBase):
    id: UUID
    tenant_id: UUID

    class Config:
        from_attributes = True