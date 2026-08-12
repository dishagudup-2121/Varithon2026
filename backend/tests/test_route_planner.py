import pytest
import networkx as nx
from datetime import datetime, timezone
from app.simulation.pilgrim_model import PilgrimGroup
from app.simulation.route_planner import plan_route, RouteResult

@pytest.fixture
def mock_group():
    return PilgrimGroup(
        group_id="G001",
        count=100,
        current_edge_id="E_CURRENT",
        progress=0.5,
        speed_mps=1.0,
        status="moving",
        destination_zone_id="Z1",
        created_at=datetime(2026, 8, 12, 12, 0, tzinfo=timezone.utc),
        updated_at=datetime(2026, 8, 12, 12, 0, tzinfo=timezone.utc)
    )

@pytest.fixture
def mock_zones():
    return {
        "features": [
            {
                "properties": {
                    "zone_id": "Z1",
                    "center": [18.1, 73.1]
                }
            },
            {
                "properties": {
                    "zone_id": "Z_DISCONNECTED",
                    "center": [18.9, 73.9]
                }
            }
        ]
    }

def test_mandatory_weighted_routing(mock_group, mock_zones):
    """
    Route A: 100m + 100m + 100m = 300m
    Route B: 150m + 50m = 200m
    The route planner must select Route B.
    """
    G = nx.DiGraph()
    # Base nodes
    G.add_node("N0", lat=18.0, lng=73.0)
    G.add_node("N1", lat=18.0, lng=73.0) # Start node (v of current edge)
    G.add_node("N_DEST", lat=18.1, lng=73.1) # Target node

    # Current edge (N0 -> N1)
    G.add_edge("N0", "N1", edge_id="E_CURRENT", length_m=10.0)

    # Route A nodes (3 hops)
    G.add_node("N_A1", lat=18.0, lng=73.0)
    G.add_node("N_A2", lat=18.0, lng=73.0)
    
    # Route B node (2 hops)
    G.add_node("N_B1", lat=18.0, lng=73.0)
    
    # Route A edges (Total = 300)
    G.add_edge("N1", "N_A1", edge_id="E_A1", length_m=100.0)
    G.add_edge("N_A1", "N_A2", edge_id="E_A2", length_m=100.0)
    G.add_edge("N_A2", "N_DEST", edge_id="E_A3", length_m=100.0)
    
    # Route B edges (Total = 200)
    G.add_edge("N1", "N_B1", edge_id="E_B1", length_m=150.0)
    G.add_edge("N_B1", "N_DEST", edge_id="E_B2", length_m=50.0)
    
    res = plan_route(G, mock_group, mock_zones)
    
    assert res.status == "routed"
    # Even though Route A has more hops (3), Route B is shorter in weight (200m < 300m)
    # Wait, shortest path minimizes weight. Both are valid. Route B (200m) should win.
    assert res.total_distance_m == 200.0
    assert res.edge_ids == ["E_B1", "E_B2"]
    assert res.node_ids == ["N1", "N_B1", "N_DEST"]

def test_unreachable_directed_route(mock_group, mock_zones):
    # One-way restriction prevents reaching destination
    G = nx.DiGraph()
    G.add_node("N0", lat=18.0, lng=73.0)
    G.add_node("N1", lat=18.0, lng=73.0)
    G.add_node("N2", lat=18.1, lng=73.1)
    
    G.add_edge("N0", "N1", edge_id="E_CURRENT", length_m=10.0)
    # Edge goes FROM N2 to N1, so N2 is unreachable from N1
    G.add_edge("N2", "N1", edge_id="E_WRONG_WAY", length_m=50.0)
    
    res = plan_route(G, mock_group, mock_zones)
    assert res.status == "unreachable"
    assert res.reason == "no_directed_path"

def test_disconnected_graph(mock_group, mock_zones):
    G = nx.DiGraph()
    G.add_node("N0", lat=18.0, lng=73.0)
    G.add_node("N1", lat=18.0, lng=73.0)
    G.add_edge("N0", "N1", edge_id="E_CURRENT", length_m=10.0)
    
    # Destination node is completely disconnected
    G.add_node("N2", lat=18.9, lng=73.9) 
    
    mock_group.destination_zone_id = "Z_DISCONNECTED"
    
    res = plan_route(G, mock_group, mock_zones)
    assert res.status == "unreachable"
    assert res.reason == "no_directed_path"

def test_endpoint_selection(mock_group, mock_zones):
    G = nx.DiGraph()
    G.add_node("N0", lat=18.0, lng=73.0)
    G.add_node("N1", lat=18.0, lng=73.0)
    G.add_node("N2", lat=18.1, lng=73.1)
    
    G.add_edge("N0", "N1", edge_id="E_CURRENT", length_m=10.0)
    # Path from N0 is shorter, but we MUST start from N1 because we are on N0->N1
    G.add_edge("N0", "N2", edge_id="E_BACKWARD", length_m=5.0)
    G.add_edge("N1", "N2", edge_id="E_FORWARD", length_m=100.0)
    
    res = plan_route(G, mock_group, mock_zones)
    assert res.status == "routed"
    assert res.start_node == "N1"
    assert res.edge_ids == ["E_FORWARD"]
    assert res.total_distance_m == 100.0

def test_invalid_current_edge(mock_group, mock_zones):
    G = nx.DiGraph()
    # Graph is empty
    res = plan_route(G, mock_group, mock_zones)
    assert res.status == "unreachable"
    assert res.reason == "invalid_current_edge"

def test_invalid_destination_zone(mock_group, mock_zones):
    G = nx.DiGraph()
    G.add_node("N0", lat=18.0, lng=73.0)
    G.add_node("N1", lat=18.0, lng=73.0)
    G.add_edge("N0", "N1", edge_id="E_CURRENT", length_m=10.0)
    
    mock_group.destination_zone_id = "Z_NONEXISTENT"
    res = plan_route(G, mock_group, mock_zones)
    assert res.status == "unreachable"
    assert res.reason == "invalid_destination_zone"
