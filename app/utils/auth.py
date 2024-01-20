from datetime import datetime, timedelta
from typing import Annotated

import models.user
import schemas.auth
import schemas.user
import sqlalchemy
from database import get_db
from fastapi import Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
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
    # TODO zabezpieczyłem za pomocą try/catch, nie wiem czy jest idealnie, ale chyba wystarczająco dobrze i spełnia cel
    try:
        user = db.query(models.user.User).filter(models.user.User.email == email).first()
    except sqlalchemy.exc.NoResultFound:
        user = None
    return user


def authenticate_user(db, email: str, password: str):
    user = get_user(db, email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.ACCESS_TOKEN_SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.auth.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user(db, token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Annotated[schemas.user.User, Depends(get_current_user)]):
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return current_user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.ACCESS_TOKEN_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.REFRESH_TOKEN_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def authorize(request: Request, response: Response, token: str = Depends(oauth2_scheme)):
    # TODO Amadeusz weź to przepisz
    # print(token)
    error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid token",
    )
    try:
        data = jwt.decode(token, settings.REFRESH_TOKEN_SECRET_KEY, settings.ALGORITHM)
        # print(data)
        if "sub" not in data:
            raise error

        user = data["sub"]
        # print(user)

        refresh_token_from_cookie = request.cookies.get("refresh_token")
        # print(refresh_token_from_cookie)
        if token != refresh_token_from_cookie:
            raise error
        data = {"sub": user}

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        new_access_token = create_access_token(data=data, expires_delta=access_token_expires)
        new_refresh_token = create_refresh_token(data=data, expires_delta=refresh_token_expires)

        response.set_cookie(
            "access_token",
            new_access_token,
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
            new_refresh_token,
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
        # return {"access_token": new_access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}
        return {"access_token": new_access_token, "token_type": "bearer"}
    except JWTError:
        raise error
