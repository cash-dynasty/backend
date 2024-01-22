from typing import Annotated

import schemas.user
from fastapi import APIRouter, Depends
from utils.auth import get_current_active_user


router = APIRouter(
    prefix="/test",
    tags=["test"],
    include_in_schema=False,
)


@router.get("/")
def read_public_endpoint():
    return {"message": "Hello from public endpoint!"}


@router.get("/protected")
def read_protected_endpoint(current_user: Annotated[schemas.user.User, Depends(get_current_active_user)]):
    return {"message": "Hello from protected endpoint!"}
