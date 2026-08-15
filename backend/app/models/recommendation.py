from sqlalchemy import Column, String, Text, DateTime, func
from ..core.database import Base

class Recommendation(Base):
    __tablename__ = "recommendations"
    
    recommendation_id = Column(String, primary_key=True)
    target_zone_id = Column(String, nullable=False)
    assignments = Column(Text, nullable=False)
    optimization_method = Column(String, default='OR-Tools')
    created_at = Column(DateTime, server_default=func.now())
    status = Column(String, default='pending')
