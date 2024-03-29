from datetime import timedelta
from typing import Annotated

import schemas.auth
import schemas.response
import schemas.user
from database import get_db
from exceptions import CouldNotValidateCredentialsException, InactiveUserException, IncorrectUsernameOrPasswordException
from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from settings import settings
from sqlalchemy.orm import Session
from utils.auth import (
    add_jwt_token_cookie,
    authenticate_user,
    create_jwt_token,
    get_current_active_user,
    get_data_from_jwt_token,
    get_user_permissions,
    oauth2_scheme,
)
from utils.response import generate_responses_for_doc


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


# TODO zastanowić się nad nazwami endpointów
# TODO recaptcha


@router.post(
    "/token",
    response_model=schemas.auth.Token,
    responses=generate_responses_for_doc(["IncorrectUsernameOrPasswordException", "InactiveUserException"]),
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response, db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise IncorrectUsernameOrPasswordException()
    if not user.is_active:
        raise InactiveUserException()

    user_id = user.id
    user_permissions = get_user_permissions(db, user_id)
    payload = {"uid": user_id, "scopes": user_permissions}

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    access_token = create_jwt_token(
        data=payload,
        expires_delta=access_token_expires,
        secret_key=settings.ACCESS_TOKEN_SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    refresh_token = create_jwt_token(
        data=payload,
        expires_delta=refresh_token_expires,
        secret_key=settings.REFRESH_TOKEN_SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    add_jwt_token_cookie(response, "access_token", access_token, settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    add_jwt_token_cookie(response, "refresh_token", refresh_token, settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60)

    return schemas.auth.Token(access_token=access_token)


@router.post(
    "/refresh",
    response_model=schemas.auth.Token,
    responses=generate_responses_for_doc(["CouldNotValidateCredentialsException"]),
)
async def login_for_refresh_token(request: Request, response: Response, token: str = Depends(oauth2_scheme)):
    refresh_token_from_cookie = request.cookies.get("refresh_token")
    if token != refresh_token_from_cookie:
        raise CouldNotValidateCredentialsException()

    token_data = get_data_from_jwt_token(token, settings.REFRESH_TOKEN_SECRET_KEY, settings.ALGORITHM)
    user_id = token_data.uid
    user_permissions = token_data.scopes
    payload = {"uid": user_id, "scopes": user_permissions}

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    new_access_token = create_jwt_token(
        data=payload,
        expires_delta=access_token_expires,
        secret_key=settings.ACCESS_TOKEN_SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    new_refresh_token = create_jwt_token(
        data=payload,
        expires_delta=refresh_token_expires,
        secret_key=settings.REFRESH_TOKEN_SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    add_jwt_token_cookie(response, "access_token", new_access_token, settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    add_jwt_token_cookie(response, "refresh_token", new_refresh_token, settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60)

    return schemas.auth.Token(access_token=new_access_token)


@router.post("/logout", response_model=schemas.response.MessageRes)
async def logout(response: Response, current_user: Annotated[schemas.user.User, Depends(get_current_active_user)]):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"detail": "logged out"}
