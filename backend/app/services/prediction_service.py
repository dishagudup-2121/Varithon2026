from app.ml.predictor import RiskPredictor
from app.services.state_service import get_zones

predictor = RiskPredictor()

def get_predictions(db) -> dict:
    """Get risk predictions for all zones."""
    zones = get_zones(db)
    predictions = []
    for zone in zones:
        zone_data = {
            'zone_id': zone.zone_id,
            'crowd_count': zone.crowd_count,
            'temperature_c': zone.temperature_c,
            'humidity_percent': zone.humidity_percent,
            'water_availability_percent': zone.water_availability_percent,
        }
        pred = predictor.predict(zone_data)
        predictions.append(pred)
    
    return {
        'predictions': predictions,
        'model_version': predictor.MODEL_VERSION,
    }
