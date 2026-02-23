from datetime import date, timedelta, datetime
from sqlalchemy.orm import Session

from app.models import Vaccination, Alert, AlertSeverity, Task


def check_vaccines_due(db: Session, farm_id, days: int = 7):
    due_date = date.today() + timedelta(days=days)
    records = db.query(Vaccination).filter(
        Vaccination.farm_id == farm_id,
        Vaccination.next_due_date.is_not(None),
        Vaccination.next_due_date <= due_date,
    ).all()
    for rec in records:
        db.add(Alert(farm_id=farm_id, alert_type='VACCINE_DUE', title='Vacina próxima do reforço', message=f'Vencimento em {rec.next_due_date}', severity=AlertSeverity.MEDIUM))
        db.add(Task(farm_id=farm_id, title='Aplicar reforço vacinal', due_at=datetime.combine(rec.next_due_date, datetime.min.time()), auto_generated=True))
    db.commit()
    return len(records)
