from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from typing import List
from ..schemas.simulation import SimulationStateResponse
from ..schemas.crowd import TemporalCrowdSnapshot
from ..simulation.simulation_loop import simulation_loop_instance

router = APIRouter(prefix="/api/simulation", tags=["Simulation"])

@router.get("/state", response_model=SimulationStateResponse)
async def get_simulation_state():
    """
    Returns a read-only deterministic snapshot of the simulation state.
    Does NOT advance the simulation tick.
    """
    return await simulation_loop_instance.get_state_snapshot_safe()

@router.get("/history", response_model=List[TemporalCrowdSnapshot])
async def get_simulation_history(limit: int = Query(60, description="Number of recent ticks to return")):
    """
    Returns the temporal crowd history up to the specified limit.
    The server strictly bounds the response to a maximum limit (e.g. 900 ticks) to protect memory/network.
    """
    # Uses the shared temporal_manager from the simulation loop
    return simulation_loop_instance.temporal_manager.get_history(limit=limit, max_limit=900)

@router.websocket("/ws")
async def simulation_websocket(websocket: WebSocket):
    await websocket.accept()
    
    # Send initial state immediately
    initial_state = await simulation_loop_instance.get_state_snapshot_safe()
    try:
        await websocket.send_text(initial_state.model_dump_json())
    except Exception:
        return
        
    await simulation_loop_instance.add_client(websocket)
    
    try:
        # Keep connection alive natively without relying on client messaging protocol.
        # This blocks until the client disconnects or an error occurs.
        while True:
            await websocket.receive()
    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        simulation_loop_instance.remove_client(websocket)

import os
APP_ENV = os.getenv("APP_ENV", "development")

if APP_ENV in ["development", "test"]:
    @router.post("/dev/tick")
    async def dev_trigger_tick():
        """Manual tick trigger for deterministic testing without sleeping."""
        await simulation_loop_instance.manual_tick()
        return {"status": "ok"}
