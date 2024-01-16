import models.user
import schemas.user
from database import get_db
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from utils.auth import get_password_hash


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.user.UserCreateRes)
async def create_user(user: schemas.user.UserCreateReq, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    new_user = models.user.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
