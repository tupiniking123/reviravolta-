from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import require_permission, get_current_user
from app.models import Alert

router = APIRouter(prefix='/alerts', tags=['alerts'])


@router.get('')
def list_alerts(m=Depends(require_permission('alerts')), db: Session = Depends(get_db)):
    return db.query(Alert).filter_by(farm_id=m.farm_id).all()


@router.post('/{alert_id}/resolve')
def resolve(alert_id: UUID, m=Depends(require_permission('alerts', write=True)), db: Session = Depends(get_db), user=Depends(get_current_user)):
    alert = db.query(Alert).filter_by(id=alert_id, farm_id=m.farm_id).first()
    if not alert:
        raise HTTPException(404, 'Not found')
    alert.status = 'RESOLVED'
    alert.resolved_at = datetime.utcnow()
    alert.resolved_by_user_id = user.id
    db.commit()
    return {'status': 'resolved'}
