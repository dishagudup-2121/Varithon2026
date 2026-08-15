from sqlalchemy import Column, String, Boolean, Float, ForeignKey
from ..core.database import Base

class Resource(Base):
    __tablename__ = "resources"
    
    resource_id = Column(String, primary_key=True)
    resource_type = Column(String, nullable=False)
    zone_id = Column(String, ForeignKey('zones.zone_id'), nullable=False)
    available = Column(Boolean, default=True)
    eta_minutes = Column(Float, nullable=True)
