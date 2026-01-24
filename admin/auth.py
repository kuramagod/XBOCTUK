import jwt

from sqlmodel import select
from typing import Annotated
from datetime import timedelta
from database import User, engine, get_session
from fastapi import Depends, HTTPException, Request
from sqladmin.authentication import AuthenticationBackend
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from core.security import get_current_user, authenticate_user, create_access_token


def admin_required(
    user: Annotated[User, Depends(get_current_user)]
):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")
    return user


AdminDep = Annotated[User, Depends(admin_required)]


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
        
        if username and password:
            session = next(get_session())
            
            user = authenticate_user(session, username, password)
            if user and user.is_admin:
                access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = create_access_token(
                    data={"sub": user.username},
                    expires_delta=access_token_expires
                )
                
                request.session.update({"token": access_token})
                return True
        
        return False
    

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True
    

    async def authenticate(self, request: Request) -> None | bool:
        token = request.session.get("token")
        
        if not token:
            return False
            
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            
            session = next(get_session())
            
            user = session.exec(select(User).where(User.username == username)).first()
            if user and user.is_admin:
                return True
        except Exception:
            return False
            
        return False