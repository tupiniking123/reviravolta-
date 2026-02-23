from sqlalchemy.orm import Session

from app.models import Farm
from app.services.inventory_service import check_inventory_low, check_inventory_expiring
from app.services.vaccination_service import check_vaccines_due
from app.services.anomaly_service import detect_spending_anomalies
from app.services.schedules_service import run_due_schedules


def run_daily(db: Session):
    farms = db.query(Farm).all()
    for farm in farms:
        check_inventory_low(db, farm.id)
        check_inventory_expiring(db, farm.id, days=30)
        check_vaccines_due(db, farm.id, days=7)
        detect_spending_anomalies(db, farm.id, window_months=3, multiplier=1.5)
        run_due_schedules(db, farm.id)
