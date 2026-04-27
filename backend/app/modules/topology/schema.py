from pydantic import BaseModel
from typing import Optional

class LinkCreate(BaseModel):
    source_switch_id: int
    source_port: str
    target_switch_id: int
    target_port: str
    description: Optional[str] = None

class LinkResponse(BaseModel):
    id: int
    source_switch_id: int
    source_port: str
    target_switch_id: int
    target_port: str
    description: Optional[str]
    class Config:
        from_attributes = True
