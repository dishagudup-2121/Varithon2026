import pytest
import networkx as nx
from app.simulation.position_resolver import resolve_position

def test_resolve_position_progress_0_and_1():
    G = nx.DiGraph()
    G.add_node("u", lat=10.0, lng=20.0)
    G.add_node("v", lat=10.1, lng=20.1)
    
    # geom is [lon, lat]
    geom = [[20.0, 10.0], [20.05, 10.05], [20.1, 10.1]]
    G.add_edge("u", "v", edge_id="E1", geometry=geom)
    
    # Progress 0 -> first coord
    pos0 = resolve_position(G, "E1", 0.0)
    assert pos0 is not None
    assert pos0.lat == 10.0
    assert pos0.lng == 20.0
    
    # Progress 1 -> last coord
    pos1 = resolve_position(G, "E1", 1.0)
    assert pos1 is not None
    assert pos1.lat == 10.1
    assert pos1.lng == 20.1

def test_resolve_position_midpoint():
    G = nx.DiGraph()
    G.add_node("u", lat=10.0, lng=20.0)
    G.add_node("v", lat=10.0, lng=20.2)
    
    geom = [[20.0, 10.0], [20.2, 10.0]]
    G.add_edge("u", "v", edge_id="E2", geometry=geom)
    
    pos = resolve_position(G, "E2", 0.5)
    assert pos is not None
    assert pos.lat == 10.0
    assert pos.lng == 20.1 # exactly half

def test_resolve_position_reversed_geometry():
    G = nx.DiGraph()
    G.add_node("u", lat=10.0, lng=20.0)
    G.add_node("v", lat=10.1, lng=20.1)
    
    # geometry is reversed relative to u->v
    geom = [[20.1, 10.1], [20.0, 10.0]]
    G.add_edge("u", "v", edge_id="E3", geometry=geom)
    
    # Progress 0 should match node u (10.0, 20.0) even though geom[0] is (10.1, 20.1)
    pos0 = resolve_position(G, "E3", 0.0)
    assert pos0 is not None
    assert pos0.lat == 10.0
    assert pos0.lng == 20.0
    
    pos1 = resolve_position(G, "E3", 1.0)
    assert pos1 is not None
    assert pos1.lat == 10.1
    assert pos1.lng == 20.1

def test_invalid_cases():
    G = nx.DiGraph()
    G.add_node("u", lat=10.0, lng=20.0)
    G.add_node("v", lat=10.1, lng=20.1)
    
    # Too few coords
    G.add_edge("u", "v", edge_id="E_SHORT", geometry=[[20.0, 10.0]])
    assert resolve_position(G, "E_SHORT", 0.0) is None
    
    # Out of bounds progress
    geom = [[20.0, 10.0], [20.1, 10.1]]
    G.add_edge("u", "v", edge_id="E_GOOD", geometry=geom)
    assert resolve_position(G, "E_GOOD", -0.1) is None
    assert resolve_position(G, "E_GOOD", 1.1) is None
    
    # Bad lat/lng
    G.add_edge("u", "v", edge_id="E_BAD", geometry=[[20.0, 10.0], [200.0, 100.0]]) # 200 lon, 100 lat is invalid
    assert resolve_position(G, "E_BAD", 0.5) is None
    
    # Unreconcilable geometry
    G.add_node("x", lat=40.0, lng=50.0)
    G.add_node("y", lat=41.0, lng=51.0)
    G.add_edge("x", "y", edge_id="E_UNREC", geometry=[[20.0, 10.0], [20.1, 10.1]]) # Doesn't match nodes
    assert resolve_position(G, "E_UNREC", 0.5) is None
