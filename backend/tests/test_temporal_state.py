import pytest
import json
import asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.simulation.temporal_manager import TemporalStateManager
from app.schemas.crowd import TemporalCrowdSnapshot, CrowdStateSnapshot, CrowdSummary

@pytest.mark.asyncio
async def test_temporal_history_recording():
    # Because simulation_loop_instance starts in lifespan,
    # let's test the endpoint directly using the test client which triggers lifespan
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Give it a moment to record tick 0 and maybe tick 1
        await asyncio.sleep(1.5)
        
        response = await client.get("/api/simulation/history?limit=10")
        assert response.status_code == 200
        history = response.json()
        
        assert len(history) >= 1
        
        # Verify tick 0 is present and strictly ordered
        ticks = [item["tick"] for item in history]
        assert ticks == sorted(ticks), "History is not chronologically ordered"
        
        # Ensure tick 0 exists if we caught it fast enough
        assert 0 in ticks, "Tick 0 was not recorded"

def test_temporal_manager_capacity():
    manager = TemporalStateManager(max_ticks=5)
    
    # Add 10 snapshots
    for i in range(10):
        snap = TemporalCrowdSnapshot(
            tick=i,
            simulation_time="2026-08-12T12:00:00Z",
            snapshot=CrowdStateSnapshot(
                summary=CrowdSummary(
                    total_pilgrims=0, total_groups=0, active_edge_count=0,
                    moving_group_count=0, stopped_group_count=0, congested_group_count=0,
                    unresolved_group_count=0
                ),
                edges=[]
            )
        )
        manager.append(snap)
        
    history = manager.get_history(limit=10)
    assert len(history) == 5, "Capacity limit exceeded"
    assert history[0].tick == 5
    assert history[-1].tick == 9
    
def test_temporal_snapshot_memory_measurement():
    """Explicitly measures the serialized JSON payload size of a snapshot."""
    from app.simulation.simulation_loop import simulation_loop_instance
    manager = simulation_loop_instance.manager
    
    # We must have some groups to get a meaningful snapshot size
    if not manager.groups:
        manager._initialize_state(85, 42)
        
    from app.simulation.crowd_aggregator import aggregate_crowd
    crowd = aggregate_crowd(manager.graph, list(manager.groups.values()))
    
    ts = TemporalCrowdSnapshot(
        tick=manager.tick,
        simulation_time=manager.sim_time.isoformat(),
        snapshot=crowd
    )
    
    json_str = ts.model_dump_json()
    byte_size = len(json_str.encode('utf-8'))
    
    print("\n" + "="*50)
    print(f"TEMPORAL SNAPSHOT MEMORY MEASUREMENT")
    print(f"Total Occupied Edges: {len(crowd.edges)}")
    print(f"Serialized JSON size: {byte_size} bytes ({byte_size / 1024:.2f} KB) per tick")
    print(f"Estimated 1 hour (3600 ticks) size: {(byte_size * 3600) / (1024 * 1024):.2f} MB")
    print("="*50 + "\n")
    
    # Assert sanity check - should be well under 100KB per tick
    assert byte_size < 100 * 1024
