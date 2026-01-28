import jwt

from sqlmodel import select
from datetime import timedelta
from database import User, engine, get_session
from fastapi import Request
from sqladmin.authentication import AuthenticationBackend
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from core.security import authenticate_user, create_access_token


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
    

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload["sub"]
        except Exception:
            return False

        session = next(get_session())
        return bool(
            session.exec(
                select(User).where(User.username == username, User.is_admin == True)
            ).first()
        )
