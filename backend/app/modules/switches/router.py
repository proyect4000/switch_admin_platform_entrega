from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.modules.switches.schema import SwitchCreate, SwitchUpdate, SwitchResponse
from app.modules.switches.service import get_switches, get_switch_by_id, create_switch, update_switch, delete_switch
from app.modules.auth.dependencies import require_role

router = APIRouter(prefix="/api/switches", tags=["Switches"])

@router.get("/", response_model=list[SwitchResponse])
def list_switches(db: Session = Depends(get_db), user=Depends(require_role(["Administrador", "Operador", "Visor"]))):
    return get_switches(db)

@router.get("/{switch_id}", response_model=SwitchResponse)
def show_switch(switch_id: int, db: Session = Depends(get_db), user=Depends(require_role(["Administrador", "Operador", "Visor"]))):
    return get_switch_by_id(db, switch_id)

@router.post("/", response_model=SwitchResponse)
def store_switch(payload: SwitchCreate, db: Session = Depends(get_db), user=Depends(require_role(["Administrador", "Operador"]))):
    return create_switch(db, payload)

@router.put("/{switch_id}", response_model=SwitchResponse)
def edit_switch(switch_id: int, payload: SwitchUpdate, db: Session = Depends(get_db), user=Depends(require_role(["Administrador", "Operador"]))):
    return update_switch(db, switch_id, payload)

@router.delete("/{switch_id}")
def remove_switch(switch_id: int, db: Session = Depends(get_db), user=Depends(require_role(["Administrador"]))):
    return delete_switch(db, switch_id)
