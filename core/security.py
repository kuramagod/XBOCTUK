import jwt

from sqlmodel import select
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status, Request
from database import SessionDep, User, get_session
from core.config import SECRET_KEY, ALGORITHM, ADMIN_USERNAME, ADMIN_PASSWORD


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


# Создание админа
def create_super_user():
    session = next(get_session())

    if session.exec(select(User).where(User.is_admin == True)).first():
        return None

    admin = User(
        username=ADMIN_USERNAME, 
        hashed_password=get_password_hash(ADMIN_PASSWORD), 
        is_admin=True
    )
    
    session.add(admin)
    session.commit()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(session: SessionDep, username: str, password: str):
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(request: Request, session: SessionDep,):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    return user