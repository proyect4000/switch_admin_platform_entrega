from fastapi import APIRouter, WebSocket, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.modules.ssh.websocket_service import ssh_websocket_console

router = APIRouter(prefix="/ws/ssh", tags=["SSH WebSocket"])

@router.websocket("/{switch_id}")
async def ssh_console(websocket: WebSocket, switch_id: int, db: Session = Depends(get_db)):
    await ssh_websocket_console(websocket, db, switch_id)
