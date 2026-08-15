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
    Spawns groups geographically constrained to the Wari operational corridor.
    """
    rng = random.Random(seed)
    
    # Extract real zone IDs and compute bounding box
    zone_ids = []
    zone_lats = []
    zone_lons = []
    
    for feature in zones_data.get('features', []):
        zid = feature.get('properties', {}).get('zone_id')
        if zid:
            zone_ids.append(zid)
            
            center = feature.get('properties', {}).get('center')
            if center and len(center) >= 2:
                zone_lats.append(center[0])
                zone_lons.append(center[1])
            else:
                geom = feature.get('geometry')
                if geom and geom.get('type') == 'Polygon':
                    coords = geom.get('coordinates', [[]])[0]
                    if coords:
                        lats = [c[1] for c in coords]
                        lons = [c[0] for c in coords]
                        zone_lats.append(sum(lats)/len(lats))
                        zone_lons.append(sum(lons)/len(lons))
            
    if not zone_ids:
        raise ValueError("No valid zones found in zones_data")
        
    # Calculate ~2km buffer in degrees (approx 0.018 degrees)
    BUFFER_DEG = 0.02
    if zone_lats and zone_lons:
        min_lat = min(zone_lats) - BUFFER_DEG
        max_lat = max(zone_lats) + BUFFER_DEG
        min_lon = min(zone_lons) - BUFFER_DEG
        max_lon = max(zone_lons) + BUFFER_DEG
    else:
        min_lat, max_lat, min_lon, max_lon = -90, 90, -180, 180
        
    # Find largest weakly connected component
    if graph.number_of_nodes() == 0:
        raise ValueError("Graph is empty")
        
    wcc = list(nx.weakly_connected_components(graph))
    largest_cc_nodes = max(wcc, key=len)
    
    # Extract valid edges from the largest component that fall within the bounding box
    valid_edges = []
    for u, v, data in graph.edges(data=True):
        if u in largest_cc_nodes and v in largest_cc_nodes:
            if data.get('length_m', 0) > 0 and 'geometry' in data and len(data['geometry']) >= 2:
                u_node = graph.nodes.get(u)
                if u_node and 'lat' in u_node and 'lng' in u_node:
                    if min_lat <= u_node['lat'] <= max_lat and min_lon <= u_node['lng'] <= max_lon:
                        valid_edges.append(data['edge_id'])
                
    if not valid_edges:
        raise ValueError("No valid edges found in the constrained corridor")
        
    groups = []
    for i in range(count):
        group_id = f"G{i+1:03d}"
        group_count = rng.randint(min_group_size, max_group_size)
        speed = rng.uniform(min_speed_mps, max_speed_mps)
        
        # Spread groups across constrained edges
        edge_id = rng.choice(valid_edges)
        
        # Assign destinations weighted towards Z1 (Alandi Temple Core Zone)
        if 'Z1' in zone_ids and rng.random() < 0.5:
            dest_zone = 'Z1'
        else:
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
