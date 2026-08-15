from pydantic import BaseModel, ConfigDict
from typing import List

class ZonePrediction(BaseModel):
    zone_id: str
    risk_probability: float
    risk_level: str
    horizon_minutes: int = 30
    confidence_source: str
    
    model_config = ConfigDict(from_attributes=True)

class PredictResponse(BaseModel):
    predictions: List[ZonePrediction]
    model_version: str
    
    model_config = ConfigDict(from_attributes=True)
