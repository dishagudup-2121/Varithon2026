from typing import List, Optional
from pydantic import BaseModel
from ..schemas.crowd import TemporalCrowdSnapshot

class EdgeFeatures(BaseModel):
    edge_id: str
    tick: int
    current_load: int
    load_t_minus_1: int
    load_t_minus_5: int
    load_t_minus_15: int
    absolute_load_change_1: int
    absolute_load_change_5: int
    absolute_load_change_15: int
    consecutive_occupied_ticks: int

def get_edge_load(snapshot: TemporalCrowdSnapshot, edge_id: str) -> int:
    """
    Deterministically retrieves the load of an edge from a sparse snapshot.
    If the edge is absent, its load is strictly 0.
    """
    for edge in snapshot.snapshot.edges:
        if edge.edge_id == edge_id:
            return edge.pilgrim_count
    return 0

def extract_features(
    history: List[TemporalCrowdSnapshot], 
    target_edge_id: str, 
    current_tick: int
) -> Optional[EdgeFeatures]:
    """
    Extracts features for a given edge at a specific tick.
    Returns None if history is insufficient (e.g., tick - 15 is missing).
    Features MUST NOT include any information > current_tick.
    """
    # 1. Build a fast lookup for tick -> snapshot
    snapshot_map = {snap.tick: snap for snap in history}
    
    if current_tick not in snapshot_map:
        return None
        
    # 2. Check if we have sufficient history (T-15)
    if (current_tick - 15) not in snapshot_map:
        return None
        
    # Ensure T-1 and T-5 also exist to build a complete feature vector
    if (current_tick - 1) not in snapshot_map or (current_tick - 5) not in snapshot_map:
        return None

    # 3. Extract loads (sparse edges safely return 0)
    load_current = get_edge_load(snapshot_map[current_tick], target_edge_id)
    load_t_1 = get_edge_load(snapshot_map[current_tick - 1], target_edge_id)
    load_t_5 = get_edge_load(snapshot_map[current_tick - 5], target_edge_id)
    load_t_15 = get_edge_load(snapshot_map[current_tick - 15], target_edge_id)
    
    # 4. Calculate consecutive occupied ticks
    # Count backwards from current_tick until load == 0 or we hit the beginning of available history
    consecutive = 0
    t = current_tick
    while t in snapshot_map:
        if get_edge_load(snapshot_map[t], target_edge_id) > 0:
            consecutive += 1
            t -= 1
        else:
            break
            
    # 5. Return deterministic features
    return EdgeFeatures(
        edge_id=target_edge_id,
        tick=current_tick,
        current_load=load_current,
        load_t_minus_1=load_t_1,
        load_t_minus_5=load_t_5,
        load_t_minus_15=load_t_15,
        absolute_load_change_1=load_current - load_t_1,
        absolute_load_change_5=load_current - load_t_5,
        absolute_load_change_15=load_current - load_t_15,
        consecutive_occupied_ticks=consecutive
    )
