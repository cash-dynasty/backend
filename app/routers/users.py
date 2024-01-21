import secrets
from datetime import datetime, timedelta

import models.user
import schemas.user
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import desc
from sqlalchemy.orm import Session
from utils.auth import get_password_hash


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


# 1. User utworzony poprawnie
# 2. Email niepoprawny
# 3. User z takim emailem już istnieje
# 4. Hasło za krótkie/długie, brak wymaganych znaków (obecnie tego nie sprawdzamy)
@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.user.UserCreateRes)
async def create_user(user: schemas.user.UserCreateReq, db: Session = Depends(get_db)):
    user_data = db.query(models.user.User).filter(models.user.User.email == user.email).first()
    if user_data:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    new_user = models.user.User(**user.model_dump())
    token = "".join(secrets.token_hex(32))
    token_expiration_date = (datetime.utcnow() + timedelta(hours=1)).isoformat()
    db.add(new_user)
    db.commit()
    new_token = models.user.ActivationToken(token=token, user_id=new_user.id, expiration_date=token_expiration_date)
    db.add(new_token)
    db.commit()
    # if "TESTING" not in os.environ:
    # send_user_create_confirmation_email(new_user.email, new_token.token)
    return new_user


# @router.patch("/activate/{email}/{token}", response_model=schemas.user.UserActivationRes)
@router.patch("/activate/{email}/{token}")
async def activate_user(email: str, token: str, db: Session = Depends(get_db)):
    user_data = (
        db.query(models.user.User)
        .outerjoin(models.user.ActivationToken)
        .where(models.user.User.email == email)
        .order_by(desc(models.user.ActivationToken.expiration_date))
    )

    print(user_data)

    # print(jsonable_encoder(user_data))
    # print(jsonable_encoder(user_data.activation_tokens))
    #
    # sorted_tokens = sorted(user_data.activation_tokens, key=lambda x: x.expiration_date, reverse=True)
    #
    # print(jsonable_encoder(sorted_tokens))

    # if not user_data:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    # if not user_data.activation_tokens[0].token == token:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    # if user_data.is_active:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already activated")
    # if datetime.fromisoformat(str(user_data.activation_tokens[0].expiration_date)) < datetime.utcnow():
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token expired")
    # user_data.is_active = True
    # user_data.activation_tokens[0].expiration_date = datetime.utcnow().isoformat()
    # db.commit()
    # db.refresh(user_data)
    return {"message": "OK"}


# TODO zrobić endpoint do generowania nowego tokena aktywacyjnego
