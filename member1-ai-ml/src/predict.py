import joblib
import json
import os
import pandas as pd
import numpy as np

# Load models globally so they are cached in memory for the FastAPI app
try:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_30m = joblib.load(os.path.join(BASE_DIR, "models", "risk_model_30m.joblib"))
    model_60m = joblib.load(os.path.join(BASE_DIR, "models", "risk_model_60m.joblib"))
    
    with open(os.path.join(BASE_DIR, "models", "model_metadata.json"), "r") as f:
        metadata = json.load(f)
except Exception as e:
    print(f"Warning: Could not load models on startup: {e}")
    model_30m = None
    model_60m = None
    metadata = {}

def get_risk_level(prob: float) -> str:
    if prob <= 0.35:
        return "low"
    elif prob <= 0.60:
        return "medium"
    elif prob <= 0.80:
        return "high"
    else:
        return "critical"

def _explain_lr(model, df):
    """
    Provides explainability by multiplying LR coefficients by the scaled feature values.
    Since we use a pipeline with ColumnTransformer, we need to extract the processed features.
    """
    try:
        classifier = model.named_steps['classifier']
        preprocessor = model.named_steps['preprocessor']
        
        # Transform the single instance
        transformed = preprocessor.transform(df)
        
        # Get feature names from the column transformer
        # This requires some manual extraction based on our specific preprocessor structure
        numeric_features = preprocessor.transformers_[0][2]
        categorical_encoder = preprocessor.transformers_[1][1]
        cat_features = categorical_encoder.get_feature_names_out(['zone_id'])
        
        all_features = list(numeric_features) + list(cat_features)
        
        # Coefficients
        coefs = classifier.coef_[0]
        
        # Calculate contributions (coef * value)
        contributions = []
        for name, value, coef in zip(all_features, transformed[0], coefs):
            # Only report the top contributions that are non-zero, usually numeric is more important
            # If it's a zone feature, just ignore it for explanation simplicity to the user
            if not name.startswith("zone_id_"):
                contrib = float(value * coef)
                contributions.append({
                    "feature": name,
                    "contribution": round(contrib, 4)
                })
        
        # Sort by absolute contribution descending
        contributions.sort(key=lambda x: abs(x["contribution"]), reverse=True)
        return contributions[:3] # Return top 3
    except Exception as e:
        # Fallback if explanation fails
        return [{"feature": "error", "contribution": 0.0}]

def predict_risk(zone_id: str, features: dict, horizon: int = 30) -> dict:
    """
    Main inference function to be imported by Member 2 (FastAPI backend).
    """
    if horizon == 30:
        model = model_30m
    elif horizon == 60:
        model = model_60m
    else:
        raise ValueError("Horizon must be 30 or 60 minutes.")
        
    if model is None:
        raise RuntimeError("Models were not loaded successfully.")

    # Prepare DataFrame matching training schema
    # Features required: ['zone_id', 'crowd_density', 'temperature_c', 'humidity_pct', 'water_availability_pct', 'hour_of_day']
    input_data = {
        'zone_id': zone_id,
        'crowd_density': features.get('crowd_density', 0.0),
        'temperature_c': features.get('temperature_c', 35.0),
        'humidity_pct': features.get('humidity_pct', 0.5),
        'water_availability_pct': features.get('water_availability_pct', 1.0),
        'hour_of_day': features.get('hour_of_day', 12)
    }
    
    df = pd.DataFrame([input_data])
    
    # Predict
    prob = float(model.predict_proba(df)[0, 1])
    
    # Explain
    top_features = _explain_lr(model, df)
    
    return {
        "zone_id": zone_id,
        "risk_probability": round(prob, 4),
        "risk_level": get_risk_level(prob),
        "horizon_minutes": horizon,
        "model_version": metadata.get("model_version", "unknown"),
        "top_features": top_features
    }
