from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.modules.auth.dependencies import require_role
from app.modules.monitoring.model import AvailabilityLog

router = APIRouter(prefix="/api/monitoring", tags=["Monitoring"])

@router.get("/availability")
def availability_history(db: Session = Depends(get_db), user=Depends(require_role(["Administrador", "Operador", "Visor"]))):
    return db.query(AvailabilityLog).order_by(AvailabilityLog.checked_at.desc()).limit(200).all()

@router.get("/availability/switch/{switch_id}")
def availability_by_switch(switch_id: int, db: Session = Depends(get_db), user=Depends(require_role(["Administrador", "Operador", "Visor"]))):
    return db.query(AvailabilityLog).filter(AvailabilityLog.switch_id == switch_id).order_by(AvailabilityLog.checked_at.desc()).limit(100).all()
