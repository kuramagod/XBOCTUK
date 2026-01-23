from typing import Annotated
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from database import SessionDep, User
from admin import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/login/")
async def login_for_access_token(
    response: Response,
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
    )

    return {"status": "ok"}


@router.get("/me/", response_model=User)
def read_user_me(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    return current_user