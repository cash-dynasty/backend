import sys

import pydantic_core
import pytest


sys.path.append(".")
sys.path.append("./app")


import schemas.user  # noqa: E402

from app.routers.users import create_user  # noqa: E402


@pytest.mark.asyncio
async def test_create_user_success(dbsession):
    test_user = schemas.user.UserCreate(email="aaa@aaa.pl", password="aaa")
    new_user = await create_user(test_user, dbsession)
    assert new_user.email == test_user.email
    assert new_user.password == test_user.password


@pytest.mark.asyncio
async def test_create_user_wrong_email(dbsession):
    with pytest.raises(pydantic_core._pydantic_core.ValidationError) as EmailValidation:
        test_user = schemas.user.UserCreate(email="aaa@aaa", password="aaa")
        await create_user(test_user, dbsession)
    assert "value is not a valid email address" in EmailValidation.value.errors()[0]["msg"]
