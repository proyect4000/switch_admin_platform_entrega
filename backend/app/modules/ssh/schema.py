from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ExecuteCommandRequest(BaseModel):
    switch_id: int
    command: str

class ExecuteCommandResponse(BaseModel):
    switch_id: int
    command: str
    output: Optional[str]
    success: bool
    error_message: Optional[str] = None

class CommandHistoryResponse(BaseModel):
    id: int
    user_id: int
    switch_id: int
    command: str
    output: Optional[str]
    success: bool
    error_message: Optional[str]
    executed_at: datetime
    class Config:
        from_attributes = True
