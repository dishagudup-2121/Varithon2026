import os
import sys
import csv
import logging
import pandas as pd
from typing import Dict, List
from collections import deque
from tqdm import tqdm

# Ensure backend root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from backend.app.simulation.state_manager import SimulationStateManager
from backend.app.simulation.crowd_aggregator import aggregate_crowd
from backend.app.schemas.crowd import TemporalCrowdSnapshot
from backend.app.ml.features import EdgeFeatures, get_edge_load

import backend.app.simulation.movement_engine as me
from backend.app.simulation.movement_engine import MovementResult
import math
from datetime import timedelta

# Monkey patch tick_movement to use a fast O(1) cache for edge resolution
# since the original iterates over the entire graph for every group, every tick.
edge_cache = {}

def fast_tick_movement(graph, group, delta_time_s):
    if not edge_cache:
        for u, v, data in graph.edges(data=True):
            eid = data.get('edge_id')
            if eid:
                edge_cache[eid] = (u, v, data.get('length_m'))
                
    if not math.isfinite(delta_time_s) or delta_time_s < 0:
        return MovementResult(group=group, distance_moved_m=0.0, edges_traversed=0, arrived=False, success=False, reason="invalid_delta_time")
    if group.status != "moving":
        return MovementResult(group=group, distance_moved_m=0.0, edges_traversed=0, arrived=(group.status == "stopped"), success=True, reason="group_not_moving")
    if not (0.0 <= group.progress <= 1.0):
        return MovementResult(group=group, distance_moved_m=0.0, edges_traversed=0, arrived=False, success=False, reason="invalid_progress")

    distance_to_move_m = group.speed_mps * delta_time_s
    distance_moved = 0.0
    edges_traversed = 0
    
    def resolve_edge(edge_id: str):
        return edge_cache.get(edge_id, (None, None, None))

    while distance_to_move_m > 0:
        u, v, length_m = resolve_edge(group.current_edge_id)
        if u is None or length_m is None or length_m <= 0:
            group.status = "stopped"
            reason = "invalid_current_edge" if u is None else "invalid_current_edge_length"
            return MovementResult(group=group, distance_moved_m=distance_moved, edges_traversed=edges_traversed, arrived=False, success=False, reason=reason)
            
        remaining_m = (1.0 - group.progress) * length_m
        if distance_to_move_m < remaining_m:
            group.progress += distance_to_move_m / length_m
            distance_moved += distance_to_move_m
            distance_to_move_m = 0.0
            break
        else:
            distance_to_move_m -= remaining_m
            distance_moved += remaining_m
            group.progress = 1.0
            if not group.route:
                group.status = "stopped"
                return MovementResult(group=group, distance_moved_m=distance_moved, edges_traversed=edges_traversed, arrived=True, success=True, reason=None)
            next_edge_id = group.route[0]
            next_u, next_v, next_length_m = resolve_edge(next_edge_id)
            if next_u is None:
                group.status = "stopped"
                return MovementResult(group=group, distance_moved_m=distance_moved, edges_traversed=edges_traversed, arrived=False, success=False, reason="invalid_route_edge")
            if next_u != v:
                group.status = "stopped"
                return MovementResult(group=group, distance_moved_m=distance_moved, edges_traversed=edges_traversed, arrived=False, success=False, reason="route_edge_disconnected")
            if next_length_m is None or next_length_m <= 0:
                group.status = "stopped"
                return MovementResult(group=group, distance_moved_m=distance_moved, edges_traversed=edges_traversed, arrived=False, success=False, reason="invalid_route_edge_length")
            group.route.pop(0)
            group.current_edge_id = next_edge_id
            group.progress = 0.0
            edges_traversed += 1

    group.updated_at += timedelta(seconds=delta_time_s)
    return MovementResult(group=group, distance_moved_m=distance_moved, edges_traversed=edges_traversed, arrived=False, success=True, reason=None)

# Apply monkey patch
import backend.app.simulation.state_manager as sm
sm.tick_movement = fast_tick_movement

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_dataset(num_ticks: int, forecast_horizon_ticks: int, output_csv: str):
    logger.info(f"Initializing SimulationStateManager for {num_ticks} ticks...")
    # Initialize deterministic simulation (seed 42, 85 groups)
    manager = SimulationStateManager(count=85, seed=42)
    
    logger.info("Running deterministic simulation loop...")
    
    # Pre-allocate dictionary mapping tick -> {edge_id: load}
    history_loads: Dict[int, Dict[str, int]] = {}
    all_edges_ever_seen = set()
    
    for tick in tqdm(range(num_ticks), desc="Simulating Ticks"):
        if tick > 0:
            manager.advance(1.0)
            
        # Fast extraction without iterating the entire graph
        tick_edge_loads = {}
        for g in manager.groups.values():
            edge_id = g.current_edge_id
            tick_edge_loads[edge_id] = tick_edge_loads.get(edge_id, 0) + g.count
            all_edges_ever_seen.add(edge_id)
            
        history_loads[manager.tick] = tick_edge_loads
        
    logger.info(f"Simulation complete. Generated {len(history_loads)} snapshots.")
    logger.info(f"Total unique active edges found: {len(all_edges_ever_seen)}")
    
    logger.info("Extracting features and targets...")
    dataset_rows = []
    
    # We can only create a valid row at tick T if T + H <= final_tick
    # and T >= 15 (to have enough history for the max lag of 15)
    final_tick = manager.tick
    valid_ticks = [t for t in sorted(history_loads.keys()) if 15 <= t <= (final_tick - forecast_horizon_ticks)]
    
    for edge_id in tqdm(all_edges_ever_seen, desc="Processing Edges"):
        # Precompute consecutive loads backwards for speed
        consecutive = 0
        consecutive_at_tick = {}
        for t in range(num_ticks):
            load = history_loads.get(t, {}).get(edge_id, 0)
            if load > 0:
                consecutive += 1
            else:
                consecutive = 0
            consecutive_at_tick[t] = consecutive
            
        for t in valid_ticks:
            current_load = history_loads[t].get(edge_id, 0)
            load_t_1 = history_loads[t-1].get(edge_id, 0)
            load_t_5 = history_loads[t-5].get(edge_id, 0)
            load_t_15 = history_loads[t-15].get(edge_id, 0)
            
            target_t = t + forecast_horizon_ticks
            target_load = history_loads[target_t].get(edge_id, 0)
            
            # Subsample purely 0 rows to keep dataset balanced and small
            if current_load == 0 and load_t_15 == 0 and target_load == 0 and consecutive_at_tick[t] == 0:
                import random
                if random.random() > 0.05:
                    continue

            dataset_rows.append({
                "edge_id": edge_id,
                "tick": t,
                "current_load": current_load,
                "load_t_minus_1": load_t_1,
                "load_t_minus_5": load_t_5,
                "load_t_minus_15": load_t_15,
                "absolute_load_change_1": current_load - load_t_1,
                "absolute_load_change_5": current_load - load_t_5,
                "absolute_load_change_15": current_load - load_t_15,
                "consecutive_occupied_ticks": consecutive_at_tick[t],
                "target_load_t_plus_h": target_load
            })
            
    df = pd.DataFrame(dataset_rows)
    # Sort chronologically to preserve strict temporal ordering
    df = df.sort_values(by=["tick", "edge_id"]).reset_index(drop=True)
    
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False)
    
    logger.info(f"Dataset saved to {output_csv}. Total valid rows: {len(df)}")
    
if __name__ == "__main__":
    NUM_TICKS = 6000
    HORIZON = 900
    OUTPUT_FILE = os.path.join(os.path.dirname(__file__), '../../data/processed/phase3_dataset.csv')
    
    generate_dataset(NUM_TICKS, HORIZON, OUTPUT_FILE)
