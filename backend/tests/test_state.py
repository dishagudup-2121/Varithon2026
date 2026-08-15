"""Test GET /api/state endpoint."""


def test_state_returns_zones(client):
    """State endpoint returns 10 seeded zones."""
    response = client.get("/api/state")
    assert response.status_code == 200
    data = response.json()
    assert "zones" in data
    assert len(data["zones"]) == 10


def test_state_returns_resources(client):
    """State endpoint returns 12 seeded resources."""
    response = client.get("/api/state")
    assert response.status_code == 200
    data = response.json()
    assert "resources" in data
    assert len(data["resources"]) == 12


def test_state_returns_agents(client):
    """State endpoint returns synthetic agent groups."""
    response = client.get("/api/state")
    assert response.status_code == 200
    data = response.json()
    assert "agents" in data
    assert len(data["agents"]) > 0


def test_state_zone_structure(client):
    """Each zone has the correct fields."""
    response = client.get("/api/state")
    data = response.json()
    zone = data["zones"][0]
    required_fields = ["zone_id", "name", "lat", "lng", "crowd_count",
                        "temperature_c", "humidity_percent", "water_availability_percent"]
    for field in required_fields:
        assert field in zone, f"Missing field: {field}"


def test_state_has_timestamp(client):
    """State response includes a timestamp."""
    response = client.get("/api/state")
    data = response.json()
    assert "timestamp" in data
