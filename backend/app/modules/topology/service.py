from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.modules.topology.model import SwitchLink

def get_topology(db: Session):
    return db.query(SwitchLink).all()

def create_link(db: Session, payload):
    link = SwitchLink(**payload.model_dump())
    db.add(link); db.commit(); db.refresh(link)
    return link

def delete_link(db: Session, link_id: int):
    link = db.query(SwitchLink).filter(SwitchLink.id == link_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Enlace no encontrado")
    db.delete(link); db.commit()
    return {"message": "Enlace eliminado correctamente"}
