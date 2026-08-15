"""Unit test for the OR-Tools ResourceOptimizer directly."""
from app.decision.optimizer import ResourceOptimizer
from app.decision.distance import haversine, estimate_eta


def test_haversine_same_point():
    """Distance between a point and itself is 0."""
    assert haversine(18.5, 73.8, 18.5, 73.8) == 0.0


def test_haversine_known_distance():
    """Pune (18.52, 73.86) to Pandharpur (17.68, 75.33) is roughly 170-180 km."""
    dist = haversine(18.52, 73.86, 17.68, 75.33)
    assert 160 < dist < 200


def test_estimate_eta():
    """40 km at 40 km/h should be 60 minutes."""
    assert estimate_eta(40.0, 40.0) == 60.0


def test_estimate_eta_zero_speed():
    """Zero speed returns fallback 999."""
    assert estimate_eta(10.0, 0.0) == 999.0


def test_optimizer_basic():
    """Optimizer assigns resources to high-risk zones."""
    optimizer = ResourceOptimizer()

    predictions = [
        {"zone_id": "Z1", "risk_probability": 0.8, "risk_level": "high"},
        {"zone_id": "Z2", "risk_probability": 0.3, "risk_level": "low"},
        {"zone_id": "Z3", "risk_probability": 0.5, "risk_level": "medium"},
    ]
    resources = [
        {"resource_id": "AMB1", "resource_type": "ambulance", "zone_id": "Z2", "available": True},
        {"resource_id": "VOL1", "resource_type": "volunteer_team", "zone_id": "Z3", "available": True},
        {"resource_id": "AMB2", "resource_type": "ambulance", "zone_id": "Z1", "available": False},
    ]
    zone_coords = {
        "Z1": (18.52, 73.86),
        "Z2": (18.51, 73.93),
        "Z3": (18.35, 74.03),
    }

    assignments = optimizer.optimize(predictions, resources, zone_coords)

    # Should only use available resources (AMB1, VOL1)
    assigned_ids = {a["resource_id"] for a in assignments}
    assert "AMB2" not in assigned_ids  # unavailable

    # High-risk Z1 should get at least one assignment
    z1_assignments = [a for a in assignments if a["to_zone_id"] == "Z1"]
    assert len(z1_assignments) >= 1

    # Low-risk Z2 should NOT be a target
    z2_assignments = [a for a in assignments if a["to_zone_id"] == "Z2"]
    assert len(z2_assignments) == 0


def test_optimizer_no_target_zones():
    """When all zones are low-risk, optimizer returns empty list."""
    optimizer = ResourceOptimizer()
    predictions = [
        {"zone_id": "Z1", "risk_probability": 0.1, "risk_level": "low"},
    ]
    resources = [
        {"resource_id": "AMB1", "resource_type": "ambulance", "zone_id": "Z1", "available": True},
    ]
    zone_coords = {"Z1": (18.52, 73.86)}

    assignments = optimizer.optimize(predictions, resources, zone_coords)
    assert assignments == []


def test_optimizer_no_available_resources():
    """When no resources are available, optimizer returns empty list."""
    optimizer = ResourceOptimizer()
    predictions = [
        {"zone_id": "Z1", "risk_probability": 0.8, "risk_level": "high"},
    ]
    resources = [
        {"resource_id": "AMB1", "resource_type": "ambulance", "zone_id": "Z1", "available": False},
    ]
    zone_coords = {"Z1": (18.52, 73.86)}

    assignments = optimizer.optimize(predictions, resources, zone_coords)
    assert assignments == []
