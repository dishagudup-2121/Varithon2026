import os
import sys

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from predict import predict_risk, get_risk_level

def test_risk_levels():
    assert get_risk_level(0.1) == "low"
    assert get_risk_level(0.4) == "medium"
    assert get_risk_level(0.7) == "high"
    assert get_risk_level(0.9) == "critical"

def test_predict_risk_30m():
    features = {
        'crowd_density': 0.85,
        'temperature_c': 40.0,
        'humidity_pct': 0.6,
        'water_availability_pct': 0.2,
        'hour_of_day': 14
    }
    result = predict_risk("Z1", features, 30)
    
    assert "zone_id" in result
    assert result["zone_id"] == "Z1"
    assert 0.0 <= result["risk_probability"] <= 1.0
    assert result["risk_level"] in ["low", "medium", "high", "critical"]
    assert result["horizon_minutes"] == 30
    assert "top_features" in result

def test_predict_risk_60m():
    features = {
        'crowd_density': 0.3,
        'temperature_c': 30.0,
        'humidity_pct': 0.4,
        'water_availability_pct': 0.8,
        'hour_of_day': 8
    }
    result = predict_risk("Z2", features, 60)
    
    assert result["zone_id"] == "Z2"
    assert result["horizon_minutes"] == 60
