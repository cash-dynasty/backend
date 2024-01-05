from datetime import datetime, timedelta
from typing import Annotated

import sqlalchemy
from fastapi import Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

import models
from database import get_db
from schemas import TokenData, User
from utils import verify_password

ACCESS_TOKEN_SECRET_KEY = "53d6391adbae0f4b765b3e77f18e10d1aa4807f1fad967ee8cdb1e0f3d39bb7f"
REFRESH_TOKEN_SECRET_KEY = "aedbe9f6f80538dbf0c18cfe4ae8e2f2e089620558cf048e3d6f8d30732b88a8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
REFRESH_TOKEN_EXPIRE_MINUTES = 5

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_user(db: Session, email: str):
    # TODO zabezpieczyłem za pomocą try/catch, nie wiem czy jest idealnie, ale chyba wystarczająco dobrze i spełnia cel
    try:
        user = db.query(models.User).filter(models.User.email == email).one()
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
        payload = jwt.decode(token, ACCESS_TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user(db, token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, ACCESS_TOKEN_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, REFRESH_TOKEN_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def authorize(request: Request, response: Response, token: str = Depends(oauth2_scheme)):
    #TODO Amadeusz weź to przepisz
    print(token)
    error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid token')
    try:
        data = jwt.decode(token, REFRESH_TOKEN_SECRET_KEY, ALGORITHM)
        print(data)
        if 'sub' not in data:
            raise error

        user = data['sub']
        print(user)

        refresh_token_from_cookie = request.cookies.get('refresh_token')
        print(refresh_token_from_cookie)
        if token != refresh_token_from_cookie:
            raise error
        data = {'sub': user}

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        new_access_token = create_access_token(data=data, expires_delta=access_token_expires)
        new_refresh_token = create_refresh_token(data=data, expires_delta=refresh_token_expires)

        response.set_cookie('access_token', new_access_token, ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                            ACCESS_TOKEN_EXPIRE_MINUTES * 60, '/', None, False, True, 'lax')
        response.set_cookie('refresh_token', new_refresh_token,
                            REFRESH_TOKEN_EXPIRE_MINUTES * 60, REFRESH_TOKEN_EXPIRE_MINUTES * 60, '/', None, False,
                            True, 'lax')
        response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                            ACCESS_TOKEN_EXPIRE_MINUTES * 60, '/', None, False, False, 'lax')
        # return {"access_token": new_access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}
        return {"access_token": new_access_token, "token_type": "bearer"}
    except JWTError:
        raise error
