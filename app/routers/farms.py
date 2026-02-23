import secrets
from datetime import datetime, timedelta
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user
from app.models import Farm, Membership, Role, InviteToken
from app.schemas import FarmCreate

router = APIRouter(prefix='/farms', tags=['farms'])


@router.post('')
def create_farm(payload: FarmCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    farm = Farm(name=payload.name, timezone=payload.timezone, currency=payload.currency)
    db.add(farm)
    db.flush()
    owner = db.query(Role).filter_by(name='OWNER').first()
    db.add(Membership(user_id=user.id, farm_id=farm.id, role_id=owner.id, status='ACTIVE'))
    db.commit()
    return farm


@router.get('')
def list_farms(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Farm).join(Membership, Membership.farm_id == Farm.id).filter(Membership.user_id == user.id).all()


@router.post('/{farm_id}/invite')
def invite(farm_id: UUID, role_name: str = 'STAFF', db: Session = Depends(get_db), user=Depends(get_current_user)):
    membership = db.query(Membership).join(Role, Role.id == Membership.role_id).filter(Membership.user_id == user.id, Membership.farm_id == farm_id).first()
    if not membership:
        raise HTTPException(403, 'Not member')
    role = db.query(Role).filter_by(name=role_name).first()
    token = secrets.token_urlsafe(32)
    inv = InviteToken(farm_id=farm_id, role_id=role.id, token=token, expires_at=datetime.utcnow() + timedelta(days=7))
    db.add(inv)
    db.commit()
    return {'invite_token': token}


@router.post('/join')
def join(data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    inv = db.query(InviteToken).filter_by(token=data.get('token')).first()
    if not inv or inv.used_at or inv.expires_at < datetime.utcnow():
        raise HTTPException(400, 'Invalid token')
    db.add(Membership(user_id=user.id, farm_id=inv.farm_id, role_id=inv.role_id, status='ACTIVE'))
    inv.used_at = datetime.utcnow()
    db.commit()
    return {'status': 'joined'}
