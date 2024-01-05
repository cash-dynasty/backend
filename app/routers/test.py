from fastapi import APIRouter, Depends

from utils.auth import get_current_active_user

# Na tą chwilę zostawiam. Jak uznasz, że możemy to wywalić, to feel free

router = APIRouter(
    prefix="/test",
    tags=["test"],
    dependencies=[Depends(get_current_active_user)],
)

router_public = APIRouter(
    prefix="/test",
    tags=["test"],
)


@router.get("/1", )
async def first_test_protected():
    return {"message": "first protected endpoint"}


@router.get("/2")
async def second_test_protected():
    return {"message": "second protected endpoint"}


@router_public.get("/3")
async def third_test_unprotected():
    return {"message": "unprotected endpoint"}
