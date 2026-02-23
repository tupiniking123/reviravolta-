from fastapi import Request
from sqlalchemy.orm import Session

from app.models import AuditLog


def log_action(db: Session, farm_id, user_id, action: str, entity: str, entity_id: str, payload: dict | None, request: Request | None = None):
    ip = request.client.host if request and request.client else None
    ua = request.headers.get('user-agent') if request else None
    db.add(AuditLog(farm_id=farm_id, user_id=user_id, action=action, entity=entity, entity_id=entity_id, payload_json=payload, ip=ip, user_agent=ua))
    db.commit()
