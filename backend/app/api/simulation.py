from fastapi import APIRouter
from ..schemas.simulation import SimulationStateResponse
from ..simulation.state_manager import SimulationStateManager

router = APIRouter(prefix="/api/simulation", tags=["Simulation"])

# Single initialization per application instance
manager = SimulationStateManager()

@router.get("/state", response_model=SimulationStateResponse)
def get_simulation_state():
    """
    Returns a read-only deterministic snapshot of the simulation state.
    Does NOT advance the simulation tick.
    """
    snapshot = manager.get_state_snapshot()
    
    return SimulationStateResponse(
        simulation_time=manager.sim_time.isoformat(),
        tick=manager.tick,
        groups=snapshot
    )
