from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json
from datetime import datetime, timezone

from app.core.database import get_db
from app.schemas.action import ApproveRequest
from app.models.recommendation import Recommendation
from app.models.action_log import ActionLog

router = APIRouter()

@router.post('/api/actions/approve')
def approve_action(request: ApproveRequest, db: Session = Depends(get_db)):
    """Approve, modify, or reject a recommendation."""
    # Find the recommendation
    rec = db.query(Recommendation).filter(
        Recommendation.recommendation_id == request.recommendation_id
    ).first()
    
    if not rec:
        raise HTTPException(status_code=404, detail=f'Recommendation {request.recommendation_id} not found')
    
    if rec.status != 'pending':
        raise HTTPException(status_code=400, detail=f'Recommendation already {rec.status}')
    
    # Validate decision
    if request.decision not in ('approve', 'modify', 'reject'):
        raise HTTPException(status_code=400, detail='Decision must be approve, modify, or reject')
    
    # Update recommendation status
    rec.status = request.decision + 'd' if request.decision != 'reject' else 'rejected'
    # approved, modified, rejected
    if request.decision == 'approve':
        rec.status = 'approved'
    elif request.decision == 'modify':
        rec.status = 'modified'
    elif request.decision == 'reject':
        rec.status = 'rejected'
    
    # Create action log
    log = ActionLog(
        recommendation_id=request.recommendation_id,
        decision=request.decision,
        modified_assignments=json.dumps(request.modified_assignments) if request.modified_assignments else None,
        decided_by='dashboard_user',
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    
    return {
        'status': 'recorded',
        'recommendation_id': request.recommendation_id,
        'decision': request.decision,
        'logged_at': log.decided_at.isoformat() if log.decided_at else datetime.now(timezone.utc).isoformat(),
    }

@router.get('/api/actions/log')
def get_action_log(db: Session = Depends(get_db)):
    """Return recent action history."""
    logs = db.query(ActionLog).order_by(ActionLog.decided_at.desc()).limit(50).all()
    return {
        'actions': [
            {
                'log_id': log.log_id,
                'recommendation_id': log.recommendation_id,
                'decision': log.decision,
                'modified_assignments': json.loads(log.modified_assignments) if log.modified_assignments else [],
                'decided_at': log.decided_at.isoformat() if log.decided_at else None,
                'decided_by': log.decided_by,
            }
            for log in logs
        ]
    }
