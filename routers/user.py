from typing import Annotated
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from database import SessionDep, Token, User
from admin import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/login/", response_model=Token)
async def login_for_access_token(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me/", response_model=User)
def read_user_me(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    return current_user