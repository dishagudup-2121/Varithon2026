# VARI OS API Contract v1

Base URL:
`http://localhost:8000`

All JSON field names use `snake_case`.

## GET /api/health

Response:

```json
{
  "status": "ok",
  "version": "0.1.0"
}
```

## GET /api/state

Returns the current Digital Twin state.

```json
{
  "timestamp": "2026-08-11T14:00:00Z",
  "zones": [
    {
      "zone_id": "Z6",
      "name": "Zone 6",
      "lat": 18.23,
      "lng": 74.12,
      "crowd_count": 5200,
      "temperature_c": 41.0,
      "humidity_percent": 68.0,
      "water_availability_percent": 28.0
    }
  ],
  "agents": [
    {
      "agent_id": "G001",
      "count": 150,
      "lat": 18.2301,
      "lng": 74.1202,
      "route_id": "R12",
      "status": "moving"
    }
  ],
  "resources": [
    {
      "resource_id": "AMB3",
      "resource_type": "ambulance",
      "zone_id": "Z2",
      "available": true
    }
  ]
}
```

## GET /api/predict

Response:

```json
{
  "predictions": [
    {
      "zone_id": "Z6",
      "risk_probability": 0.78,
      "risk_level": "high",
      "horizon_minutes": 30,
      "confidence_source": "model.predict_proba()"
    }
  ],
  "model_version": "risk-model-v1"
}
```

`risk_probability` MUST come from the trained model at demo time. It must not be hardcoded.

## GET /api/recommend

Response:

```json
{
  "target_zone_id": "Z6",
  "assignments": [
    {
      "resource_id": "AMB3",
      "resource_type": "ambulance",
      "from_zone_id": "Z2",
      "to_zone_id": "Z6",
      "eta_minutes": 11,
      "reason": "High predicted risk with available resource."
    }
  ],
  "optimization_method": "OR-Tools"
}
```

## POST /api/simulate

Request:

```json
{
  "action": "close_route",
  "route_id": "A",
  "extra_volunteers": 0
}
```

Response:

```json
{
  "scenario": {
    "action": "close_route",
    "route_id": "A"
  },
  "before": {
    "congestion_percent": 62.0,
    "avg_eta_minutes": 18.0,
    "medical_access_percent": 91.0
  },
  "after": {
    "congestion_percent": 80.0,
    "avg_eta_minutes": 27.0,
    "medical_access_percent": 76.0
  },
  "delta": {
    "congestion_percent": 18.0,
    "avg_eta_minutes": 9.0,
    "medical_access_percent": -15.0
  },
  "simulation_method": "NetworkX graph-flow approximation",
  "calibration_note": "Illustrative MVP coefficients; production values require historical Wari calibration."
}
```

## WebSocket /ws/twin

Purpose:
Live Digital Twin agent/resource state.

Message:

```json
{
  "timestamp": "2026-08-11T14:00:01Z",
  "agents": [
    {
      "agent_id": "G001",
      "count": 150,
      "lat": 18.2301,
      "lng": 74.1202,
      "route_id": "R12",
      "status": "moving"
    }
  ]
}
```

## POST /api/actions/approve

Request:

```json
{
  "recommendation_id": "REC-001",
  "decision": "approve",
  "modified_assignments": []
}
```

Allowed decision values:
- `approve`
- `modify`
- `reject`

## GET /api/explain

Response:

```json
{
  "language": "en",
  "summary": "Zone 6 has the highest predicted risk...",
  "reasoning": "Crowd density is increasing while water availability is decreasing.",
  "confidence_caveat": "Risk probability comes from the trained model..."
}
```

For Marathi, use:
`GET /api/explain?language=mr`

## Breaking-change rule

Changing a required field, field type, endpoint name, or response structure requires:
1. update this document,
2. update Pydantic schemas,
3. update frontend TypeScript types,
4. test all affected modules.
