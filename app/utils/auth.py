from datetime import datetime, timedelta
from typing import Annotated

import models.user
import schemas.auth
import schemas.user
from database import get_db
from exceptions import CouldNotValidateCredentialsException, InactiveUserException, UnauthorizedException
from fastapi import Depends, Response
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from settings import settings
from sqlalchemy.orm import Session
from utils.commons import get_current_time


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def get_user_by_id(db: Session, user_id: int):
    user = db.query(models.user.User).filter(models.user.User.id == user_id).first()
    return user


def get_user_by_email(db: Session, email: str):
    user = db.query(models.user.User).filter(models.user.User.email == email).first()
    return user


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def get_user_permissions(db: Session, user_id: int):
    permission_data = db.query(models.user.UserPermission).filter(models.user.UserPermission.user_id == user_id).all()
    user_permissions = []
    for permission in permission_data:
        user_permissions.append(permission.name)
    user_permissions.sort()
    return user_permissions


def get_data_from_jwt_token(token: str, secret_key: str, algorithm: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        user_id = payload.get("uid")
        if user_id is None:
            raise CouldNotValidateCredentialsException()
        token_scopes = payload.get("scopes")
        user_data = schemas.auth.TokenData(uid=user_id, scopes=token_scopes)
    except ExpiredSignatureError:
        raise UnauthorizedException("Token has expired.")
    except JWTError:
        raise CouldNotValidateCredentialsException()
    return user_data


async def get_current_user(
    security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    token_data = get_data_from_jwt_token(token, settings.ACCESS_TOKEN_SECRET_KEY, settings.ALGORITHM)
    user = get_user_by_id(db, token_data.uid)
    if user is None:
        raise CouldNotValidateCredentialsException()
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise UnauthorizedException(
                detail="Not enough permissions", headers={"WWW-Authenticate": authenticate_value}
            )
    return user


async def get_current_active_user(current_user: Annotated[schemas.user.User, Depends(get_current_user)]):
    if not current_user.is_active:
        raise InactiveUserException()
    return current_user


def create_jwt_token(data: dict, expires_delta: timedelta, secret_key: str, algorithm: str):
    to_encode = data.copy()
    issued_at = get_current_time()
    expiration_time = issued_at + expires_delta
    to_encode.update({"iat": issued_at, "exp": expiration_time})  # TODO przetestować, że te pola znajdują się w tokenie
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def add_jwt_token_cookie(response: Response, name: str, value: str, expires: datetime | str | int):
    response.set_cookie(
        key=name,
        value=value,
        max_age=expires,
        expires=expires,
        path="/",
        domain=None,
        secure=False,  # TODO przestawić na True dla komunikacji https (na środowisku)
        httponly=True,
        samesite="lax",
    )
