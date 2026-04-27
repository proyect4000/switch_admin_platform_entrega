from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class SwitchCreate(BaseModel):
    name: str
    ip_address: str
    brand: Optional[str] = None
    model: Optional[str] = None
    location: Optional[str] = None
    ssh_port: int = 22
    ssh_username: str
    ssh_password: str = Field(min_length=1)

class SwitchUpdate(BaseModel):
    name: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    location: Optional[str] = None
    ssh_port: Optional[int] = None
    ssh_username: Optional[str] = None
    ssh_password: Optional[str] = None

class SwitchResponse(BaseModel):
    id: int
    name: str
    ip_address: str
    brand: Optional[str]
    model: Optional[str]
    location: Optional[str]
    ssh_port: int
    ssh_username: str
    status: str
    last_seen_at: Optional[datetime]
    class Config:
        from_attributes = True
