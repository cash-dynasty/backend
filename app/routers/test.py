from typing import Annotated

import schemas.user
from fastapi import APIRouter, Depends, Security
from settings import settings
from utils.auth import get_current_active_user


include_in_schema = True if settings.ENVIRONMENT in ["local", "dev"] else False

router = APIRouter(
    prefix="/test",
    tags=["test"],
    include_in_schema=include_in_schema,
)


@router.get("/")
def read_public_endpoint():
    return {"detail": "Hello from public endpoint!"}


@router.get("/protected")
def read_protected_endpoint(current_user: Annotated[schemas.user.User, Depends(get_current_active_user)]):
    return {"detail": "Hello from protected endpoint!"}


@router.get("/admin")
def read_admin_endpoint(
    current_user: Annotated[schemas.user.User, Security(get_current_active_user, scopes=["admin"])]
):
    return {"detail": "Hello from admin endpoint!"}
