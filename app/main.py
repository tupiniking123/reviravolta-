from fastapi import FastAPI

from app.jobs.scheduler import start_scheduler
from app.db import SessionLocal
from app.bootstrap import seed_roles_permissions
from app.routers import (
    auth,
    farms,
    members,
    income,
    expense,
    categories,
    inventory,
    cattle,
    vaccinations,
    schedules,
    alerts,
    reports,
    export_powerbi,
    audit,
)

app = FastAPI(title='FarmOps Multi-Tenant API')

for r in [auth, farms, members, income, expense, categories, inventory, cattle, vaccinations, schedules, alerts, reports, export_powerbi, audit]:
    app.include_router(r.router)


@app.on_event('startup')
def startup_event():
    db = SessionLocal()
    try:
        seed_roles_permissions(db)
    finally:
        db.close()
    start_scheduler()


@app.get('/health')
def health():
    return {'status': 'ok'}
