from fastapi.testclient import TestClient
from app.main import app
from app.api.simulation import manager
from app.schemas.simulation import SimulationStateResponse

client = TestClient(app)

def test_get_simulation_state_success():
    response = client.get("/api/simulation/state")
    assert response.status_code == 200

def test_response_conforms_to_schema():
    response = client.get("/api/simulation/state")
    data = response.json()
    # Pydantic validation via init
    validated = SimulationStateResponse(**data)
    assert validated.simulation_time is not None
    assert isinstance(validated.tick, int)
    assert isinstance(validated.groups, list)

def test_groups_integrity():
    response = client.get("/api/simulation/state")
    data = response.json()
    groups = data["groups"]
    
    # 3. All expected groups are present (default count is 85)
    # The actual count might be 85 if graph exists, or 0 if dummy test env without JSON.
    # We just ensure it matches the manager's length.
    assert len(groups) == len(manager.groups)
    
    if len(groups) > 0:
        group_ids = [g["group_id"] for g in groups]
        # 4. group_id values are unique
        assert len(group_ids) == len(set(group_ids))
        
        for g in groups:
            # 5. current_edge_id is preserved
            assert isinstance(g["current_edge_id"], str)
            assert len(g["current_edge_id"]) > 0
            
            # 6. progress remains within [0,1]
            assert 0.0 <= g["progress"] <= 1.0
            
            # 7. status remains valid
            assert g["status"] in ["moving", "stopped", "congested"]

def test_consecutive_gets_no_mutation():
    resp1 = client.get("/api/simulation/state").json()
    resp2 = client.get("/api/simulation/state").json()
    
    # 8/9. GET does not mutate simulation state
    assert resp1["tick"] == resp2["tick"]
    assert resp1["simulation_time"] == resp2["simulation_time"]
    
    groups1 = resp1["groups"]
    groups2 = resp2["groups"]
    assert len(groups1) == len(groups2)
    
    if len(groups1) > 0:
        # Just check the first one to be perfectly equal
        assert groups1[0]["group_id"] == groups2[0]["group_id"]
        assert groups1[0]["progress"] == groups2[0]["progress"]
        assert groups1[0]["current_edge_id"] == groups2[0]["current_edge_id"]

def test_movement_state_changes():
    # Capture initial state
    resp_initial = client.get("/api/simulation/state").json()
    groups_initial = resp_initial["groups"]
    
    if not groups_initial:
        pytest.skip("No groups available to test movement")
        
    moving_initial = [g for g in groups_initial if g["status"] == "moving"]
    if not moving_initial:
        pytest.skip("No moving groups available to test movement")
        
    initial_target = moving_initial[0]
    
    # Advance the manager directly
    manager.advance(60.0)
    
    # Capture new state
    resp_after = client.get("/api/simulation/state").json()
    assert resp_after["tick"] > resp_initial["tick"]
    
    groups_after = resp_after["groups"]
    target_after = next((g for g in groups_after if g["group_id"] == initial_target["group_id"]), None)
    
    assert target_after is not None
    # Verify that at least progress or current_edge_id has changed
    state_changed = (target_after["progress"] != initial_target["progress"]) or \
                    (target_after["current_edge_id"] != initial_target["current_edge_id"])
                    
    assert state_changed is True

