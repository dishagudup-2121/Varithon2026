from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.prediction_service import get_predictions

router = APIRouter()

@router.get('/api/predict')
def predict(db: Session = Depends(get_db)):
    """Return current model risk predictions for all zones."""
    return get_predictions(db)
