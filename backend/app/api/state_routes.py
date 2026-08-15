from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.state_service import get_current_state

router = APIRouter()

@router.get('/api/state')
def get_state(db: Session = Depends(get_db)):
    """Return the current Digital Twin state with zones, agents, and resources."""
    return get_current_state(db)
