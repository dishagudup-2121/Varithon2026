"""Test POST /api/actions/approve and GET /api/actions/log endpoints."""


def _create_recommendation(client):
    """Helper: create a recommendation so we have something to approve."""
    response = client.get("/api/recommend")
    return response.json()["recommendation_id"]


def test_approve_recommendation(client):
    """Approving a pending recommendation succeeds."""
    rec_id = _create_recommendation(client)
    response = client.post("/api/actions/approve", json={
        "recommendation_id": rec_id,
        "decision": "approve",
        "modified_assignments": [],
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "recorded"
    assert data["decision"] == "approve"
    assert data["recommendation_id"] == rec_id


def test_reject_recommendation(client):
    """Rejecting a pending recommendation succeeds."""
    rec_id = _create_recommendation(client)
    response = client.post("/api/actions/approve", json={
        "recommendation_id": rec_id,
        "decision": "reject",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["decision"] == "reject"


def test_modify_recommendation(client):
    """Modifying a recommendation with changed assignments succeeds."""
    rec_id = _create_recommendation(client)
    response = client.post("/api/actions/approve", json={
        "recommendation_id": rec_id,
        "decision": "modify",
        "modified_assignments": [{"resource_id": "AMB1", "to_zone_id": "Z3"}],
    })
    assert response.status_code == 200
    data = response.json()
    assert data["decision"] == "modify"


def test_cannot_approve_twice(client):
    """Cannot approve an already-approved recommendation."""
    rec_id = _create_recommendation(client)
    # First approval
    client.post("/api/actions/approve", json={
        "recommendation_id": rec_id,
        "decision": "approve",
    })
    # Second approval should fail
    response = client.post("/api/actions/approve", json={
        "recommendation_id": rec_id,
        "decision": "approve",
    })
    assert response.status_code == 400


def test_approve_nonexistent_fails(client):
    """Approving a non-existent recommendation returns 404."""
    response = client.post("/api/actions/approve", json={
        "recommendation_id": "REC-DOES-NOT-EXIST",
        "decision": "approve",
    })
    assert response.status_code == 404


def test_action_log(client):
    """GET /api/actions/log returns recorded actions."""
    # Create and approve one to ensure there's at least one log entry
    rec_id = _create_recommendation(client)
    client.post("/api/actions/approve", json={
        "recommendation_id": rec_id,
        "decision": "approve",
    })
    response = client.get("/api/actions/log")
    assert response.status_code == 200
    data = response.json()
    assert "actions" in data
    assert len(data["actions"]) >= 1
    log_entry = data["actions"][0]
    assert "log_id" in log_entry
    assert "recommendation_id" in log_entry
    assert "decision" in log_entry
