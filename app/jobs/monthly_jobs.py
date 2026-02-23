from datetime import date
from sqlalchemy.orm import Session

from app.models import Farm, SnapshotMonthly
from app.services.finance_service import get_summary


def generate_monthly_snapshot(db: Session):
    month_start = date.today().replace(day=1)
    farms = db.query(Farm).all()
    for farm in farms:
        summary = get_summary(db, farm.id, month_start, date.today())
        row = db.query(SnapshotMonthly).filter_by(farm_id=farm.id, month=month_start).first()
        if not row:
            row = SnapshotMonthly(farm_id=farm.id, month=month_start)
            db.add(row)
        row.total_income = summary['total_income']
        row.total_expense = summary['total_expense']
        row.direct_expense = summary['direct_expense']
        row.gross_profit = summary['gross_profit']
        row.net_profit = summary['net_profit']
    db.commit()


def reconcile_profit_month(db: Session):
    return generate_monthly_snapshot(db)
