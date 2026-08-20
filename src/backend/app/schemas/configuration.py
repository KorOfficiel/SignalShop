from pydantic import BaseModel
from typing import Any
from uuid import UUID

class ConfigurationUpdate(BaseModel):
    value: Any

class ConfigurationRead(BaseModel):
    id: UUID
    tenant_id: UUID
    key: str
    value: Any

    class Config:
        from_attributes = True