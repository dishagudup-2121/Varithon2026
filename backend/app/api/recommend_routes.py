from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import json
import uuid
from datetime import datetime

from app.core.database import get_db
from app.services.prediction_service import get_predictions
from app.services.state_service import get_available_resources, get_zone_coords
from app.decision.optimizer import ResourceOptimizer
from app.models.recommendation import Recommendation

router = APIRouter()
optimizer = ResourceOptimizer()

@router.get('/api/recommend')
def recommend(db: Session = Depends(get_db)):
    """Generate optimized resource recommendations using OR-Tools."""
    # Get predictions
    pred_data = get_predictions(db)
    predictions = pred_data['predictions']
    
    # Get available resources as list of dicts
    resources = get_available_resources(db)
    resource_dicts = [{'resource_id': r.resource_id, 'resource_type': r.resource_type, 'zone_id': r.zone_id, 'available': r.available} for r in resources]
    
    # Get zone coordinates
    zone_coords = get_zone_coords(db)
    
    # Run optimization
    assignments = optimizer.optimize(predictions, resource_dicts, zone_coords)
    
    # Find the highest risk zone as primary target
    sorted_preds = sorted(predictions, key=lambda p: p['risk_probability'], reverse=True)
    target_zone = sorted_preds[0]['zone_id'] if sorted_preds else 'Z1'
    
    # Generate recommendation ID
    rec_count = db.query(Recommendation).count()
    rec_id = f'REC-{rec_count + 1:03d}'
    
    # Save recommendation to DB
    rec = Recommendation(
        recommendation_id=rec_id,
        target_zone_id=target_zone,
        assignments=json.dumps(assignments),
        optimization_method='OR-Tools CP-SAT',
        status='pending',
    )
    db.add(rec)
    db.commit()
    
    return {
        'recommendation_id': rec_id,
        'target_zone_id': target_zone,
        'assignments': assignments,
        'optimization_method': 'OR-Tools CP-SAT',
    }
