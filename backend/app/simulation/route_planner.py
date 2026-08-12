import networkx as nx
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from .pilgrim_model import PilgrimGroup
import math

class RouteResult(BaseModel):
    group_id: str
    status: str
    reason: Optional[str] = None
    start_node: Optional[str] = None
    target_node: Optional[str] = None
    node_ids: List[str] = Field(default_factory=list)
    edge_ids: List[str] = Field(default_factory=list)
    total_distance_m: float = 0.0

def calculate_haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371000.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def _get_zone_center(zones_data: Dict[str, Any], zone_id: str):
    for feature in zones_data.get('features', []):
        if feature.get('properties', {}).get('zone_id') == zone_id:
            center = feature.get('properties', {}).get('center')
            if center and len(center) >= 2:
                # Based on zones.json schema, center is [lat, lon]
                return center[0], center[1]
            geom = feature.get('geometry')
            if geom and geom.get('type') == 'Polygon':
                coords = geom.get('coordinates', [[]])[0]
                if coords:
                    lats = [c[1] for c in coords]
                    lons = [c[0] for c in coords]
                    return sum(lats)/len(lats), sum(lons)/len(lons)
    return None, None

def _find_nearest_node(graph: nx.DiGraph, lat: float, lon: float) -> str:
    nearest = None
    min_dist = float('inf')
    for n, data in graph.nodes(data=True):
        n_lat, n_lon = data.get('lat'), data.get('lng')
        if n_lat is not None and n_lon is not None:
            d = calculate_haversine(lat, lon, n_lat, n_lon)
            if d < min_dist:
                min_dist = d
                nearest = n
    return nearest

def plan_route(graph: nx.DiGraph, group: PilgrimGroup, zones_data: Dict[str, Any]) -> RouteResult:
    # 1. Resolve current edge and find forward endpoint (v)
    current_edge_id = group.current_edge_id
    
    # Resolve the exact directed edge (u, v) matching this ID
    matched_edges = []
    for u, v, data in graph.edges(data=True):
        if data.get('edge_id') == current_edge_id:
            matched_edges.append((u, v))
            
    if len(matched_edges) != 1:
        return RouteResult(
            group_id=group.group_id,
            status="unreachable",
            reason="invalid_current_edge"
        )
        
    start_node = matched_edges[0][1] # The forward endpoint 'v'
    
    if not graph.has_node(start_node):
        return RouteResult(
            group_id=group.group_id,
            status="unreachable",
            reason="invalid_current_edge"
        )
    
    # 2. Resolve destination zone
    dest_lat, dest_lon = _get_zone_center(zones_data, group.destination_zone_id)
    if dest_lat is None or dest_lon is None:
        return RouteResult(
            group_id=group.group_id,
            status="unreachable",
            reason="invalid_destination_zone"
        )
        
    # 3. Find target graph node
    target_node = _find_nearest_node(graph, dest_lat, dest_lon)
    if target_node is None:
        return RouteResult(
            group_id=group.group_id,
            status="unreachable",
            reason="graph_empty"
        )
        
    if start_node == target_node:
        return RouteResult(
            group_id=group.group_id,
            status="routed",
            start_node=start_node,
            target_node=target_node,
            node_ids=[start_node],
            edge_ids=[],
            total_distance_m=0.0
        )
        
    # 4. Shortest path routing respecting directionality
    try:
        path_nodes = nx.shortest_path(graph, source=start_node, target=target_node, weight="length_m")
    except nx.NetworkXNoPath:
        return RouteResult(
            group_id=group.group_id,
            status="unreachable",
            reason="no_directed_path"
        )
        
    # 5. Extract edge IDs and total distance
    edge_ids = []
    total_dist = 0.0
    
    for i in range(len(path_nodes) - 1):
        u = path_nodes[i]
        v = path_nodes[i+1]
        edge_data = graph.get_edge_data(u, v)
        if not edge_data or 'edge_id' not in edge_data:
            return RouteResult(
                group_id=group.group_id,
                status="unreachable",
                reason="corrupt_graph_edge"
            )
        edge_ids.append(edge_data['edge_id'])
        total_dist += edge_data.get('length_m', 0.0)
        
    return RouteResult(
        group_id=group.group_id,
        status="routed",
        start_node=start_node,
        target_node=target_node,
        node_ids=path_nodes,
        edge_ids=edge_ids,
        total_distance_m=total_dist
    )
