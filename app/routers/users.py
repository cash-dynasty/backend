from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from utils import get_password_hash

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
