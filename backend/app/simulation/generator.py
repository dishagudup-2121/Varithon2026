import random
import networkx as nx
from typing import List, Dict, Any
from datetime import datetime
from .pilgrim_model import PilgrimGroup

def generate_pilgrim_groups(
    graph: nx.DiGraph,
    zones_data: Dict[str, Any],
    simulation_time: datetime,
    count: int = 30,
    seed: int = 42,
    min_group_size: int = 50,
    max_group_size: int = 500,
    min_speed_mps: float = 0.5,
    max_speed_mps: float = 1.5
) -> List[PilgrimGroup]:
    """
    Deterministic synthetic generator for pilgrim groups.
    """
    rng = random.Random(seed)
    
    # Extract real zone IDs
    zone_ids = []
    for feature in zones_data.get('features', []):
        zid = feature.get('properties', {}).get('zone_id')
        if zid:
            zone_ids.append(zid)
            
    if not zone_ids:
        raise ValueError("No valid zones found in zones_data")
        
    # Find largest weakly connected component
    if graph.number_of_nodes() == 0:
        raise ValueError("Graph is empty")
        
    wcc = list(nx.weakly_connected_components(graph))
    largest_cc_nodes = max(wcc, key=len)
    
    # Extract valid edges from the largest component
    valid_edges = []
    for u, v, data in graph.edges(data=True):
        if u in largest_cc_nodes and v in largest_cc_nodes:
            if data.get('length_m', 0) > 0 and 'geometry' in data and len(data['geometry']) >= 2:
                valid_edges.append(data['edge_id'])
                
    if not valid_edges:
        raise ValueError("No valid edges found in the largest connected component")
        
    groups = []
    for i in range(count):
        group_id = f"G{i+1:03d}"
        group_count = rng.randint(min_group_size, max_group_size)
        speed = rng.uniform(min_speed_mps, max_speed_mps)
        
        # Spread groups across edges, allows sharing
        edge_id = rng.choice(valid_edges)
        
        dest_zone = rng.choice(zone_ids)
        
        # Progress spread across the edge
        progress = rng.uniform(0.0, 1.0)
        
        groups.append(PilgrimGroup(
            group_id=group_id,
            count=group_count,
            current_edge_id=edge_id,
            progress=progress,
            speed_mps=speed,
            status="moving",
            destination_zone_id=dest_zone,
            route=[],
            created_at=simulation_time,
            updated_at=simulation_time
        ))
        
    return groups
