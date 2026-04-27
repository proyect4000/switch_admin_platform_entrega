from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database.base import Base

class CommandHistory(Base):
    __tablename__ = "command_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    switch_id = Column(Integer, ForeignKey("switches.id"), nullable=False)
    command = Column(String(500), nullable=False)
    output = Column(Text, nullable=True)
    success = Column(Boolean, default=True)
    error_message = Column(Text, nullable=True)
    executed_at = Column(DateTime(timezone=True), server_default=func.now())
