from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime, timezone
from app.modules.switches.model import Switch
from app.modules.switches.schema import SwitchCreate, SwitchUpdate
from app.core.encryption import encrypt_text
from app.modules.ssh.service import validate_ssh_connection

def get_switches(db: Session):
    return db.query(Switch).order_by(Switch.id.desc()).all()

def get_switch_by_id(db: Session, switch_id: int):
    switch = db.query(Switch).filter(Switch.id == switch_id).first()
    if not switch:
        raise HTTPException(status_code=404, detail="Switch no encontrado")
    return switch

def create_switch(db: Session, payload: SwitchCreate):
    existing = db.query(Switch).filter(Switch.ip_address == payload.ip_address).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe un switch registrado con esta IP")
    is_valid, message = validate_ssh_connection(payload.ip_address, payload.ssh_username, payload.ssh_password, payload.ssh_port)
    status = "online" if is_valid else "error"
    if not is_valid:
        # Para ambientes institucionales, no bloqueamos el alta: queda registrado como error para corrección posterior.
        # Cambie esta política si desea exigir SSH exitoso antes de guardar.
        pass
    switch = Switch(
        name=payload.name, ip_address=payload.ip_address, brand=payload.brand, model=payload.model, location=payload.location,
        ssh_port=payload.ssh_port, ssh_username=payload.ssh_username, ssh_password_encrypted=encrypt_text(payload.ssh_password),
        status=status, last_seen_at=datetime.now(timezone.utc) if status == "online" else None
    )
    db.add(switch); db.commit(); db.refresh(switch)
    return switch

def update_switch(db: Session, switch_id: int, payload: SwitchUpdate):
    switch = get_switch_by_id(db, switch_id)
    data = payload.model_dump(exclude_unset=True)
    if "ssh_password" in data:
        if data["ssh_password"]:
            switch.ssh_password_encrypted = encrypt_text(data["ssh_password"])
        del data["ssh_password"]
    for key, value in data.items():
        setattr(switch, key, value)
    db.commit(); db.refresh(switch)
    return switch

def delete_switch(db: Session, switch_id: int):
    switch = get_switch_by_id(db, switch_id)
    db.delete(switch); db.commit()
    return {"message": "Switch eliminado correctamente"}
