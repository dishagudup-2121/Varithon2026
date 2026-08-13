import pytest
import networkx as nx
from datetime import datetime
from app.simulation.pilgrim_model import PilgrimGroup
from app.simulation.crowd_aggregator import aggregate_crowd

def build_test_graph():
    G = nx.DiGraph()
    G.add_edge("N1", "N2", edge_id="E1")
    G.add_edge("N2", "N3", edge_id="E2")
    G.add_edge("N3", "N4", edge_id="E3")
    return G

def create_group(group_id, edge_id, count, status="moving"):
    return PilgrimGroup(
        group_id=group_id,
        count=count,
        current_edge_id=edge_id,
        progress=0.5,
        speed_mps=1.0,
        status=status,
        destination_zone_id="Z1",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

def test_1_empty_simulation():
    G = build_test_graph()
    snap = aggregate_crowd(G, [])
    assert snap.summary.total_groups == 0
    assert snap.summary.total_pilgrims == 0
    assert snap.summary.active_edge_count == 0
    assert snap.summary.unresolved_group_count == 0
    assert len(snap.edges) == 0

def test_2_one_group_one_edge():
    G = build_test_graph()
    g1 = create_group("G1", "E1", 100)
    snap = aggregate_crowd(G, [g1])
    assert snap.summary.total_groups == 1
    assert snap.summary.total_pilgrims == 100
    assert snap.summary.active_edge_count == 1
    assert len(snap.edges) == 1
    assert snap.edges[0].edge_id == "E1"
    assert snap.edges[0].pilgrim_count == 100

def test_3_multiple_groups_same_edge():
    G = build_test_graph()
    g1 = create_group("G1", "E1", 100)
    g2 = create_group("G2", "E1", 200)
    snap = aggregate_crowd(G, [g1, g2])
    assert snap.summary.active_edge_count == 1
    assert snap.edges[0].pilgrim_count == 300
    assert snap.edges[0].group_count == 2

def test_4_groups_on_different_edges():
    G = build_test_graph()
    g1 = create_group("G1", "E1", 100)
    g2 = create_group("G2", "E2", 200)
    snap = aggregate_crowd(G, [g1, g2])
    assert snap.summary.active_edge_count == 2
    assert len(snap.edges) == 2

def test_5_correct_pilgrim_count():
    G = build_test_graph()
    snap = aggregate_crowd(G, [create_group("G1", "E1", 50), create_group("G2", "E1", 75)])
    assert snap.edges[0].pilgrim_count == 125
    assert snap.summary.total_pilgrims == 125

def test_6_correct_group_count():
    G = build_test_graph()
    snap = aggregate_crowd(G, [create_group("G1", "E1", 10), create_group("G2", "E1", 10)])
    assert snap.edges[0].group_count == 2
    assert snap.summary.total_groups == 2

def test_7_moving_group_classification():
    G = build_test_graph()
    snap = aggregate_crowd(G, [create_group("G1", "E1", 10, "moving")])
    assert snap.edges[0].moving_group_count == 1
    assert snap.summary.moving_group_count == 1

def test_8_stopped_group_classification():
    G = build_test_graph()
    snap = aggregate_crowd(G, [create_group("G1", "E1", 10, "stopped")])
    assert snap.edges[0].stopped_group_count == 1
    assert snap.summary.stopped_group_count == 1

def test_9_congested_group_classification():
    G = build_test_graph()
    snap = aggregate_crowd(G, [create_group("G1", "E1", 10, "congested")])
    assert snap.edges[0].congested_group_count == 1
    assert snap.summary.congested_group_count == 1

def test_10_mixed_statuses_on_same_edge():
    G = build_test_graph()
    snap = aggregate_crowd(G, [
        create_group("G1", "E1", 10, "moving"),
        create_group("G2", "E1", 10, "stopped"),
        create_group("G3", "E1", 10, "congested")
    ])
    assert snap.edges[0].group_count == 3
    assert snap.edges[0].moving_group_count == 1
    assert snap.edges[0].stopped_group_count == 1
    assert snap.edges[0].congested_group_count == 1

def test_11_invalid_current_edge_id():
    G = build_test_graph()
    snap = aggregate_crowd(G, [create_group("G1", "E_INVALID", 10)])
    assert snap.summary.unresolved_group_count == 1
    assert snap.summary.active_edge_count == 0
    assert len(snap.edges) == 0

def test_12_multiple_invalid_groups():
    G = build_test_graph()
    snap = aggregate_crowd(G, [
        create_group("G1", "E_INVALID1", 10),
        create_group("G2", "E_INVALID2", 10)
    ])
    assert snap.summary.unresolved_group_count == 2
    assert len(snap.edges) == 0

def test_13_no_mutation_of_input_pilgrim_group():
    G = build_test_graph()
    g1 = create_group("G1", "E1", 100)
    snap = aggregate_crowd(G, [g1])
    assert g1.count == 100
    assert g1.current_edge_id == "E1"

def test_14_no_mutation_of_graph():
    G = build_test_graph()
    assert G.number_of_edges() == 3
    snap = aggregate_crowd(G, [create_group("G1", "E1", 100)])
    assert G.number_of_edges() == 3

def test_15_deterministic_output_ordering():
    G = build_test_graph()
    # Add out of order
    snap = aggregate_crowd(G, [
        create_group("G3", "E3", 10),
        create_group("G1", "E1", 10),
        create_group("G2", "E2", 10)
    ])
    assert snap.edges[0].edge_id == "E1"
    assert snap.edges[1].edge_id == "E2"
    assert snap.edges[2].edge_id == "E3"

def test_16_zero_load_edges_are_excluded():
    G = build_test_graph()
    snap = aggregate_crowd(G, [create_group("G1", "E1", 10)])
    # E2 and E3 exist in graph but not in result
    assert len(snap.edges) == 1

def test_17_large_group_count_values():
    G = build_test_graph()
    snap = aggregate_crowd(G, [create_group("G1", "E1", 9999999)])
    assert snap.edges[0].pilgrim_count == 9999999
    assert snap.summary.total_pilgrims == 9999999

def test_18_all_groups_unresolved():
    G = build_test_graph()
    snap = aggregate_crowd(G, [create_group("G1", "INVALID", 10)])
    assert snap.summary.unresolved_group_count == 1
    assert snap.summary.active_edge_count == 0

def test_19_combination_of_valid_and_unresolved_groups():
    G = build_test_graph()
    snap = aggregate_crowd(G, [
        create_group("G1", "E1", 100),
        create_group("G2", "INVALID", 200)
    ])
    assert snap.summary.total_pilgrims == 300
    assert snap.summary.total_groups == 2
    assert snap.summary.unresolved_group_count == 1
    assert snap.summary.active_edge_count == 1
    assert len(snap.edges) == 1
    assert snap.edges[0].pilgrim_count == 100

def test_20_total_summary_values_equal_aggregates():
    G = build_test_graph()
    snap = aggregate_crowd(G, [
        create_group("G1", "E1", 10, "moving"),
        create_group("G2", "E2", 20, "stopped")
    ])
    assert snap.summary.total_pilgrims == sum(e.pilgrim_count for e in snap.edges)
    assert snap.summary.moving_group_count == sum(e.moving_group_count for e in snap.edges)
    assert snap.summary.stopped_group_count == sum(e.stopped_group_count for e in snap.edges)
