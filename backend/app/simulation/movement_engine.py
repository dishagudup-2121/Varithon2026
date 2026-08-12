from pydantic import BaseModel
from typing import Optional
import networkx as nx
import math
from datetime import timedelta
from .pilgrim_model import PilgrimGroup

class MovementResult(BaseModel):
    group: PilgrimGroup
    distance_moved_m: float
    edges_traversed: int
    arrived: bool
    success: bool
    reason: Optional[str] = None

def tick_movement(graph: nx.DiGraph, group: PilgrimGroup, delta_time_s: float) -> MovementResult:
    # 1. Delta Time Validation
    if not math.isfinite(delta_time_s) or delta_time_s < 0:
        return MovementResult(
            group=group, 
            distance_moved_m=0.0, 
            edges_traversed=0, 
            arrived=False, 
            success=False, 
            reason="invalid_delta_time"
        )
        
    # 2. Status check
    if group.status != "moving":
        return MovementResult(
            group=group, 
            distance_moved_m=0.0, 
            edges_traversed=0, 
            arrived=(group.status == "stopped"), 
            success=True, 
            reason="group_not_moving"
        )

    # 3. Progress Validation
    if not (0.0 <= group.progress <= 1.0):
        return MovementResult(
            group=group, 
            distance_moved_m=0.0, 
            edges_traversed=0, 
            arrived=False, 
            success=False, 
            reason="invalid_progress"
        )

    distance_to_move_m = group.speed_mps * delta_time_s
    distance_moved = 0.0
    edges_traversed = 0
    
    # Helper to resolve an edge_id to its properties
    def resolve_edge(edge_id: str):
        for edge_u, edge_v, data in graph.edges(data=True):
            if data.get('edge_id') == edge_id:
                return edge_u, edge_v, data.get('length_m')
        return None, None, None

    while distance_to_move_m > 0:
        u, v, length_m = resolve_edge(group.current_edge_id)
        
        if u is None or length_m is None or length_m <= 0:
            group.status = "stopped"
            reason = "invalid_current_edge" if u is None else "invalid_current_edge_length"
            return MovementResult(
                group=group, 
                distance_moved_m=distance_moved, 
                edges_traversed=edges_traversed, 
                arrived=False, 
                success=False, 
                reason=reason
            )
            
        remaining_m = (1.0 - group.progress) * length_m
        
        if distance_to_move_m < remaining_m:
            # Does not cross boundary
            group.progress += distance_to_move_m / length_m
            distance_moved += distance_to_move_m
            distance_to_move_m = 0.0
            break
        else:
            # Crosses boundary
            distance_to_move_m -= remaining_m
            distance_moved += remaining_m
            group.progress = 1.0
            
            if not group.route:
                # Reached end of route
                group.status = "stopped"
                # Keep progress at 1.0
                return MovementResult(
                    group=group, 
                    distance_moved_m=distance_moved, 
                    edges_traversed=edges_traversed, 
                    arrived=True, 
                    success=True, 
                    reason=None
                )
                
            # Peek next edge
            next_edge_id = group.route[0]
            next_u, next_v, next_length_m = resolve_edge(next_edge_id)
            
            if next_u is None:
                group.status = "stopped"
                return MovementResult(
                    group=group, 
                    distance_moved_m=distance_moved, 
                    edges_traversed=edges_traversed, 
                    arrived=False, 
                    success=False, 
                    reason="invalid_route_edge"
                )
                
            if next_u != v:
                group.status = "stopped"
                return MovementResult(
                    group=group, 
                    distance_moved_m=distance_moved, 
                    edges_traversed=edges_traversed, 
                    arrived=False, 
                    success=False, 
                    reason="route_edge_disconnected"
                )
                
            if next_length_m is None or next_length_m <= 0:
                group.status = "stopped"
                return MovementResult(
                    group=group, 
                    distance_moved_m=distance_moved, 
                    edges_traversed=edges_traversed, 
                    arrived=False, 
                    success=False, 
                    reason="invalid_route_edge_length"
                )
                
            # All validation succeeded, consume it
            group.route.pop(0)
            group.current_edge_id = next_edge_id
            group.progress = 0.0
            edges_traversed += 1

    group.updated_at += timedelta(seconds=delta_time_s)
    
    return MovementResult(
        group=group, 
        distance_moved_m=distance_moved, 
        edges_traversed=edges_traversed, 
        arrived=False, 
        success=True, 
        reason=None
    )
