"""Test GET /api/predict endpoint."""


def test_predict_returns_all_zones(client):
    """Predict endpoint returns a prediction for each of the 10 zones."""
    response = client.get("/api/predict")
    assert response.status_code == 200
    data = response.json()
    assert "predictions" in data
    assert len(data["predictions"]) == 10


def test_predict_has_model_version(client):
    """Response includes model_version."""
    response = client.get("/api/predict")
    data = response.json()
    assert "model_version" in data
    assert data["model_version"] != ""


def test_predict_risk_values_valid(client):
    """Risk probability is between 0 and 1; risk_level is valid."""
    response = client.get("/api/predict")
    data = response.json()
    for pred in data["predictions"]:
        assert 0.0 <= pred["risk_probability"] <= 1.0
        assert pred["risk_level"] in ("low", "medium", "high")
        assert pred["horizon_minutes"] > 0
        assert "zone_id" in pred


def test_predict_high_risk_zones_exist(client):
    """At least some zones should be high risk with the seeded data."""
    response = client.get("/api/predict")
    data = response.json()
    high_risk = [p for p in data["predictions"] if p["risk_level"] == "high"]
    # With our seed data (Z10 has 8500 crowd, 40.5C, 22% water), there should be high risk
    assert len(high_risk) >= 1
