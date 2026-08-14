from pydantic import BaseModel
from typing import List

class CrowdEdgeLoad(BaseModel):
    edge_id: str
    pilgrim_count: int
    group_count: int
    moving_group_count: int
    stopped_group_count: int
    congested_group_count: int

class CrowdSummary(BaseModel):
    total_pilgrims: int
    total_groups: int
    active_edge_count: int
    moving_group_count: int
    stopped_group_count: int
    congested_group_count: int
    unresolved_group_count: int

class CrowdStateSnapshot(BaseModel):
    summary: CrowdSummary
    edges: List[CrowdEdgeLoad]

class TemporalCrowdSnapshot(BaseModel):
    tick: int
    simulation_time: str
    snapshot: CrowdStateSnapshot
