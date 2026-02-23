from datetime import datetime
from dateutil.rrule import rrulestr
from sqlalchemy.orm import Session

from app.models import Schedule, Expense, ExpenseCategory


def run_due_schedules(db: Session, farm_id):
    now = datetime.utcnow()
    schedules = db.query(Schedule).filter(Schedule.farm_id == farm_id, Schedule.is_active.is_(True), Schedule.next_run_at <= now).all()
    for s in schedules:
        if s.schedule_type.value == 'PAYROLL':
            payload = s.payload_json or {}
            cat = db.query(ExpenseCategory).filter(ExpenseCategory.farm_id == farm_id, ExpenseCategory.name == 'Salário do caseiro').first()
            if not cat:
                cat = db.query(ExpenseCategory).filter(ExpenseCategory.farm_id.is_(None), ExpenseCategory.name == 'Salário do caseiro').first()
            db.add(Expense(farm_id=farm_id, date=now.date(), category_id=cat.id, description=payload.get('description', s.name), amount=payload.get('amount', 0), vendor=payload.get('vendor')))
        next_occ = rrulestr(s.rrule, dtstart=s.next_run_at).after(now)
        s.next_run_at = next_occ
    db.commit()
    return len(schedules)
