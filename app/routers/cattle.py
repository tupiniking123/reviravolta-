from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import require_permission
from app.models import Cattle
from app.schemas import CattleCreate

router = APIRouter(prefix='/cattle', tags=['cattle'])


@router.post('')
def create_cattle(payload: CattleCreate, m=Depends(require_permission('cattle', write=True)), db: Session = Depends(get_db)):
    rec = Cattle(farm_id=m.farm_id, **payload.model_dump())
    db.add(rec)
    db.commit()
    return rec


@router.get('')
def list_cattle(m=Depends(require_permission('cattle')), db: Session = Depends(get_db)):
    return db.query(Cattle).filter_by(farm_id=m.farm_id).all()
