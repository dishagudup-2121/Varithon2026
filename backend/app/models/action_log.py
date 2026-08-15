from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from ..core.database import Base

class ActionLog(Base):
    __tablename__ = "action_logs"
    
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    recommendation_id = Column(String, ForeignKey('recommendations.recommendation_id'), nullable=False)
    decision = Column(String, nullable=False)
    modified_assignments = Column(Text, nullable=True)
    decided_at = Column(DateTime, server_default=func.now())
    decided_by = Column(String, default='dashboard_user')
