import pytest
import networkx as nx
from app.graph.graph_builder import build_graph
from app.graph.graph_validator import validate_graph

def test_bidirectional_way():
    osm_data = {
        "elements": [
            {"type": "node", "id": 1, "lat": 18.0, "lon": 73.0},
            {"type": "node", "id": 2, "lat": 18.1, "lon": 73.1},
            {"type": "way", "id": 10, "nodes": [1, 2], "tags": {"highway": "primary"}}
        ]
    }
    G = build_graph(osm_data)
    assert G.number_of_nodes() == 2
    assert G.number_of_edges() == 2
    assert G.has_edge("N_1", "N_2")
    assert G.has_edge("N_2", "N_1")
    
    val = validate_graph(G)
    assert val["valid"] is True

def test_oneway_forward():
    osm_data = {
        "elements": [
            {"type": "node", "id": 1, "lat": 18.0, "lon": 73.0},
            {"type": "node", "id": 2, "lat": 18.1, "lon": 73.1},
            {"type": "way", "id": 10, "nodes": [1, 2], "tags": {"highway": "primary", "oneway": "yes"}}
        ]
    }
    G = build_graph(osm_data)
    assert G.number_of_edges() == 1
    assert G.has_edge("N_1", "N_2")
    assert not G.has_edge("N_2", "N_1")

def test_oneway_reverse():
    osm_data = {
        "elements": [
            {"type": "node", "id": 1, "lat": 18.0, "lon": 73.0},
            {"type": "node", "id": 2, "lat": 18.1, "lon": 73.1},
            {"type": "node", "id": 3, "lat": 18.2, "lon": 73.2},
            {"type": "way", "id": 10, "nodes": [1, 2, 3], "tags": {"highway": "primary", "oneway": "-1"}}
        ]
    }
    G = build_graph(osm_data)
    assert G.number_of_edges() == 2
    # N3 -> N2 and N2 -> N1
    assert G.has_edge("N_3", "N_2")
    assert G.has_edge("N_2", "N_1")
    assert not G.has_edge("N_1", "N_2")
    assert not G.has_edge("N_2", "N_3")

def test_missing_node_coordinates():
    osm_data = {
        "elements": [
            {"type": "node", "id": 1, "lat": 18.0, "lon": 73.0},
            {"type": "node", "id": 2}, # missing coordinates
            {"type": "way", "id": 10, "nodes": [1, 2], "tags": {"highway": "primary"}}
        ]
    }
    G = build_graph(osm_data)
    val = validate_graph(G)
    assert val["valid"] is False
    assert any("missing coordinates" in err for err in val["errors"])

def test_shared_osm_nodes():
    osm_data = {
        "elements": [
            {"type": "node", "id": 1, "lat": 18.0, "lon": 73.0},
            {"type": "node", "id": 2, "lat": 18.1, "lon": 73.1},
            {"type": "node", "id": 3, "lat": 18.2, "lon": 73.2},
            {"type": "way", "id": 10, "nodes": [1, 2], "tags": {"highway": "primary"}},
            {"type": "way", "id": 11, "nodes": [2, 3], "tags": {"highway": "secondary"}}
        ]
    }
    G = build_graph(osm_data)
    assert G.number_of_nodes() == 3
    # N2 is shared. Edges should be 1<->2 and 2<->3 (total 4 edges)
    assert G.number_of_edges() == 4
    assert G.has_edge("N_1", "N_2")
    assert G.has_edge("N_2", "N_3")

def test_edge_geometry_preserved():
    osm_data = {
        "elements": [
            {"type": "node", "id": 1, "lat": 18.0, "lon": 73.0},
            {"type": "node", "id": 2, "lat": 18.1, "lon": 73.1},
            {"type": "way", "id": 10, "nodes": [1, 2], "tags": {"highway": "primary", "oneway": "yes"}}
        ]
    }
    G = build_graph(osm_data)
    data = G.get_edge_data("N_1", "N_2")
    assert "geometry" in data
    assert data["geometry"] == [[73.0, 18.0], [73.1, 18.1]]

def test_duplicate_edge_id_validation():
    # Construct an invalid graph manually to test validator
    G = nx.DiGraph()
    G.add_node("N_1", lat=18.0, lng=73.0)
    G.add_node("N_2", lat=18.1, lng=73.1)
    G.add_edge("N_1", "N_2", edge_id="DUP_1", route_id="R_1", osm_way_id=1, highway="primary", name="test", length_m=10.0, oneway=True, geometry=[])
    G.add_edge("N_2", "N_1", edge_id="DUP_1", route_id="R_1", osm_way_id=1, highway="primary", name="test", length_m=10.0, oneway=True, geometry=[])
    
    val = validate_graph(G)
    assert val["valid"] is False
    assert any("Duplicate edge_id" in err for err in val["errors"])
