import pytest
from datetime import datetime, timezone

from app.ml.features import EdgeFeatures, extract_features
from app.schemas.crowd import TemporalCrowdSnapshot, CrowdEdgeLoad, CrowdStateSnapshot, CrowdSummary

def build_fake_history(num_ticks: int, edge_id: str, load_sequence: list) -> list:
    history = []
    base_time = datetime(2026, 8, 12, 12, 0, tzinfo=timezone.utc)
    for i in range(num_ticks):
        edges = []
        if load_sequence[i] > 0:
            edges.append(CrowdEdgeLoad(
                edge_id=edge_id, 
                pilgrim_count=load_sequence[i],
                group_count=1,
                moving_group_count=1,
                stopped_group_count=0,
                congested_group_count=0
            ))
            
        snap = CrowdStateSnapshot(
            summary=CrowdSummary(
                total_pilgrims=load_sequence[i],
                total_groups=1,
                active_edge_count=1,
                moving_group_count=1,
                stopped_group_count=0,
                congested_group_count=0,
                unresolved_group_count=0
            ),
            edges=edges
        )
        ts = TemporalCrowdSnapshot(
            tick=i,
            simulation_time=base_time.isoformat(),
            snapshot=snap
        )
        history.append(ts)
    return history

def test_temporal_leakage_feature_extraction():
    """
    Ensures that for current_tick T, features NEVER access > T.
    """
    # Create history of 20 ticks. Target edge load goes up by 1 each tick.
    # So load at tick 0 is 0, tick 15 is 15, tick 19 is 19.
    edge_id = "E_R_OSM_123_1_2"
    loads = [i for i in range(20)]
    history = build_fake_history(20, edge_id, loads)
    
    current_tick = 15
    features = extract_features(history, edge_id, current_tick)
    
    assert features is not None
    assert features.current_load == 15
    assert features.load_t_minus_1 == 14
    assert features.load_t_minus_5 == 10
    assert features.load_t_minus_15 == 0
    
    # We should have strictly no access to tick 16+ data in the returned features
    # (By definition of the EdgeFeatures schema, there are no forward features)
    feature_dict = features.model_dump()
    for key in feature_dict.keys():
        assert "plus" not in key
        assert "future" not in key

def test_insufficient_history_returns_none():
    edge_id = "E_R_OSM_123_1_2"
    loads = [i for i in range(10)]
    history = build_fake_history(10, edge_id, loads)
    
    # Tick 9 does not have T-15 history available
    features = extract_features(history, edge_id, 9)
    assert features is None
    
def test_inference_isolation():
    """
    Test that the prediction engine safely returns None when missing models,
    rather than crashing.
    """
    from app.ml.inference import PredictionEngine
    from app.simulation.temporal_manager import TemporalStateManager
    
    # Force a fresh engine which won't find a model if we mess up the paths or haven't trained
    engine = PredictionEngine()
    engine.model_loaded = False
    
    temp_manager = TemporalStateManager()
    edge_id = "E_R_OSM_123_1_2"
    
    # This MUST return None, and MUST NOT throw an exception
    result = engine.predict_edge_load(temp_manager, edge_id)
    assert result is None
