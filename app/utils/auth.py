from datetime import datetime, timedelta
from typing import Annotated

import models.user
import schemas.auth
import schemas.user
from database import get_db
from exceptions import CouldNotValidateCredentialsException, InactiveUserException, UnauthorizedException
from fastapi import Depends, Response
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from settings import settings
from sqlalchemy.orm import Session


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def get_user(db: Session, email: str):
    user = db.query(models.user.User).filter(models.user.User.email == email).first()
    return user


def authenticate_user(db: Session, email: str, password: str):
    user = get_user(db, email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def get_data_from_jwt_token(token: str, secret_key: str, algorithm: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        email = payload.get("sub")
        if email is None:
            raise CouldNotValidateCredentialsException
        user_data = schemas.auth.TokenData(email=email)
    except ExpiredSignatureError:
        raise UnauthorizedException("Token has expired.")
    except JWTError:
        raise CouldNotValidateCredentialsException
    return user_data


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    token_data = get_data_from_jwt_token(token, settings.ACCESS_TOKEN_SECRET_KEY, settings.ALGORITHM)
    user = get_user(db, token_data.email)
    if user is None:
        raise CouldNotValidateCredentialsException
    return user


async def get_current_active_user(current_user: Annotated[schemas.user.User, Depends(get_current_user)]):
    if not current_user.is_active:
        raise InactiveUserException
    return current_user


def create_jwt_token(data: dict, expires_delta: timedelta, secret_key: str, algorithm: str):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def add_jwt_token_cookie(response: Response, name: str, value: str, expires: datetime | str | int):
    response.set_cookie(
        name,
        value,
        expires,
        expires,
        "/",
        None,
        False,  # TODO przestawić na True?
        True,
        "lax",
    )
