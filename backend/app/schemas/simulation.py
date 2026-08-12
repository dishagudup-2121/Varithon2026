from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime

class GeoPosition(BaseModel):
    lat: float = Field(ge=-90.0, le=90.0)
    lng: float = Field(ge=-180.0, le=180.0)

class PilgrimGroupResponse(BaseModel):
    group_id: str
    count: int
    speed_mps: float
    progress: float
    status: Literal["moving", "stopped", "congested"]
    current_edge_id: str
    destination_zone_id: str
    updated_at: datetime
    position: Optional[GeoPosition] = None

class SimulationStateResponse(BaseModel):
    simulation_time: str
    tick: int
    groups: List[PilgrimGroupResponse]
