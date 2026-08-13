import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.simulation.state_manager import SimulationStateManager

def main():
    print("Generating static edge_geometry.json...")
    
    # Initialize the SimulationStateManager to build the authoritative Phase 2A graph
    manager = SimulationStateManager(count=85, seed=42)
    graph = manager.graph
    
    edge_geometry = {}
    
    for u, v, data in graph.edges(data=True):
        edge_id = data.get("edge_id")
        geometry = data.get("geometry")
        
        # Valid NetworkX geometry format is [[lon, lat], [lon, lat], ...]
        if edge_id and geometry:
            edge_geometry[edge_id] = geometry
            
    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend/src/data/geospatial/edge_geometry.json'))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    
    with open(out_path, "w") as f:
        # Generate a compact JSON file without indentation for optimal payload size
        json.dump(edge_geometry, f, separators=(',', ':'))
        
    print(f"Total edge geometries generated: {len(edge_geometry)}")
    print(f"File saved to: {out_path}")
    print(f"File size: {os.path.getsize(out_path) / 1024:.2f} KB")

if __name__ == "__main__":
    main()
