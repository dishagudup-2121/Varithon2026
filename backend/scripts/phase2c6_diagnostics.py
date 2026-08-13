import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.simulation.state_manager import SimulationStateManager
from app.simulation.crowd_aggregator import aggregate_crowd

def main():
    print("PHASE 2C-6 GEOMETRY RESOLUTION DIAGNOSTICS")
    print("=" * 50)
    
    # 1. Load static edge geometry
    json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend/src/data/geospatial/edge_geometry.json'))
    
    if not os.path.exists(json_path):
        print("ERROR: edge_geometry.json not found!")
        sys.exit(1)
        
    with open(json_path, 'r') as f:
        edge_geometry = json.load(f)
        
    file_size_kb = os.path.getsize(json_path) / 1024
    total_generated = len(edge_geometry)
    
    print(f"Total edge geometries generated: {total_generated}")
    print(f"edge_geometry.json file size: {file_size_kb:.2f} KB")
    
    # 2. Get CrowdEdgeLoad entries
    manager = SimulationStateManager(count=85, seed=42)
    groups = list(manager.groups.values())
    snapshot = aggregate_crowd(manager.graph, groups)
    
    entries_received = len(snapshot.edges)
    print(f"\nNumber of CrowdEdgeLoad entries received: {entries_received}")
    
    # 3. Resolve
    resolved = 0
    unresolved_ids = []
    
    for edge in snapshot.edges:
        if edge.edge_id in edge_geometry:
            resolved += 1
        else:
            unresolved_ids.append(edge.edge_id)
            
    unresolved = len(unresolved_ids)
    
    print(f"Number of edge IDs successfully resolved to geometry: {resolved}")
    print(f"Number of unresolved edge IDs: {unresolved}")
    if unresolved > 0:
        print(f"Unresolved edge IDs: {unresolved_ids}")
        
    percentage = (resolved / entries_received * 100) if entries_received > 0 else 0
    print(f"Percentage of crowd edges successfully rendered/resolved: {percentage:.2f}%")

if __name__ == "__main__":
    main()
