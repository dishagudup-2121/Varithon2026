from pydantic import BaseModel, ConfigDict
from typing import List

class Assignment(BaseModel):
    resource_id: str
    resource_type: str
    from_zone_id: str
    to_zone_id: str
    eta_minutes: float
    reason: str
    
    model_config = ConfigDict(from_attributes=True)

class RecommendResponse(BaseModel):
    recommendation_id: str
    target_zone_id: str
    assignments: List[Assignment]
    optimization_method: str = 'OR-Tools'
    
    model_config = ConfigDict(from_attributes=True)

class FullRecommendResponse(BaseModel):
    recommendations: List[RecommendResponse]
    
    model_config = ConfigDict(from_attributes=True)
