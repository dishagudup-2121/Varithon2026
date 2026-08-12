import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.simulation.state_manager import SimulationStateManager

def main():
    print("Initializing Simulation State Manager (Phase 2C-3B)...")
    try:
        manager = SimulationStateManager()
    except Exception as e:
        print(f"Error initializing manager: {e}")
        sys.exit(1)
        
    print("Retrieving state snapshot with resolved positions...")
    snapshot = manager.get_state_snapshot()
    
    total = len(snapshot)
    resolved = 0
    failed = 0
    
    print("\nValidating positions...")
    for group in snapshot:
        pos = group.position
        if pos is None:
            print(f"WARNING: Group {group.group_id} failed to resolve position on edge {group.current_edge_id}")
            failed += 1
        else:
            if not (-90.0 <= pos.lat <= 90.0 and -180.0 <= pos.lng <= 180.0):
                print(f"ERROR: Group {group.group_id} resolved to invalid bounds ({pos.lat}, {pos.lng})")
                sys.exit(1)
            resolved += 1
            
    print("\nAdvancing simulation by 60s...")
    manager.advance(60.0)
    snapshot2 = manager.get_state_snapshot()
    
    changed = 0
    for g1, g2 in zip(snapshot, snapshot2):
        if g1.position and g2.position:
            if g1.position.lat != g2.position.lat or g1.position.lng != g2.position.lng:
                changed += 1

    print("\n==================================================")
    print("PHASE 2C-3B DIAGNOSTIC REPORT")
    print("==================================================")
    print(f"Total Groups Evaluated: {total}")
    print(f"Successfully Resolved Positions: {resolved}")
    print(f"Failed Resolutions: {failed}")
    print(f"Positions Changed after 60s Advance: {changed}")
    print("==================================================")
    
    if failed > 0:
        print("Diagnostic FAILED due to unresolvable positions.")
        sys.exit(1)

if __name__ == "__main__":
    main()
