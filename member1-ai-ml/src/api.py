from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from predict import predict_risk

app = FastAPI(
    title="VARI OS - ML Prediction API",
    description="Local test adapter for Member 1 ML Module. Member 2 should import predict_risk directly.",
    version="1.0.0"
)

class Features(BaseModel):
    crowd_density: float
    temperature_c: float
    humidity_pct: float
    water_availability_pct: float
    hour_of_day: int

class PredictionRequest(BaseModel):
    zone_id: str
    features: Features
    horizon_minutes: int = 30

@app.post("/predict")
def predict_endpoint(request: PredictionRequest):
    try:
        result = predict_risk(
            zone_id=request.zone_id,
            features=request.features.dict(),
            horizon=request.horizon_minutes
        )
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
