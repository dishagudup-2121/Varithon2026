import networkx as nx
import math
from typing import Optional, List, Tuple
from ..graph.graph_model import calculate_haversine
from ..schemas.simulation import GeoPosition

def resolve_position(graph: nx.DiGraph, edge_id: str, progress: float) -> Optional[GeoPosition]:
    """
    Resolves the geographic position of a given progress along a directed edge.
    Returns GeoPosition(lat, lng) or None if resolution fails.
    """
    if not (0.0 <= progress <= 1.0):
        return None
        
    # Find the edge
    u, v, data = None, None, None
    for src, dst, edata in graph.edges(data=True):
        if edata.get("edge_id") == edge_id:
            u, v, data = src, dst, edata
            break
            
    if u is None or data is None:
        return None
        
    geom = data.get("geometry")
    if not geom or len(geom) < 2:
        return None
        
    # Nodes coordinates for alignment checking
    u_node = graph.nodes.get(u)
    v_node = graph.nodes.get(v)
    
    if not u_node or not v_node:
        return None
        
    u_lat, u_lng = u_node.get("lat"), u_node.get("lng")
    v_lat, v_lng = v_node.get("lat"), v_node.get("lng")
    
    if None in (u_lat, u_lng, v_lat, v_lng):
        return None
        
    # Geometry points are stored as [lon, lat]
    p0_lon, p0_lat = geom[0]
    pn_lon, pn_lat = geom[-1]
    
    # Check orientation with 50m tolerance for minor graph simplifications
    TOLERANCE_M = 50.0
    
    dist_p0_to_u = calculate_haversine(p0_lat, p0_lon, u_lat, u_lng)
    dist_pn_to_v = calculate_haversine(pn_lat, pn_lon, v_lat, v_lng)
    
    dist_p0_to_v = calculate_haversine(p0_lat, p0_lon, v_lat, v_lng)
    dist_pn_to_u = calculate_haversine(pn_lat, pn_lon, u_lat, u_lng)
    
    is_forward = dist_p0_to_u <= TOLERANCE_M and dist_pn_to_v <= TOLERANCE_M
    is_reversed = dist_pn_to_u <= TOLERANCE_M and dist_p0_to_v <= TOLERANCE_M
    
    if not is_forward and not is_reversed:
        # Cannot be reliably reconciled
        return None
        
    active_geom = geom if is_forward else list(reversed(geom))
    
    # Calculate cumulative distances
    cumulative_distances: List[float] = [0.0]
    for i in range(1, len(active_geom)):
        prev_lon, prev_lat = active_geom[i-1]
        curr_lon, curr_lat = active_geom[i]
        
        # Guard against malformed lat/lng
        if not (-90.0 <= prev_lat <= 90.0 and -180.0 <= prev_lon <= 180.0 and 
                -90.0 <= curr_lat <= 90.0 and -180.0 <= curr_lon <= 180.0):
            return None
            
        segment_dist = calculate_haversine(prev_lat, prev_lon, curr_lat, curr_lon)
        cumulative_distances.append(cumulative_distances[-1] + segment_dist)
        
    total_length = cumulative_distances[-1]
    
    if total_length == 0.0:
        # Avoid division by zero on zero-length geometries, just return first point
        pt = active_geom[0]
        return GeoPosition(lat=pt[1], lng=pt[0])
        
    target_dist = progress * total_length
    
    # Find the segment containing the target distance
    for i in range(1, len(cumulative_distances)):
        if cumulative_distances[i] >= target_dist:
            # Interpolate within this segment
            prev_dist = cumulative_distances[i-1]
            segment_length = cumulative_distances[i] - prev_dist
            
            if segment_length == 0.0:
                pt = active_geom[i]
                return GeoPosition(lat=pt[1], lng=pt[0])
                
            fraction = (target_dist - prev_dist) / segment_length
            
            lon1, lat1 = active_geom[i-1]
            lon2, lat2 = active_geom[i]
            
            interp_lat = lat1 + (lat2 - lat1) * fraction
            interp_lon = lon1 + (lon2 - lon1) * fraction
            
            return GeoPosition(lat=interp_lat, lng=interp_lon)
            
    # Fallback to exact end point if float math slightly exceeds
    end_pt = active_geom[-1]
    return GeoPosition(lat=end_pt[1], lng=end_pt[0])
