import os
import sys
import json
from datetime import datetime, timezone

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.graph.graph_builder import build_graph
from app.simulation.generator import generate_pilgrim_groups
from app.simulation.route_planner import plan_route
from app.simulation.movement_engine import tick_movement

def main():
    osm_path = os.path.join(os.path.dirname(__file__), '../../osm_data.json')
    if not os.path.exists(osm_path):
        print(f"Error: Could not find {osm_path}")
        return
        
    print("Loading OSM data...")
    with open(osm_path, 'r') as f:
        osm_data = json.load(f)
        
    print("Building Phase 2A Graph...")
    G = build_graph(osm_data)
    
    zones_path = os.path.join(os.path.dirname(__file__), '../../frontend/src/data/geospatial/zones.json')
    if not os.path.exists(zones_path):
        print(f"Error: Could not find {zones_path}")
        return
        
    print("Loading Phase 1 Zones...")
    with open(zones_path, 'r') as f:
        zones_data = json.load(f)
        
    print("Generating Synthetic Pilgrim Groups...")
    sim_time = datetime(2026, 8, 12, 12, 0, tzinfo=timezone.utc)
    seed = 42
    
    groups = generate_pilgrim_groups(
        graph=G,
        zones_data=zones_data,
        simulation_time=sim_time,
        count=85,
        seed=seed,
        min_group_size=50,
        max_group_size=500,
        min_speed_mps=0.5,
        max_speed_mps=1.5
    )
    
    print("Planning routes for all groups (Phase 2C-1)...")
    
    routed_groups = []
    for g in groups:
        res = plan_route(G, g, zones_data)
        if res.status == "routed":
            g.route = res.edge_ids
            routed_groups.append(g)

    print("Running Movement Engine Diagnostic (Phase 2C-2)...")
    DELTA_TIME_S = 60.0 # 1 minute tick
    
    success_count = 0
    failure_count = 0
    arrived_count = 0
    total_dist_moved = 0.0
    total_transitions = 0
    reasons = {}
    
    for g in routed_groups:
        move_res = tick_movement(G, g, DELTA_TIME_S)
        
        if move_res.success:
            success_count += 1
            total_dist_moved += move_res.distance_moved_m
            total_transitions += move_res.edges_traversed
            if move_res.arrived:
                arrived_count += 1
        else:
            failure_count += 1
            reason = move_res.reason or "unknown"
            reasons[reason] = reasons.get(reason, 0) + 1

    moving = sum(1 for g in routed_groups if g.status == "moving")
    stopped = sum(1 for g in routed_groups if g.status == "stopped")

    print("\n==================================================")
    print("PHASE 2C-2 STATUS")
    print("==================================================")
    print("WEBSOCKET: NOT IMPLEMENTED")
    print("FRONTEND ANIMATION: NOT IMPLEMENTED")
    print("REAL-TIME STREAMING: NOT IMPLEMENTED")
    print("CONGESTION/FLOOD AWARENESS: NOT IMPLEMENTED")
    print("AI/ML: NOT IMPLEMENTED")
    
    print("\n--- MOVEMENT ENGINE STATISTICS (60s tick) ---")
    print(f"- Total initially routed groups: {len(routed_groups)}")
    print(f"- Moving groups (after tick): {moving}")
    print(f"- Stopped groups (after tick): {stopped}")
    print(f"- Successful movements: {success_count}")
    print(f"- Movement failures: {failure_count}")
    print(f"- Arrivals: {arrived_count}")
    print(f"- Total distance moved: {total_dist_moved:.2f} m")
    print(f"- Total edge transitions: {total_transitions}")
    
    if failure_count > 0:
        print("  Failure Reasons:")
        for r, count in reasons.items():
            print(f"    - {r}: {count}")

if __name__ == "__main__":
    main()
