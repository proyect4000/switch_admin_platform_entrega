from pydantic import BaseModel, EmailStr
from typing import Optional

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserAuthResponse(BaseModel):
    id: int
    name: str
    email: str
    role: Optional[str] = None
