from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import require_permission
from app.models import Expense
from app.schemas import ExpenseCreate

router = APIRouter(prefix='/expense', tags=['expense'])


@router.post('')
def create_expense(payload: ExpenseCreate, m=Depends(require_permission('finance', write=True)), db: Session = Depends(get_db)):
    rec = Expense(farm_id=m.farm_id, **payload.model_dump())
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec


@router.get('')
def list_expense(m=Depends(require_permission('finance')), db: Session = Depends(get_db)):
    return db.query(Expense).filter_by(farm_id=m.farm_id).all()


@router.delete('/{expense_id}')
def delete_expense(expense_id: UUID, m=Depends(require_permission('finance', write=True)), db: Session = Depends(get_db)):
    expense = db.query(Expense).filter_by(id=expense_id, farm_id=m.farm_id).first()
    if not expense:
        raise HTTPException(404, 'Not found')
    expense.deleted_at = datetime.utcnow()
    db.commit()
    return {'status': 'deleted'}
