from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_active_farm_membership, require_permission
from app.models import ExpenseCategory

router = APIRouter(prefix='/categories', tags=['categories'])


@router.get('')
def list_categories(m=Depends(require_permission('finance')), db: Session = Depends(get_db)):
    return db.query(ExpenseCategory).filter((ExpenseCategory.farm_id == m.farm_id) | (ExpenseCategory.farm_id.is_(None))).all()
