import pytest
import networkx as nx
import math
from datetime import datetime, timezone
from app.simulation.pilgrim_model import PilgrimGroup
from app.simulation.movement_engine import tick_movement

@pytest.fixture
def sample_graph():
    G = nx.DiGraph()
    # Simple straight line N0 -> N1 -> N2 -> N3 -> N4
    G.add_node("N0")
    G.add_node("N1")
    G.add_node("N2")
    G.add_node("N3")
    G.add_node("N4")
    
    G.add_edge("N0", "N1", edge_id="E0", length_m=100.0)
    G.add_edge("N1", "N2", edge_id="E1", length_m=50.0)
    G.add_edge("N2", "N3", edge_id="E2", length_m=25.0)
    G.add_edge("N3", "N4", edge_id="E3", length_m=10.0)
    
    # Disconnected edge
    G.add_node("N5")
    G.add_node("N6")
    G.add_edge("N5", "N6", edge_id="E_DISC", length_m=100.0)
    
    return G

@pytest.fixture
def mock_group():
    return PilgrimGroup(
        group_id="G001",
        count=100,
        current_edge_id="E0",
        progress=0.0,
        speed_mps=1.0,
        status="moving",
        destination_zone_id="Z1",
        route=["E1", "E2", "E3"],
        created_at=datetime(2026, 8, 12, 12, 0, tzinfo=timezone.utc),
        updated_at=datetime(2026, 8, 12, 12, 0, tzinfo=timezone.utc)
    )

def test_1_movement_within_single_edge_and_13_progress_bounds(sample_graph, mock_group):
    # E0 is 100m. Speed is 1.0 m/s. Move for 10s -> 10m
    res = tick_movement(sample_graph, mock_group, 10.0)
    assert res.success is True
    assert res.arrived is False
    assert res.distance_moved_m == 10.0
    assert mock_group.progress == 0.1 # 10 / 100
    assert mock_group.current_edge_id == "E0"
    
def test_2_progress_calculation(sample_graph, mock_group):
    mock_group.progress = 0.5 # 50m remaining on E0
    res = tick_movement(sample_graph, mock_group, 25.0) # Move 25m
    assert res.success is True
    assert mock_group.progress == 0.75

def test_3_exact_edge_boundary_crossing(sample_graph, mock_group):
    # Move exactly 100m. Should reach the end of E0 and transition to E1 at progress 0.0
    res = tick_movement(sample_graph, mock_group, 100.0)
    assert res.success is True
    assert mock_group.current_edge_id == "E1"
    assert mock_group.progress == 0.0
    assert res.edges_traversed == 1

def test_4_transition_to_next_edge(sample_graph, mock_group):
    # Move 110m. E0 is 100m, E1 is 50m.
    # Should consume E0, and 10m of E1.
    res = tick_movement(sample_graph, mock_group, 110.0)
    assert res.success is True
    assert mock_group.current_edge_id == "E1"
    assert mock_group.progress == 10.0 / 50.0 # 0.2
    assert res.edges_traversed == 1

def test_5_multi_edge_traversal(sample_graph, mock_group):
    # Move 170m. 
    # E0(100m) + E1(50m) + 20m of E2(25m)
    res = tick_movement(sample_graph, mock_group, 170.0)
    assert res.success is True
    assert mock_group.current_edge_id == "E2"
    assert mock_group.progress == 20.0 / 25.0 # 0.8
    assert res.edges_traversed == 2
    assert mock_group.route == ["E3"]

def test_6_arrival_when_route_empty(sample_graph, mock_group):
    # Total distance of route: E0(100) + E1(50) + E2(25) + E3(10) = 185m
    # Move 200m. Should arrive at 185m.
    res = tick_movement(sample_graph, mock_group, 200.0)
    assert res.success is True
    assert res.arrived is True
    assert mock_group.status == "stopped"
    assert mock_group.progress == 1.0
    assert mock_group.current_edge_id == "E3"
    assert res.distance_moved_m == 185.0 # Distance moved capped at arrival

def test_7_stationary_no_op(sample_graph, mock_group):
    mock_group.status = "stopped"
    res = tick_movement(sample_graph, mock_group, 10.0)
    assert res.success is True
    assert res.distance_moved_m == 0.0
    assert mock_group.progress == 0.0
    assert res.reason == "group_not_moving"

def test_8_invalid_current_edge(sample_graph, mock_group):
    mock_group.current_edge_id = "E_INVALID"
    res = tick_movement(sample_graph, mock_group, 10.0)
    assert res.success is False
    assert res.reason == "invalid_current_edge"
    assert mock_group.status == "stopped"

def test_9_invalid_route_edge(sample_graph, mock_group):
    mock_group.route = ["E_INVALID"]
    res = tick_movement(sample_graph, mock_group, 110.0) # Enough to force transition
    assert res.success is False
    assert res.reason == "invalid_route_edge"
    assert mock_group.status == "stopped"
    # Should have moved 100m on E0 before failing
    assert res.distance_moved_m == 100.0

def test_10_disconnected_next_edge(sample_graph, mock_group):
    mock_group.route = ["E_DISC"] # Not connected to N1 (end of E0)
    res = tick_movement(sample_graph, mock_group, 110.0)
    assert res.success is False
    assert res.reason == "route_edge_disconnected"
    assert mock_group.status == "stopped"

def test_11_invalid_edge_length(sample_graph, mock_group):
    # Set current edge length to 0
    sample_graph.edges["N0", "N1"]["length_m"] = 0.0
    res = tick_movement(sample_graph, mock_group, 10.0)
    assert res.success is False
    assert res.reason == "invalid_current_edge_length"

def test_12_invalid_delta_time(sample_graph, mock_group):
    res = tick_movement(sample_graph, mock_group, -5.0)
    assert res.success is False
    assert res.reason == "invalid_delta_time"
    
    res2 = tick_movement(sample_graph, mock_group, float('inf'))
    assert res2.success is False
    assert res2.reason == "invalid_delta_time"

def test_14_deterministic_repeated_execution(sample_graph, mock_group):
    # Two small ticks vs one big tick should yield identical states (within float tolerance)
    group1 = mock_group.model_copy(deep=True)
    group2 = mock_group.model_copy(deep=True)
    
    tick_movement(sample_graph, group1, 60.0)
    tick_movement(sample_graph, group1, 60.0)
    
    tick_movement(sample_graph, group2, 120.0)
    
    assert group1.current_edge_id == group2.current_edge_id
    assert math.isclose(group1.progress, group2.progress, rel_tol=1e-5)

def test_15_distance_moved_equals_speed_x_time(sample_graph, mock_group):
    # Normal case
    res1 = tick_movement(sample_graph, mock_group, 50.0)
    assert res1.distance_moved_m == 50.0
    
    # Arrival case (capping)
    res2 = tick_movement(sample_graph, mock_group, 200.0) # only 135m remaining
    assert res2.distance_moved_m == 135.0

def test_invalid_progress(sample_graph, mock_group):
    mock_group.progress = 1.5
    res = tick_movement(sample_graph, mock_group, 10.0)
    assert res.success is False
    assert res.reason == "invalid_progress"
