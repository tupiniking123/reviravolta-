from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import require_permission
from app.models import InventoryItem, InventoryMovement
from app.schemas import InventoryItemCreate, InventoryMovementCreate
from app.services.inventory_service import inventory_status

router = APIRouter(prefix='/inventory', tags=['inventory'])


@router.post('/items')
def create_item(payload: InventoryItemCreate, m=Depends(require_permission('inventory', write=True)), db: Session = Depends(get_db)):
    item = InventoryItem(farm_id=m.farm_id, **payload.model_dump())
    db.add(item)
    db.commit()
    return item


@router.get('/items')
def list_items(m=Depends(require_permission('inventory')), db: Session = Depends(get_db)):
    return db.query(InventoryItem).filter_by(farm_id=m.farm_id).all()


@router.post('/movements')
def create_movement(payload: InventoryMovementCreate, m=Depends(require_permission('inventory', write=True)), db: Session = Depends(get_db)):
    mov = InventoryMovement(farm_id=m.farm_id, **payload.model_dump())
    db.add(mov)
    db.commit()
    return mov


@router.get('/status')
def status(m=Depends(require_permission('inventory')), db: Session = Depends(get_db)):
    return inventory_status(db, m.farm_id)
