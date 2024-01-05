from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import schemas.auth
from database import get_db
from settings import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES
from utils.auth import authenticate_user, create_access_token, create_refresh_token, authorize

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/token", response_model=schemas.auth.Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 response: Response, db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(data={"sub": user.email}, expires_delta=refresh_token_expires)

    response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                        ACCESS_TOKEN_EXPIRE_MINUTES * 60, '/', None, False, True, 'lax')
    response.set_cookie('refresh_token', refresh_token,
                        REFRESH_TOKEN_EXPIRE_MINUTES * 60, REFRESH_TOKEN_EXPIRE_MINUTES * 60, '/', None, False, True,
                        'lax')
    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                        ACCESS_TOKEN_EXPIRE_MINUTES * 60, '/', None, False, False, 'lax')
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/refresh")
async def login_for_refresh_token(token_data: dict = Depends(authorize)):
    return token_data
