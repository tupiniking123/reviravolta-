from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import require_permission
from app.models import Schedule
from app.schemas import ScheduleCreate

router = APIRouter(prefix='/schedules', tags=['schedules'])


@router.post('')
def create_schedule(payload: ScheduleCreate, m=Depends(require_permission('schedules', write=True)), db: Session = Depends(get_db)):
    sch = Schedule(farm_id=m.farm_id, **payload.model_dump())
    db.add(sch)
    db.commit()
    return sch


@router.get('')
def list_schedules(m=Depends(require_permission('schedules')), db: Session = Depends(get_db)):
    return db.query(Schedule).filter_by(farm_id=m.farm_id).all()
