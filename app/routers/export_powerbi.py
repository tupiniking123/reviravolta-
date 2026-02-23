from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import require_permission
from app.services.powerbi_service import query_to_csv

router = APIRouter(prefix='/export/powerbi', tags=['export'])


def _csv(sql, db):
    data = query_to_csv(db, sql)
    return Response(content=data, media_type='text/csv')


@router.get('/financial_monthly.csv')
def financial_monthly(m=Depends(require_permission('export')), db: Session = Depends(get_db)):
    return _csv(f"SELECT * FROM vw_financial_monthly WHERE farm_id = '{m.farm_id}'", db)


@router.get('/expenses_by_category.csv')
def expenses_by_category(m=Depends(require_permission('export')), db: Session = Depends(get_db)):
    return _csv(f"SELECT * FROM vw_expenses_by_category WHERE farm_id = '{m.farm_id}'", db)


@router.get('/cashflow_daily.csv')
def cashflow_daily(m=Depends(require_permission('export')), db: Session = Depends(get_db)):
    return _csv(f"SELECT * FROM vw_cashflow_daily WHERE farm_id = '{m.farm_id}'", db)


@router.get('/inventory_status.csv')
def inventory_status(m=Depends(require_permission('export')), db: Session = Depends(get_db)):
    return _csv(f"SELECT * FROM vw_inventory_status WHERE farm_id = '{m.farm_id}'", db)


@router.get('/vaccinations_due.csv')
def vaccinations_due(m=Depends(require_permission('export')), db: Session = Depends(get_db)):
    return _csv(f"SELECT * FROM vw_vaccinations_due WHERE farm_id = '{m.farm_id}'", db)
