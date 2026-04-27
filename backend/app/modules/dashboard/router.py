from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.modules.auth.dependencies import require_role
from app.modules.switches.model import Switch
from app.modules.ssh.command_model import CommandHistory
from app.modules.monitoring.model import AvailabilityLog

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/summary")
def dashboard_summary(db: Session = Depends(get_db), user=Depends(require_role(["Administrador", "Operador", "Visor"]))):
    return {
        "total_switches": db.query(Switch).count(),
        "online": db.query(Switch).filter(Switch.status == "online").count(),
        "offline": db.query(Switch).filter(Switch.status == "offline").count(),
        "error": db.query(Switch).filter(Switch.status == "error").count(),
        "warning": db.query(Switch).filter(Switch.status == "warning").count(),
        "last_commands": db.query(CommandHistory).order_by(CommandHistory.executed_at.desc()).limit(10).all(),
        "last_availability": db.query(AvailabilityLog).order_by(AvailabilityLog.checked_at.desc()).limit(10).all()
    }
