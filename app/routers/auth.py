from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import settings
from app.db import get_db
from app.deps import get_current_user
from app.models import User
from app.schemas import UserCreate, LoginInput, Token, UserOut
from app.security import create_token, get_password_hash, verify_password, decode_token

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/register', response_model=UserOut)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter_by(email=payload.email).first():
        raise HTTPException(400, 'Email already exists')
    user = User(name=payload.name, email=payload.email, password_hash=get_password_hash(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post('/login', response_model=Token)
def login(payload: LoginInput, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(401, 'Invalid credentials')
    access = create_token({'sub': str(user.id)}, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh = create_token({'sub': str(user.id)}, timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS), refresh=True)
    return Token(access_token=access, refresh_token=refresh)


@router.post('/refresh', response_model=Token)
def refresh(data: dict, db: Session = Depends(get_db)):
    payload = decode_token(data.get('refresh_token', ''), refresh=True)
    user = db.get(User, payload.get('sub'))
    if not user:
        raise HTTPException(401, 'Invalid token')
    access = create_token({'sub': str(user.id)}, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_t = create_token({'sub': str(user.id)}, timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS), refresh=True)
    return Token(access_token=access, refresh_token=refresh_t)


@router.get('/me', response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user
