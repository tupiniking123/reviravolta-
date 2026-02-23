from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import require_permission
from app.models import Income
from app.schemas import IncomeCreate

router = APIRouter(prefix='/income', tags=['income'])


@router.post('')
def create_income(payload: IncomeCreate, m=Depends(require_permission('finance', write=True)), db: Session = Depends(get_db)):
    rec = Income(farm_id=m.farm_id, **payload.model_dump())
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec


@router.get('')
def list_income(m=Depends(require_permission('finance')), db: Session = Depends(get_db)):
    return db.query(Income).filter_by(farm_id=m.farm_id).all()
