import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.simulation.state_manager import SimulationStateManager
from app.simulation.crowd_aggregator import aggregate_crowd

def main():
    print("PHASE 2C-5 DIAGNOSTICS")
    print("=" * 50)
    
    print("Initializing SimulationStateManager (builds graph, generates pilgrims, plans routes)...")
    manager = SimulationStateManager(count=85, seed=42)
    
    print("Running Crowd Aggregator...")
    
    groups = list(manager.groups.values())
    snapshot = aggregate_crowd(manager.graph, groups)
    
    print(f"\nTotal Groups: {snapshot.summary.total_groups}")
    print(f"Total Pilgrims: {snapshot.summary.total_pilgrims}")
    print(f"Occupied Edge Count: {snapshot.summary.active_edge_count}")
    print(f"Moving Groups: {snapshot.summary.moving_group_count}")
    print(f"Stopped Groups: {snapshot.summary.stopped_group_count}")
    print(f"Congested Groups: {snapshot.summary.congested_group_count}")
    print(f"Unresolved Groups: {snapshot.summary.unresolved_group_count}")
    
    # top 10 edges
    edges_sorted = sorted(snapshot.edges, key=lambda e: e.pilgrim_count, reverse=True)
    
    if edges_sorted:
        print(f"\nMaximum Edge Pilgrim Count: {edges_sorted[0].pilgrim_count}")
    
    print("\nTop 10 Occupied Edges by Pilgrim Count:")
    for i, e in enumerate(edges_sorted[:10]):
        print(f"  {i+1}. {e.edge_id} -> {e.pilgrim_count} pilgrims ({e.group_count} groups)")
        
    print("\nDiagnostic PASSED")

if __name__ == "__main__":
    main()
