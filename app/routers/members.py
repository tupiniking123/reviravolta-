from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user
from app.models import Membership, Role

router = APIRouter(prefix='/farms', tags=['members'])


def _is_admin(db, user_id, farm_id):
    m = db.query(Membership).join(Role, Role.id == Membership.role_id).filter(Membership.user_id == user_id, Membership.farm_id == farm_id).first()
    return bool(m and m.role_id)


@router.get('/{farm_id}/members')
def list_members(farm_id: UUID, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not _is_admin(db, user.id, farm_id):
        raise HTTPException(403, 'Denied')
    return db.query(Membership).filter_by(farm_id=farm_id).all()


@router.patch('/{farm_id}/members/{user_id}/role')
def update_role(farm_id: UUID, user_id: UUID, data: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not _is_admin(db, user.id, farm_id):
        raise HTTPException(403, 'Denied')
    role = db.query(Role).filter_by(name=data.get('role')).first()
    m = db.query(Membership).filter_by(user_id=user_id, farm_id=farm_id).first()
    m.role_id = role.id
    db.commit()
    return {'status': 'updated'}


@router.delete('/{farm_id}/members/{user_id}')
def remove_member(farm_id: UUID, user_id: UUID, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not _is_admin(db, user.id, farm_id):
        raise HTTPException(403, 'Denied')
    db.query(Membership).filter_by(user_id=user_id, farm_id=farm_id).delete()
    db.commit()
    return {'status': 'removed'}
