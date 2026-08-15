from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any

class SimulateRequest(BaseModel):
    action: str
    route_id: Optional[str] = None
    extra_volunteers: int = 0
    
    model_config = ConfigDict(from_attributes=True)

class SimulationMetrics(BaseModel):
    congestion_percent: float
    avg_eta_minutes: float
    medical_access_percent: float
    
    model_config = ConfigDict(from_attributes=True)

class SimulateResponse(BaseModel):
    scenario: Dict[str, Any]
    before: SimulationMetrics
    after: SimulationMetrics
    delta: SimulationMetrics
    simulation_method: str
    calibration_note: str
    
    model_config = ConfigDict(from_attributes=True)
