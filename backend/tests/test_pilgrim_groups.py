import pytest
import networkx as nx
from datetime import datetime, timezone
from pydantic import ValidationError
from app.simulation.pilgrim_model import PilgrimGroup
from app.simulation.generator import generate_pilgrim_groups

@pytest.fixture
def sample_graph():
    G = nx.DiGraph()
    # Component 1 (Largest)
    G.add_node("N1")
    G.add_node("N2")
    G.add_node("N3")
    G.add_edge("N1", "N2", edge_id="E1", length_m=10.0, geometry=[[0,0], [1,1]])
    G.add_edge("N2", "N3", edge_id="E2", length_m=15.0, geometry=[[1,1], [2,2]])
    
    # Component 2 (Smaller)
    G.add_node("N4")
    G.add_node("N5")
    G.add_edge("N4", "N5", edge_id="E3", length_m=5.0, geometry=[[3,3], [4,4]])
    return G

@pytest.fixture
def sample_zones():
    return {
        "features": [
            {"properties": {"zone_id": "Z1"}},
            {"properties": {"zone_id": "Z2"}}
        ]
    }

def test_deterministic_generation(sample_graph, sample_zones):
    t = datetime(2026, 8, 12, 12, 0, tzinfo=timezone.utc)
    groups1 = generate_pilgrim_groups(sample_graph, sample_zones, t, count=10, seed=42)
    groups2 = generate_pilgrim_groups(sample_graph, sample_zones, t, count=10, seed=42)
    
    for g1, g2 in zip(groups1, groups2):
        assert g1.group_id == g2.group_id
        assert g1.count == g2.count
        assert g1.current_edge_id == g2.current_edge_id
        assert g1.progress == g2.progress
        assert g1.speed_mps == g2.speed_mps
        assert g1.destination_zone_id == g2.destination_zone_id

def test_different_seeds(sample_graph, sample_zones):
    t = datetime(2026, 8, 12, 12, 0, tzinfo=timezone.utc)
    groups1 = generate_pilgrim_groups(sample_graph, sample_zones, t, count=5, seed=42)
    groups2 = generate_pilgrim_groups(sample_graph, sample_zones, t, count=5, seed=99)
    
    # At least one generated attribute should differ
    assert any(g1.count != g2.count for g1, g2 in zip(groups1, groups2))

def test_unique_group_ids(sample_graph, sample_zones):
    t = datetime(2026, 8, 12, 12, 0, tzinfo=timezone.utc)
    groups = generate_pilgrim_groups(sample_graph, sample_zones, t, count=10, seed=42)
    ids = [g.group_id for g in groups]
    assert len(ids) == len(set(ids))

def test_valid_assignments(sample_graph, sample_zones):
    t = datetime(2026, 8, 12, 12, 0, tzinfo=timezone.utc)
    groups = generate_pilgrim_groups(sample_graph, sample_zones, t, count=10, seed=42)
    
    for g in groups:
        assert g.count > 0
        # Should only be E1 or E2 from largest component
        assert g.current_edge_id in ["E1", "E2"]
        assert 0.0 <= g.progress <= 1.0
        assert g.speed_mps > 0.0
        assert g.destination_zone_id in ["Z1", "Z2"]
        assert g.created_at == t
        assert g.updated_at == t

def test_multiple_groups_share_edge(sample_graph, sample_zones):
    t = datetime(2026, 8, 12, 12, 0, tzinfo=timezone.utc)
    # 100 groups, only 2 valid edges -> must have sharing
    groups = generate_pilgrim_groups(sample_graph, sample_zones, t, count=100, seed=42)
    
    edge_counts = {"E1": 0, "E2": 0}
    for g in groups:
        edge_counts[g.current_edge_id] += 1
        
    assert edge_counts["E1"] > 1
    assert edge_counts["E2"] > 1

def test_invalid_models():
    t = datetime.now()
    
    with pytest.raises(ValidationError):
        # invalid progress
        PilgrimGroup(group_id="G1", count=100, current_edge_id="E1", progress=1.5, speed_mps=1.0, status="moving", destination_zone_id="Z1", created_at=t, updated_at=t)
        
    with pytest.raises(ValidationError):
        # invalid count
        PilgrimGroup(group_id="G1", count=-5, current_edge_id="E1", progress=0.5, speed_mps=1.0, status="moving", destination_zone_id="Z1", created_at=t, updated_at=t)
        
    with pytest.raises(ValidationError):
        # invalid speed
        PilgrimGroup(group_id="G1", count=10, current_edge_id="E1", progress=0.5, speed_mps=-1.0, status="moving", destination_zone_id="Z1", created_at=t, updated_at=t)

def test_missing_zones(sample_graph):
    t = datetime.now()
    with pytest.raises(ValueError, match="No valid zones found"):
        generate_pilgrim_groups(sample_graph, {}, t)
