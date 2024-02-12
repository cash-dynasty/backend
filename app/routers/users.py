import os
from datetime import datetime

import models.user
import schemas.user
from database import get_db
from exceptions import (
    AlreadyActivatedException,
    InvalidTokenException,
    TokenExpiredException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from utils.auth import get_password_hash, get_user_by_email
from utils.email import send_user_create_confirmation_email
from utils.generators import generate_activation_token


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.user.UserCreateRes)
async def create_user(user: schemas.user.UserCreateReq, db: Session = Depends(get_db)):
    user_data = db.query(models.user.User).filter(models.user.User.email == user.email).first()
    if user_data:
        raise UserAlreadyExistsException()
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    new_user = models.user.User(**user.model_dump())
    token = generate_activation_token()
    db.add(new_user)
    db.commit()
    new_token = models.user.ActivationToken(
        token=token["token"], user_id=new_user.id, expiration_date=token["expiration_date"]
    )
    db.add(new_token)
    db.commit()
    if "TESTING" not in os.environ:
        send_user_create_confirmation_email(new_user.email, new_token.token)
    return new_user


@router.patch("/activate", operation_id="activate_user", response_model=schemas.user.UserActivationRes)
async def activate_user(user: schemas.user.UserActivationReq, db: Session = Depends(get_db)):
    user_data = get_user_by_email(db, user.email)
    if not user_data:
        raise UserNotFoundException
    if user_data.is_active:
        raise AlreadyActivatedException

    token_data = (
        db.query(models.user.ActivationToken)
        .filter(models.user.ActivationToken.user_id == user_data.id)
        .order_by(models.user.ActivationToken.expiration_date.desc())
        .first()
    )

    if token_data.token != user.token:
        raise InvalidTokenException
    if token_data.expiration_date < datetime.utcnow():
        raise TokenExpiredException

    user_data.is_active = True
    token_data.expiration_date = datetime.utcnow().isoformat()
    db.commit()
    db.refresh(user_data)
    db.refresh(token_data)
    return user_data


# TODO zrobić endpoint do generowania nowego tokena aktywacyjnego
