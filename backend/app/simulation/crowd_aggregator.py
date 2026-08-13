import networkx as nx
from typing import List, Dict
from .pilgrim_model import PilgrimGroup
from ..schemas.crowd import CrowdEdgeLoad, CrowdSummary, CrowdStateSnapshot

def aggregate_crowd(graph: nx.DiGraph, groups: List[PilgrimGroup]) -> CrowdStateSnapshot:
    """
    Deterministically computes edge-level crowd loads from PilgrimGroup state.
    Does NOT mutate graph or groups.
    Zero-load edges are omitted. Results are sorted by edge_id.
    """
    
    # 1. Build authoritative valid edge lookup
    valid_edge_ids = set()
    for _, _, edata in graph.edges(data=True):
        edge_id = edata.get("edge_id")
        if edge_id:
            valid_edge_ids.add(edge_id)
            
    edge_aggregates: Dict[str, CrowdEdgeLoad] = {}
    
    # Track summary
    total_pilgrims = 0
    total_groups = len(groups)
    moving_group_count = 0
    stopped_group_count = 0
    congested_group_count = 0
    unresolved_group_count = 0
    
    for g in groups:
        total_pilgrims += g.count
        
        # update summary statuses
        if g.status == "moving":
            moving_group_count += 1
        elif g.status == "stopped":
            stopped_group_count += 1
        elif g.status == "congested":
            congested_group_count += 1
            
        edge_id = g.current_edge_id
        
        # validate edge id
        if edge_id not in valid_edge_ids:
            unresolved_group_count += 1
            continue
            
        if edge_id not in edge_aggregates:
            edge_aggregates[edge_id] = CrowdEdgeLoad(
                edge_id=edge_id,
                pilgrim_count=0,
                group_count=0,
                moving_group_count=0,
                stopped_group_count=0,
                congested_group_count=0
            )
            
        agg = edge_aggregates[edge_id]
        agg.pilgrim_count += g.count
        agg.group_count += 1
        
        if g.status == "moving":
            agg.moving_group_count += 1
        elif g.status == "stopped":
            agg.stopped_group_count += 1
        elif g.status == "congested":
            agg.congested_group_count += 1

    edges_list = list(edge_aggregates.values())
    edges_list.sort(key=lambda x: x.edge_id)
    
    summary = CrowdSummary(
        total_pilgrims=total_pilgrims,
        total_groups=total_groups,
        active_edge_count=len(edges_list),
        moving_group_count=moving_group_count,
        stopped_group_count=stopped_group_count,
        congested_group_count=congested_group_count,
        unresolved_group_count=unresolved_group_count
    )
    
    return CrowdStateSnapshot(summary=summary, edges=edges_list)
