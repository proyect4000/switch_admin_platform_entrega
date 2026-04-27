from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.modules.auth.dependencies import require_role
from app.modules.users.model import User
from app.modules.ssh.schema import ExecuteCommandRequest, ExecuteCommandResponse, CommandHistoryResponse
from app.modules.ssh.command_service import execute_ssh_command, get_command_history, get_switch_command_history

router = APIRouter(prefix="/api/ssh", tags=["SSH"])

@router.post("/execute", response_model=ExecuteCommandResponse)
def execute_command(payload: ExecuteCommandRequest, db: Session = Depends(get_db), current_user: User = Depends(require_role(["Administrador", "Operador"]))):
    return execute_ssh_command(db, current_user.id, payload.switch_id, payload.command)

@router.get("/history", response_model=list[CommandHistoryResponse])
def history(db: Session = Depends(get_db), current_user: User = Depends(require_role(["Administrador", "Operador", "Visor"]))):
    return get_command_history(db)

@router.get("/history/switch/{switch_id}", response_model=list[CommandHistoryResponse])
def history_by_switch(switch_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_role(["Administrador", "Operador", "Visor"]))):
    return get_switch_command_history(db, switch_id)
