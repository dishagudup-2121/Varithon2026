from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any
from datetime import datetime

class ApproveRequest(BaseModel):
    recommendation_id: str
    decision: str
    modified_assignments: List[Dict[str, Any]] = []
    
    model_config = ConfigDict(from_attributes=True)

class ApproveResponse(BaseModel):
    status: str
    recommendation_id: str
    decision: str
    logged_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
