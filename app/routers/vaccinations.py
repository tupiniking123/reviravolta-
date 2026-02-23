from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import require_permission
from app.models import Vaccination
from app.schemas import VaccinationCreate

router = APIRouter(prefix='/vaccinations', tags=['vaccinations'])


@router.post('')
def create_vacc(payload: VaccinationCreate, m=Depends(require_permission('vaccinations', write=True)), db: Session = Depends(get_db)):
    rec = Vaccination(farm_id=m.farm_id, **payload.model_dump())
    db.add(rec)
    db.commit()
    return rec


@router.get('')
def list_vacc(m=Depends(require_permission('vaccinations')), db: Session = Depends(get_db)):
    return db.query(Vaccination).filter_by(farm_id=m.farm_id).all()
