from datetime import date
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import Expense, Alert, AlertSeverity


def detect_spending_anomalies(db: Session, farm_id, window_months: int = 3, multiplier: float = 1.5):
    current = date.today().replace(day=1)
    created = 0
    cats = db.query(Expense.category_id).filter(Expense.farm_id == farm_id, Expense.deleted_at.is_(None)).distinct().all()
    for (category_id,) in cats:
        current_total = db.query(func.coalesce(func.sum(Expense.amount), 0)).filter(
            Expense.farm_id == farm_id,
            Expense.category_id == category_id,
            func.date_trunc('month', Expense.date) == current,
        ).scalar()
        hist_avg = db.query(func.coalesce(func.avg(func.sum(Expense.amount)).over(), 0)).filter(
            Expense.farm_id == farm_id,
            Expense.category_id == category_id,
            Expense.date < current,
        ).scalar() or 0
        if hist_avg and current_total > (multiplier * hist_avg):
            db.add(Alert(farm_id=farm_id, alert_type='SPENDING_ANOMALY', title='Anomalia de gastos', message='Gasto acima da média histórica', severity=AlertSeverity.HIGH))
            created += 1
    db.commit()
    return created
