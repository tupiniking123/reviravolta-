from typing import Annotated
from uuid import UUID

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import User, Membership, Role, Permission
from app.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)) -> User:
    payload = decode_token(token)
    user = db.get(User, payload.get('sub'))
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    return user


def get_active_farm_membership(
    x_farm_id: Annotated[str, Header(alias='X-Farm-Id')],
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Membership:
    try:
        farm_id = UUID(x_farm_id)
    except Exception:
        raise HTTPException(status_code=400, detail='Invalid X-Farm-Id')
    membership = db.query(Membership).filter_by(user_id=user.id, farm_id=farm_id, status='ACTIVE').first()
    if not membership:
        raise HTTPException(status_code=403, detail='No membership for farm')
    return membership


def require_permission(module: str, write: bool = False):
    def _checker(membership: Membership = Depends(get_active_farm_membership), db: Session = Depends(get_db)) -> Membership:
        role = db.get(Role, membership.role_id)
        perm = db.query(Permission).filter_by(role_id=role.id, module=module).first()
        allowed = perm.can_write if write else perm.can_read
        if not allowed:
            raise HTTPException(status_code=403, detail='Permission denied')
        return membership

    return _checker
