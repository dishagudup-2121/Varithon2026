import math
from typing import Dict, Any, List

def calculate_haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great-circle distance between two points on the Earth surface in meters."""
    R = 6371000.0  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2)**2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def get_node_id(osm_node_id: int) -> str:
    """Generate deterministic node ID from OSM node ID."""
    return f"N_{osm_node_id}"

def get_edge_id(osm_way_id: int, u_node_id: int, v_node_id: int) -> str:
    """Generate deterministic edge ID."""
    return f"E_R_OSM_{osm_way_id}_{u_node_id}_{v_node_id}"

def get_route_id(osm_way_id: int) -> str:
    """Generate deterministic route ID for an OSM way."""
    return f"R_OSM_{osm_way_id}"
