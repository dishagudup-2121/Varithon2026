from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.explain_service import get_explanation

router = APIRouter()

@router.get('/api/explain')
def explain(language: str = Query(default='en', pattern='^(en|mr)$'), db: Session = Depends(get_db)):
    """Return a structured explanation of the current risk situation."""
    return get_explanation(db, language=language)
