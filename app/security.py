from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
ALGORITHM = 'HS256'


MODULES = ['finance', 'inventory', 'cattle', 'vaccinations', 'schedules', 'reports', 'export', 'alerts', 'users', 'audit']
ROLE_MATRIX = {
    'OWNER': {m: (True, True) for m in MODULES},
    'ADMIN': {m: (True, True) for m in MODULES},
    'MANAGER': {
        'finance': (True, True),
        'inventory': (True, True),
        'cattle': (True, True),
        'vaccinations': (True, True),
        'schedules': (True, True),
        'reports': (True, True),
        'export': (True, True),
        'alerts': (True, True),
        'users': (False, False),
        'audit': (False, False),
    },
    'STAFF': {
        'finance': (True, True),
        'inventory': (True, True),
        'cattle': (True, True),
        'vaccinations': (True, True),
        'schedules': (False, False),
        'reports': (True, False),
        'export': (False, False),
        'alerts': (True, False),
        'users': (False, False),
        'audit': (False, False),
    },
    'VIEWER': {
        'finance': (True, False),
        'inventory': (True, False),
        'cattle': (True, False),
        'vaccinations': (True, False),
        'schedules': (False, False),
        'reports': (True, False),
        'export': (True, False),
        'alerts': (True, False),
        'users': (False, False),
        'audit': (False, False),
    },
}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_token(data: dict[str, Any], expires_delta: timedelta, refresh: bool = False) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({'exp': expire, 'type': 'refresh' if refresh else 'access'})
    secret = settings.JWT_REFRESH_SECRET_KEY if refresh else settings.JWT_SECRET_KEY
    return jwt.encode(to_encode, secret, algorithm=ALGORITHM)


def decode_token(token: str, refresh: bool = False) -> dict[str, Any]:
    secret = settings.JWT_REFRESH_SECRET_KEY if refresh else settings.JWT_SECRET_KEY
    try:
        payload = jwt.decode(token, secret, algorithms=[ALGORITHM])
        return payload
    except JWTError as exc:
        raise ValueError('Invalid token') from exc
