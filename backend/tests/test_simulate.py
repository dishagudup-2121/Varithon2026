"""Test POST /api/simulate endpoint."""


def test_simulate_close_route(client):
    """Simulate closing a route increases congestion."""
    response = client.post("/api/simulate", json={
        "action": "close_route",
        "route_id": "A",
        "extra_volunteers": 0,
    })
    assert response.status_code == 200
    data = response.json()
    assert "scenario" in data
    assert "before" in data
    assert "after" in data
    assert "delta" in data
    assert "simulation_method" in data
    assert "calibration_note" in data
    # Closing a route should increase congestion
    assert data["delta"]["congestion_percent"] > 0


def test_simulate_add_volunteers(client):
    """Simulate adding volunteers reduces congestion."""
    response = client.post("/api/simulate", json={
        "action": "add_volunteers",
        "route_id": "A",
        "extra_volunteers": 3,
    })
    assert response.status_code == 200
    data = response.json()
    # Adding volunteers should reduce congestion
    assert data["delta"]["congestion_percent"] < 0


def test_simulate_response_structure(client):
    """Response has correct metric fields."""
    response = client.post("/api/simulate", json={
        "action": "close_route",
        "route_id": "B",
    })
    data = response.json()
    for section in ("before", "after", "delta"):
        assert "congestion_percent" in data[section]
        assert "avg_eta_minutes" in data[section]
        assert "medical_access_percent" in data[section]


def test_simulate_has_calibration_note(client):
    """Response must include calibration disclaimer."""
    response = client.post("/api/simulate", json={"action": "close_route"})
    data = response.json()
    assert "calibration" in data["calibration_note"].lower()
