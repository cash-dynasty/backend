import random

import fastapi
import pytest
from fastapi.testclient import TestClient
from utils.tests import inject_source_path

from app.routers.users import router


client = TestClient(router)

inject_source_path()


def test_create_user_success():
    mocked_email = f"user{random.randint(1000, 999999999)}@test.com"
    response = client.post("/users/create", json={"password": "testpassword", "email": mocked_email})
    assert response.status_code == 201
    assert response.json()["email"] == mocked_email


def test_create_user_wrong_email():
    mocked_wrong_email = "user"
    with pytest.raises(fastapi.exceptions.RequestValidationError) as EmailValidation:
        response = client.post("/users/create", json={"password": "testpassword", "email": mocked_wrong_email})
    assert "value is not a valid email" in EmailValidation.value.errors()[0]["msg"]