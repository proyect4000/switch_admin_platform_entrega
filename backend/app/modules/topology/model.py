from sqlalchemy import Column, Integer, ForeignKey, String
from app.database.base import Base

class SwitchLink(Base):
    __tablename__ = "switch_links"
    id = Column(Integer, primary_key=True, index=True)
    source_switch_id = Column(Integer, ForeignKey("switches.id"), nullable=False)
    source_port = Column(String(50), nullable=False)
    target_switch_id = Column(Integer, ForeignKey("switches.id"), nullable=False)
    target_port = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
