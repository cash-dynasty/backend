from datetime import timedelta
from typing import Annotated

import schemas.auth
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from settings import settings
from sqlalchemy.orm import Session
from utils.auth import authenticate_user, authorize, create_access_token, create_refresh_token


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


# TODO zastanowić się nad nazwami endpointów

# TODO nie logować użytkownika (nie zwracać tokenu), jeśli nie jest aktywny


# 1. poprawne logowanie
# 2. niepoprawny email
# 3. email nie istnieje w bazie
# 4. niepoprawne hasło
@router.post("/token", response_model=schemas.auth.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response, db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(data={"sub": user.email}, expires_delta=refresh_token_expires)

    response.set_cookie(
        "access_token",
        access_token,
        settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "/",
        None,
        False,
        True,
        "lax",
    )
    response.set_cookie(
        "refresh_token",
        refresh_token,
        settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        "/",
        None,
        False,
        True,
        "lax",
    )
    response.set_cookie(
        "logged_in",
        "True",
        settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "/",
        None,
        False,
        False,
        "lax",
    )
    return {"access_token": access_token, "token_type": "bearer"}


# 1. poprawny refresh
# 2. błędny/nieważny refresh token
# 3. (?) nie ma tokena w ciastku
@router.post("/refresh")
async def login_for_refresh_token(token_data: dict = Depends(authorize)):
    return token_data
