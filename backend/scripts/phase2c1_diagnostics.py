import os
import sys
import json
from datetime import datetime, timezone

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.graph.graph_builder import build_graph
from app.simulation.generator import generate_pilgrim_groups
from app.simulation.route_planner import plan_route

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
    
    print("Planning routes for all groups...")
    
    routed = 0
    unreachable = 0
    reasons = {}
    
    for g in groups:
        res = plan_route(G, g, zones_data)
        if res.status == "routed":
            routed += 1
        else:
            unreachable += 1
            reason = res.reason or "unknown"
            reasons[reason] = reasons.get(reason, 0) + 1
            
    print("\n==================================================")
    print("PHASE 2C-1 STATUS")
    print("==================================================")
    print("MOVEMENT: NOT IMPLEMENTED")
    print("GEOMETRIC INTERPOLATION: NOT IMPLEMENTED")
    print("WEBSOCKET: NOT IMPLEMENTED")
    print("REAL-TIME STREAMING: NOT IMPLEMENTED")
    print("DYNAMIC CONGESTION WEIGHTS: NOT IMPLEMENTED")
    print("FLOOD-AWARE ROUTING: NOT IMPLEMENTED")
    print("AI/ML PREDICTION: NOT IMPLEMENTED")
    
    print("\n--- ROUTE PLANNING STATISTICS ---")
    print(f"- Total groups: {len(groups)}")
    print(f"- Successfully routed: {routed}")
    print(f"- Unreachable groups: {unreachable}")
    if unreachable > 0:
        print("  Reasons:")
        for r, count in reasons.items():
            print(f"    - {r}: {count}")

if __name__ == "__main__":
    main()
