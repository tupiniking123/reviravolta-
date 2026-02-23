from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import require_permission
from app.models import AuditLog

router = APIRouter(prefix='/audit', tags=['audit'])


@router.get('')
def list_audit(m=Depends(require_permission('audit')), db: Session = Depends(get_db)):
    return db.query(AuditLog).filter_by(farm_id=m.farm_id).all()
