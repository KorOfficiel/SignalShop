from pydantic import BaseModel
from typing import Optional, List, Any
from uuid import UUID

class OptionDefinitionBase(BaseModel):
    product_id: UUID
    name: str
    type: str  # single_choice, multiple_choice, text, number, boolean
    required: bool = False
    choices: Optional[List[str]] = None  # liste des choix pour single/multiple

class OptionDefinitionCreate(OptionDefinitionBase):
    pass

class OptionDefinitionUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    required: Optional[bool] = None
    choices: Optional[List[str]] = None

class OptionDefinitionRead(OptionDefinitionBase):
    id: UUID

    class Config:
        from_attributes = True