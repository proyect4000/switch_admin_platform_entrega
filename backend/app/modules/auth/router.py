from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.core.security import create_access_token
from app.modules.auth.schema import LoginRequest, TokenResponse, UserAuthResponse
from app.modules.auth.service import authenticate_user
from app.modules.auth.dependencies import get_current_user
from app.modules.users.model import User

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    token = create_access_token({"sub": str(user.id), "email": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserAuthResponse)
def me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "name": current_user.name, "email": current_user.email, "role": current_user.role.name if current_user.role else None}
