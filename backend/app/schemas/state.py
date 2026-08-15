from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List

class ZoneState(BaseModel):
    zone_id: str
    name: str
    lat: float
    lng: float
    crowd_count: int
    temperature_c: float
    humidity_percent: float
    water_availability_percent: float
    
    model_config = ConfigDict(from_attributes=True)

class AgentState(BaseModel):
    agent_id: str
    count: int
    lat: float
    lng: float
    route_id: str
    status: str
    
    model_config = ConfigDict(from_attributes=True)

class ResourceState(BaseModel):
    resource_id: str
    resource_type: str
    zone_id: str
    available: bool
    
    model_config = ConfigDict(from_attributes=True)

class SystemState(BaseModel):
    timestamp: datetime
    zones: List[ZoneState]
    agents: List[AgentState]
    resources: List[ResourceState]
    
    model_config = ConfigDict(from_attributes=True)
