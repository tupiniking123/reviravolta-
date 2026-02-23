from apscheduler.schedulers.background import BackgroundScheduler

from app.db import SessionLocal
from app.jobs.daily_jobs import run_daily
from app.jobs.monthly_jobs import generate_monthly_snapshot, reconcile_profit_month

scheduler = BackgroundScheduler()


def _daily_runner():
    db = SessionLocal()
    try:
        run_daily(db)
    finally:
        db.close()


def _monthly_runner():
    db = SessionLocal()
    try:
        generate_monthly_snapshot(db)
        reconcile_profit_month(db)
    finally:
        db.close()


def start_scheduler():
    scheduler.add_job(_daily_runner, 'cron', hour=3, minute=0, id='daily-jobs', replace_existing=True)
    scheduler.add_job(_monthly_runner, 'cron', day=1, hour=4, minute=0, id='monthly-jobs', replace_existing=True)
    scheduler.start()
