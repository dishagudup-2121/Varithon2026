from pydantic import BaseModel, Field
from typing import List, Literal
from datetime import datetime

class PilgrimGroup(BaseModel):
    group_id: str
    count: int = Field(gt=0)
    current_edge_id: str
    progress: float = Field(ge=0.0, le=1.0)
    speed_mps: float = Field(gt=0.0)
    status: Literal["moving", "stopped", "congested"]
    destination_zone_id: str
    route: List[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
