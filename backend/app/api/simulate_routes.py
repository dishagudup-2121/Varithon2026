from fastapi import APIRouter
from app.simulation.simulator import Simulator
from app.schemas.simulate import SimulateRequest

router = APIRouter()
simulator = Simulator()

@router.post('/api/simulate')
def simulate(request: SimulateRequest):
    """Run a what-if simulation scenario."""
    request_data = request.model_dump()
    result = simulator.run(request_data)
    return result
