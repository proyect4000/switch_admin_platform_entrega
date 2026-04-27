from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database.base import Base

class AvailabilityLog(Base):
    __tablename__ = "availability_logs"
    id = Column(Integer, primary_key=True, index=True)
    switch_id = Column(Integer, ForeignKey("switches.id"), nullable=False)
    status = Column(String(30), nullable=False)
    latency_ms = Column(Float, nullable=True)
    message = Column(String(255), nullable=True)
    checked_at = Column(DateTime(timezone=True), server_default=func.now())
