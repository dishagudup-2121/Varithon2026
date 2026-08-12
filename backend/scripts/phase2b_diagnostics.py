import os
import sys
import json
from datetime import datetime, timezone

# Add parent directory to path so we can import app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.graph.graph_builder import build_graph
from app.simulation.generator import generate_pilgrim_groups

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
    
    # We will generate ~100 groups as per requirement ("30-100 groups")
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
    
    # Compute statistics
    total_pilgrims = sum(g.count for g in groups)
    min_size = min(g.count for g in groups)
    max_size = max(g.count for g in groups)
    min_speed = min(g.speed_mps for g in groups)
    max_speed = max(g.speed_mps for g in groups)
    
    dest_zones = set(g.destination_zone_id for g in groups)
    source_edges = set(g.current_edge_id for g in groups)
    
    edge_counts = {}
    for g in groups:
        edge_counts[g.current_edge_id] = edge_counts.get(g.current_edge_id, 0) + 1
    
    groups_sharing = sum(count for count in edge_counts.values() if count > 1)
    
    print("\n==================================================")
    print("PHASE 2B STATUS")
    print("==================================================")
    print("MOVEMENT: NOT IMPLEMENTED")
    print("ROUTING: NOT IMPLEMENTED")
    print("WEBSOCKET: NOT IMPLEMENTED")
    print("FRONTEND: NOT MODIFIED")
    
    print("\n--- SYNTHETIC PILGRIM GROUP STATISTICS ---")
    print(f"- number of groups: {len(groups)}")
    print(f"- total simulated pilgrims: {total_pilgrims}")
    print(f"- min/max group size: {min_size} / {max_size}")
    print(f"- min/max speed: {min_speed:.2f} m/s / {max_speed:.2f} m/s")
    print(f"- number of destination zones: {len(dest_zones)}")
    print(f"- number of source edges: {len(source_edges)}")
    print(f"- number of groups sharing edges: {groups_sharing}")
    print(f"- random seed: {seed}")
    print(f"- simulation timestamp: {sim_time.isoformat()}")

if __name__ == "__main__":
    main()
