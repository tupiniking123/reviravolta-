from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import require_permission
from app.models import Income, Expense
from app.services.finance_service import get_summary

router = APIRouter(prefix='/reports', tags=['reports'])


@router.get('/summary')
def summary(start: date, end: date, m=Depends(require_permission('reports')), db: Session = Depends(get_db)):
    return get_summary(db, m.farm_id, start, end)


@router.get('/cashflow')
def cashflow(start: date, end: date, m=Depends(require_permission('reports')), db: Session = Depends(get_db)):
    income = db.query(Income.date, func.sum(Income.amount).label('income')).filter(Income.farm_id == m.farm_id, Income.date >= start, Income.date <= end).group_by(Income.date).all()
    expense = db.query(Expense.date, func.sum(Expense.amount).label('expense')).filter(Expense.farm_id == m.farm_id, Expense.date >= start, Expense.date <= end).group_by(Expense.date).all()
    return {'income': income, 'expense': expense}
