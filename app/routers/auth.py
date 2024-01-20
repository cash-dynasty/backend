from datetime import timedelta
from typing import Annotated

import schemas.auth
from database import get_db
from exceptions import CouldNotValidateCredentialsException, InactiveUserException, IncorrectUsernameOrPasswordException
from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from settings import settings
from sqlalchemy.orm import Session
from utils.auth import add_jwt_token_cookie, authenticate_user, create_jwt_token, get_data_from_jwt_token, oauth2_scheme


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


# TODO zastanowić się nad nazwami endpointów
# TODO recaptcha


@router.post("/token", response_model=schemas.auth.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response, db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise IncorrectUsernameOrPasswordException
    if not user.is_active:
        raise InactiveUserException

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    access_token = create_jwt_token(
        data={"sub": user.email},
        expires_delta=access_token_expires,
        secret_key=settings.ACCESS_TOKEN_SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    refresh_token = create_jwt_token(
        data={"sub": user.email},
        expires_delta=refresh_token_expires,
        secret_key=settings.REFRESH_TOKEN_SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    add_jwt_token_cookie(response, "access_token", access_token, settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    add_jwt_token_cookie(response, "refresh_token", refresh_token, settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60)

    # TODO do usunięcia?
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


@router.post("/refresh", response_model=schemas.auth.Token)
async def login_for_refresh_token(request: Request, response: Response, token: str = Depends(oauth2_scheme)):
    refresh_token_from_cookie = request.cookies.get("refresh_token")
    if token != refresh_token_from_cookie:
        raise CouldNotValidateCredentialsException

    token_data = get_data_from_jwt_token(token, settings.REFRESH_TOKEN_SECRET_KEY, settings.ALGORITHM)
    email = token_data.email
    data = {"sub": email}

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    new_access_token = create_jwt_token(
        data=data,
        expires_delta=access_token_expires,
        secret_key=settings.ACCESS_TOKEN_SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    new_refresh_token = create_jwt_token(
        data=data,
        expires_delta=refresh_token_expires,
        secret_key=settings.REFRESH_TOKEN_SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    add_jwt_token_cookie(response, "access_token", new_access_token, settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    add_jwt_token_cookie(response, "refresh_token", new_refresh_token, settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60)

    # TODO do usunięcia?
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
    return {"access_token": new_access_token, "token_type": "bearer"}
