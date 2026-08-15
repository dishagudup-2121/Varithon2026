"""Test GET /api/recommend endpoint."""


def test_recommend_returns_assignments(client):
    """Recommend endpoint returns OR-Tools assignments."""
    response = client.get("/api/recommend")
    assert response.status_code == 200
    data = response.json()
    assert "recommendation_id" in data
    assert "target_zone_id" in data
    assert "assignments" in data
    assert data["optimization_method"] == "OR-Tools CP-SAT"


def test_recommend_assignments_have_required_fields(client):
    """Each assignment has the required fields."""
    response = client.get("/api/recommend")
    data = response.json()
    if data["assignments"]:
        assignment = data["assignments"][0]
        required = ["resource_id", "resource_type", "from_zone_id",
                     "to_zone_id", "eta_minutes", "reason"]
        for field in required:
            assert field in assignment, f"Missing field: {field}"


def test_recommend_generates_unique_ids(client):
    """Each call generates a new recommendation ID."""
    r1 = client.get("/api/recommend").json()
    r2 = client.get("/api/recommend").json()
    assert r1["recommendation_id"] != r2["recommendation_id"]


def test_recommend_assigns_available_resources_only(client):
    """Only available resources should appear in assignments."""
    response = client.get("/api/recommend")
    data = response.json()
    # AMB4 and VOL3 are unavailable in seed data
    unavailable = {"AMB4", "VOL3"}
    assigned_ids = {a["resource_id"] for a in data["assignments"]}
    assert assigned_ids.isdisjoint(unavailable), "Unavailable resource was assigned"
