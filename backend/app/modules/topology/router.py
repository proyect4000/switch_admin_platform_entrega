from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.modules.auth.dependencies import require_role
from app.modules.topology.service import get_topology, create_link, delete_link
from app.modules.topology.schema import LinkCreate, LinkResponse

router = APIRouter(prefix="/api/topology", tags=["Topology"])

@router.get("/", response_model=list[LinkResponse])
def topology(db: Session = Depends(get_db), user=Depends(require_role(["Administrador", "Operador", "Visor"]))):
    return get_topology(db)

@router.post("/", response_model=LinkResponse)
def add_link(payload: LinkCreate, db: Session = Depends(get_db), user=Depends(require_role(["Administrador", "Operador"]))):
    return create_link(db, payload)

@router.delete("/{link_id}")
def remove_link(link_id: int, db: Session = Depends(get_db), user=Depends(require_role(["Administrador", "Operador"]))):
    return delete_link(db, link_id)
