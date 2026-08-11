# VARI OS - AI/ML & Predictive Risk Engine (Member 1)

This module forms the predictive intelligence layer for VARI OS, transforming current zone conditions into a probability of future risk within 30-60 minutes.

> **IMPORTANT WARNING:** This model was trained and evaluated on synthetically generated data for hackathon prototyping. The relationships and coefficients are illustrative and are not derived from real Wari operational data.

## Features
- Forecasts imminent crowd and environmental stress dynamically.
- Outputs risk probability and categorical risk levels.
- Provides model-based feature explainability using Logisitic Regression coefficients.

## Architecture & Integration
The inference logic is encapsulated purely in Python and has no web framework dependencies. 

**Member 2 Integration Instructions:**
1. Do not spin up `api.py` in production. It is only for local testing.
2. Directly import `predict_risk` from `src/predict.py` in the main FastAPI backend.
```python
from member1_ai_ml.src.predict import predict_risk

result = predict_risk("Z6", features_dict, horizon=30)
```

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Generating Data & Training
```bash
python src/data_generator.py
python src/train_model.py
python src/evaluate_model.py
```

## Local Testing
```bash
pytest tests/
```
To run the local adapter for REST testing:
```bash
python src/api.py
```
Send a POST request to `http://localhost:8001/predict`.

## Output Contract
```json
{
  "zone_id": "Z6",
  "risk_probability": 0.82,
  "risk_level": "critical",
  "horizon_minutes": 30,
  "model_version": "v1.0.0",
  "top_features": [
    {
      "feature": "crowd_density",
      "contribution": 0.45
    }
  ]
}
```

## Risk Thresholds
- 0.00 – 0.35: Low
- 0.36 – 0.60: Medium
- 0.61 – 0.80: High
- 0.81 – 1.00: Critical
