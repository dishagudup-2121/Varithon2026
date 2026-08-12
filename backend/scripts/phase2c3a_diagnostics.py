import os
import sys

# Add parent directory to path to allow importing app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.simulation.state_manager import SimulationStateManager
from app.schemas.simulation import SimulationStateResponse

def main():
    print("Initializing Simulation State Manager...")
    try:
        manager = SimulationStateManager()
    except Exception as e:
        print(f"Error initializing manager: {e}")
        sys.exit(1)
        
    print("Retrieving state snapshot...")
    snapshot = manager.get_state_snapshot()
    
    print("\nValidating response schema...")
    try:
        response = SimulationStateResponse(
            simulation_time=manager.sim_time.isoformat(),
            tick=manager.tick,
            groups=snapshot
        )
        print("Schema validation successful!")
    except Exception as e:
        print(f"Schema validation failed: {e}")
        sys.exit(1)
        
    total_groups = len(snapshot)
    total_pilgrims = sum(g.count for g in snapshot)
    
    moving = sum(1 for g in snapshot if g.status == "moving")
    stopped = sum(1 for g in snapshot if g.status == "stopped")
    congested = sum(1 for g in snapshot if g.status == "congested")
    
    unique_edges = set(g.current_edge_id for g in snapshot)
    
    print("\n==================================================")
    print("PHASE 2C-3A DIAGNOSTIC REPORT")
    print("==================================================")
    print(f"Simulation Timestamp: {response.simulation_time}")
    print(f"Tick: {response.tick}")
    print(f"Number of Groups: {total_groups}")
    print(f"Total Pilgrims: {total_pilgrims}")
    print(f"Unique Current Edges Occupied: {len(unique_edges)}")
    print(f"Groups Moving: {moving}")
    print(f"Groups Stopped: {stopped}")
    print(f"Groups Congested: {congested}")
    print("==================================================")

if __name__ == "__main__":
    main()
