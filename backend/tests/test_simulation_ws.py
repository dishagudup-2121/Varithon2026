import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.simulation.simulation_loop import SimulationLoop
from unittest.mock import patch
import asyncio

@pytest.fixture
def test_client():
    with patch('app.main.simulation_loop_instance.start'):
        with TestClient(app) as client:
            yield client

def test_websocket_accepts_and_sends_initial_state(test_client):
    with test_client.websocket_connect("/api/simulation/ws") as websocket:
        data = websocket.receive_json()
        assert "simulation_time" in data
        assert "tick" in data
        assert "groups" in data

def test_rest_api_still_works_and_does_not_advance_tick(test_client):
    response_init = test_client.get("/api/simulation/state")
    initial_tick = response_init.json()["tick"]
    
    response = test_client.get("/api/simulation/state")
    assert response.status_code == 200
    assert response.json()["tick"] == initial_tick

def test_internal_route_not_exposed(test_client):
    with test_client.websocket_connect("/api/simulation/ws") as websocket:
        data = websocket.receive_json()
        if len(data["groups"]) > 0:
            assert "route" not in data["groups"][0]
            assert "current_edge_id" in data["groups"][0]

# --- Direct Unit Tests for SimulationLoop to bypass TestClient concurrency limits ---

class MockWS:
    def __init__(self, fail=False):
        self.messages = []
        self.fail = fail
    async def send_text(self, text):
        if self.fail:
            raise Exception("Network Error")
        self.messages.append(text)

@pytest.mark.asyncio
async def test_manual_tick_broadcasts_to_clients():
    loop = SimulationLoop()
    ws1 = MockWS()
    ws2 = MockWS()
    
    await loop.add_client(ws1)
    await loop.add_client(ws2)
    
    await loop.manual_tick()
    
    assert len(ws1.messages) == 1
    assert len(ws2.messages) == 1
    assert ws1.messages[0] == ws2.messages[0]

@pytest.mark.asyncio
async def test_failed_client_does_not_stop_broadcast():
    loop = SimulationLoop()
    ws_good = MockWS()
    ws_fail = MockWS(fail=True)
    
    await loop.add_client(ws_good)
    await loop.add_client(ws_fail)
    
    assert len(loop.clients) == 2
    
    await loop.manual_tick()
    
    # Good client got it
    assert len(ws_good.messages) == 1
    # Failed client is removed
    assert len(loop.clients) == 1
    assert ws_fail not in loop.clients

def test_production_environment_hides_endpoint():
    """Proves that under APP_ENV=production, the dev tick route returns 404 securely without stopping loop."""
    import sys
    import os
    import subprocess
    
    env = os.environ.copy()
    env["APP_ENV"] = "production"
    
    code = '''
import asyncio
from fastapi.testclient import TestClient
from app.main import app

with TestClient(app) as client:
    # Verify it returns 404
    resp = client.post("/api/simulation/dev/tick")
    assert resp.status_code == 404, f"Expected 404 but got {resp.status_code}"
    
    # Verify simulation loop still initialized
    from app.simulation.simulation_loop import simulation_loop_instance
    assert simulation_loop_instance.task is not None, "Simulation loop task should be running in production"
    '''
    
    result = subprocess.run(
        [sys.executable, "-c", code], 
        env=env, 
        cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("Subprocess stdout:", result.stdout)
        print("Subprocess stderr:", result.stderr)
        
    assert result.returncode == 0
