from pydantic import BaseModel
from typing import List
from ..simulation.pilgrim_model import PilgrimGroup

class SimulationStateResponse(BaseModel):
    simulation_time: str
    tick: int
    groups: List[PilgrimGroup]
