from datetime import date, timedelta
from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.models import InventoryItem, InventoryMovement, MovementType, Alert, AlertSeverity


def inventory_status(db: Session, farm_id):
    rows = db.query(
        InventoryItem.id,
        InventoryItem.name,
        InventoryItem.min_level,
        InventoryItem.expires_at,
        func.coalesce(func.sum(case((InventoryMovement.movement_type == MovementType.IN, InventoryMovement.qty), else_=-InventoryMovement.qty)), 0).label('balance'),
    ).outerjoin(InventoryMovement, InventoryMovement.item_id == InventoryItem.id).filter(
        InventoryItem.farm_id == farm_id,
        InventoryItem.deleted_at.is_(None),
    ).group_by(InventoryItem.id).all()
    return rows


def check_inventory_low(db: Session, farm_id):
    created = 0
    for row in inventory_status(db, farm_id):
        if row.balance < row.min_level:
            db.add(Alert(farm_id=farm_id, alert_type='INVENTORY_LOW', title=f'Estoque baixo: {row.name}', message='Saldo abaixo do mínimo', severity=AlertSeverity.HIGH))
            created += 1
    db.commit()
    return created


def check_inventory_expiring(db: Session, farm_id, days: int = 30):
    threshold = date.today() + timedelta(days=days)
    items = db.query(InventoryItem).filter(
        InventoryItem.farm_id == farm_id,
        InventoryItem.expires_at.is_not(None),
        InventoryItem.expires_at <= threshold,
        InventoryItem.deleted_at.is_(None),
    ).all()
    for item in items:
        db.add(Alert(farm_id=farm_id, alert_type='INVENTORY_EXPIRING', title=f'Item vencendo: {item.name}', message=f'Vence em {item.expires_at}', severity=AlertSeverity.MEDIUM))
    db.commit()
    return len(items)
