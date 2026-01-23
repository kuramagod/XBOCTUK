import jwt
import os

from typing import Annotated
from dotenv import load_dotenv
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from fastapi import Depends, HTTPException, status, Request
from sqlmodel import select, Session
from database import SessionDep, User, engine


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


# Создание админа
def create_super_user():
    with Session(engine) as session:
        if session.exec(select(User).where(User.is_admin == True)).first():
            return None
    
    username = os.getenv("ADMIN_USERNAME")
    password = os.getenv("ADMIN_PASSWORD")
    
    admin = User(
        username=username, 
        hashed_password=get_password_hash(password), 
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


async def get_current_user(
        request: Request,
        session: SessionDep,
):
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


def admin_required(
    user: Annotated[User, Depends(get_current_user)]
):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")
    return user

AdminDep = Annotated[User, Depends(admin_required)]