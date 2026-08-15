from sqlalchemy import Column, String, Float, Integer
from ..core.database import Base

class Zone(Base):
    __tablename__ = "zones"
    
    zone_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    crowd_count = Column(Integer, default=0)
    temperature_c = Column(Float, default=35.0)
    humidity_percent = Column(Float, default=50.0)
    water_availability_percent = Column(Float, default=80.0)
