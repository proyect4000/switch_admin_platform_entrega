from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database.base import Base

class Switch(Base):
    __tablename__ = "switches"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    ip_address = Column(String(50), unique=True, nullable=False)
    brand = Column(String(100), nullable=True)
    model = Column(String(100), nullable=True)
    location = Column(String(150), nullable=True)
    ssh_port = Column(Integer, default=22)
    ssh_username = Column(String(100), nullable=False)
    ssh_password_encrypted = Column(String(500), nullable=False)
    status = Column(String(30), default="offline")
    last_seen_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
