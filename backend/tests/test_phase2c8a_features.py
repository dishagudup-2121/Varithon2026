import pytest
from app.schemas.crowd import TemporalCrowdSnapshot, CrowdStateSnapshot, CrowdSummary, CrowdEdgeLoad
from app.ml.features import extract_features, get_edge_load
from app.ml.baseline import predict_persistence
from app.ml.evaluation import evaluate_predictions

def _make_snap(tick: int, edge_id: str, load: int):
    return TemporalCrowdSnapshot(
        tick=tick,
        simulation_time="2026-08-15T12:00:00Z",
        snapshot=CrowdStateSnapshot(
            summary=CrowdSummary(
                total_pilgrims=0, total_groups=0, active_edge_count=0,
                moving_group_count=0, stopped_group_count=0, congested_group_count=0,
                unresolved_group_count=0
            ),
            edges=[
                CrowdEdgeLoad(
                    edge_id=edge_id, pilgrim_count=load, group_count=1,
                    moving_group_count=1, stopped_group_count=0, congested_group_count=0
                )
            ] if load > 0 else []
        )
    )

def test_feature_extraction_and_baseline():
    history = []
    # Build history from tick 0 to 20
    # edge1 will have varying loads. edge2 will be sparse.
    for i in range(21):
        if i < 10:
            load = 100
        elif i < 15:
            load = 200
        else:
            load = 50
        history.append(_make_snap(i, "edge1", load))
        
    # Add a sparse edge (edge2) that only appears at tick 18
    for i in range(21):
        if i == 18:
            history[i].snapshot.edges.append(CrowdEdgeLoad(
                edge_id="edge2", pilgrim_count=300, group_count=1,
                moving_group_count=1, stopped_group_count=0, congested_group_count=0
            ))

    # Test 1: current load, lags, changes
    f1 = extract_features(history, "edge1", 15)
    assert f1 is not None
    assert f1.current_load == 50
    assert f1.load_t_minus_1 == 200 # at tick 14
    assert f1.load_t_minus_5 == 200 # at tick 10
    assert f1.load_t_minus_15 == 100 # at tick 0
    assert f1.absolute_load_change_1 == -150
    assert f1.absolute_load_change_5 == -150
    assert f1.absolute_load_change_15 == -50
    
    # Test occupancy
    assert f1.consecutive_occupied_ticks == 16 # Ticks 0 to 15 inclusive is 16 ticks
    
    # Test sparse edge -> zero
    f2 = extract_features(history, "edge2", 15)
    assert f2 is not None
    assert f2.current_load == 0
    assert f2.load_t_minus_1 == 0
    assert f2.consecutive_occupied_ticks == 0
    
    # Test edge becoming empty and newly appearing
    f3 = extract_features(history, "edge2", 18)
    assert f3.current_load == 300
    assert f3.load_t_minus_1 == 0
    assert f3.consecutive_occupied_ticks == 1 # only occupied at tick 18
    
    f4 = extract_features(history, "edge2", 19)
    assert f4.current_load == 0
    assert f4.load_t_minus_1 == 300
    assert f4.consecutive_occupied_ticks == 0
    
    # Test insufficient history
    f_invalid = extract_features(history, "edge1", 10)
    assert f_invalid is None # missing T-15 because tick is 10, T-15 = -5
    
    # Test persistence prediction
    assert predict_persistence(f1) == 50
    assert predict_persistence(f2) == 0
    
    # Test future leakage prevention
    f_leakage = extract_features(history[:16], "edge1", 15)
    assert f_leakage is not None
    assert f_leakage.current_load == 50
    
    # Test Evaluation
    preds = [100, 200, 300]
    targets = [110, 200, 250]
    edges = ["e1", "e2", "e1"]
    
    metrics = evaluate_predictions(preds, targets, edges, 0)
    assert metrics.mae == (10 + 0 + 50) / 3
    assert metrics.rmse == ((10**2 + 0 + 50**2) / 3) ** 0.5
    assert metrics.evaluated_samples == 3
    assert metrics.unique_edges == 2
    
    # Test target extraction (get_edge_load)
    assert get_edge_load(history[15], "edge1") == 50
    assert get_edge_load(history[15], "edge3") == 0
    
    # Deterministic repeated evaluation
    m1 = evaluate_predictions(preds, targets, edges, 0)
    m2 = evaluate_predictions(preds, targets, edges, 0)
    assert m1.mae == m2.mae and m1.rmse == m2.rmse
