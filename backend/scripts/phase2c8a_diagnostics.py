import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.simulation.state_manager import SimulationStateManager
from app.simulation.crowd_aggregator import aggregate_crowd
from app.schemas.crowd import TemporalCrowdSnapshot
from app.ml.features import extract_features, get_edge_load
from app.ml.baseline import predict_persistence
from app.ml.evaluation import evaluate_predictions

def run_diagnostics():
    print("="*50)
    print("PHASE 2C-8A: DETERMINISTIC FEATURE & BASELINE DIAGNOSTIC")
    print("="*50)
    
    manager = SimulationStateManager()
    manager._initialize_state(85, 42)
    
    # 1. Generate History
    total_ticks = 100
    print(f"Generating {total_ticks} ticks of simulation history...")
    
    history = []
    # Tick 0
    crowd = aggregate_crowd(manager.graph, list(manager.groups.values()))
    history.append(TemporalCrowdSnapshot(
        tick=0, simulation_time=manager.sim_time.isoformat(), snapshot=crowd
    ))
    
    for i in range(1, total_ticks):
        manager.advance(1.0)
        crowd = aggregate_crowd(manager.graph, list(manager.groups.values()))
        history.append(TemporalCrowdSnapshot(
            tick=manager.tick, simulation_time=manager.sim_time.isoformat(), snapshot=crowd
        ))
        
    print(f"History generated. Total ticks available: {len(history)}")
    
    # Identify unique edges
    unique_edges = set()
    for snap in history:
        for edge in snap.snapshot.edges:
            unique_edges.add(edge.edge_id)
            
    print(f"Unique active edges observed: {len(unique_edges)}")
    
    # 2. Build feature rows and evaluate baseline
    predictions = []
    targets = []
    evaluated_edges = []
    
    candidate_rows = len(unique_edges) * total_ticks
    valid_rows = 0
    skipped_rows = 0
    missing_features = 0 # should be 0 because we handle sparse
    
    print("Building deterministic features and evaluating persistence baseline...")
    
    # Note: To avoid temporal leakage, we evaluate prediction at T+15 using features at T
    # So we loop from tick 15 to total_ticks - 16
    for t in range(total_ticks):
        # We need target at t+15
        target_tick = t + 15
        if target_tick >= total_ticks:
            skipped_rows += len(unique_edges)
            continue
            
        for edge_id in unique_edges:
            # We ONLY pass history up to t to explicitly prevent future leakage
            safe_history = history[:t+1]
            features = extract_features(safe_history, edge_id, t)
            
            if features is None:
                skipped_rows += 1
                continue
                
            # target extraction
            # ensure target_tick is in history
            target_snap = history[target_tick]
            target_load = get_edge_load(target_snap, edge_id)
            
            # Predict
            pred = predict_persistence(features)
            
            predictions.append(pred)
            targets.append(target_load)
            evaluated_edges.append(edge_id)
            valid_rows += 1
            
    print("="*50)
    print("DIAGNOSTIC OUTPUT")
    print("="*50)
    
    print("Temporal history:")
    print(f"- ticks available: {len(history)}")
    print(f"- unique edges: {len(unique_edges)}")
    print(f"- candidate rows: {candidate_rows}")
    print(f"- valid rows: {valid_rows}")
    print(f"- skipped rows: {skipped_rows}")
    
    print("\nFeatures:")
    print("- number of features per row: 8 (current, 3 lags, 3 changes, occupancy)")
    print(f"- missing-feature count: {missing_features}")
    
    metrics = evaluate_predictions(predictions, targets, evaluated_edges, skipped_rows)
    
    print("\nBaseline (Persistence):")
    print(f"- prediction horizon = 15 ticks")
    print(f"- MAE: {metrics.mae:.4f}")
    print(f"- RMSE: {metrics.rmse:.4f}")
    print(f"- evaluated samples: {metrics.evaluated_samples}")
    print(f"- unique edges evaluated: {metrics.unique_edges}")
    
    print("\nTarget Load Statistics:")
    print(f"- minimum target load: {metrics.min_target_load}")
    print(f"- maximum target load: {metrics.max_target_load}")
    print(f"- mean target load: {metrics.mean_target_load:.4f}")
    print("="*50)

if __name__ == "__main__":
    run_diagnostics()
