import sys
from datetime import timedelta
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


sys.path.append("./app")

from database import Base, get_db  # noqa: E402
from main import app  # noqa: E402
from settings import settings  # noqa: E402
from utils.auth import create_jwt_token  # noqa: E402
from utils.commons import get_current_time  # noqa: E402


SQLALCHEMY_DATABASE_URL = settings.POSTGRESQL_CONNECTION_URL_TEST

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture()
def user_data():
    return {"email": "arydlewski@cashdynasty.pl", "password": "password123"}


@pytest.fixture()
def inactive_user(client, user_data):
    with patch(
        "routers.users.generate_activation_token",
        return_value={
            "token": "test_token",
            "expiration_date": get_current_time() + timedelta(minutes=settings.ACTIVATION_TOKEN_EXPIRE_MINUTES),
        },
    ):
        with patch("routers.users.send_user_create_activation_email"):
            res = client.post("/users/create", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture()
def inactive_user_with_expired_activation_token(client, user_data):
    with patch(
        "routers.users.generate_activation_token",
        return_value={"token": "test_token", "expiration_date": get_current_time()},
    ):
        with patch("routers.users.send_user_create_activation_email"):
            res = client.post("/users/create", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture()
def user(client, inactive_user):
    res = client.patch("/users/activate", json={"email": inactive_user["email"], "token": "test_token"})
    assert res.status_code == 200
    new_user = res.json()
    new_user["password"] = inactive_user["password"]
    new_user["id"] = inactive_user["id"]
    assert new_user["is_active"]
    return new_user


@pytest.fixture()
def authorized_client(client, user):
    res = client.post(
        "/auth/token",
        data={"username": user["email"], "password": user["password"]},
    )
    assert res.status_code == 200
    access_token = res.json()["access_token"]
    client.headers = {**client.headers, "Authorization": f"Bearer {access_token}"}
    return client


@pytest.fixture()
def client_with_expired_token(client):
    access_token = create_jwt_token(
        data={"uid": 1},
        expires_delta=timedelta(-1),
        secret_key=settings.ACCESS_TOKEN_SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    client.headers = {**client.headers, "Authorization": f"Bearer {access_token}"}
    return client


@pytest.fixture()
def client_with_invalid_token(client):
    access_token = create_jwt_token(
        data={"uid": 1},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        secret_key=settings.ACCESS_TOKEN_SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    client.headers = {**client.headers, "Authorization": f"Bearer {access_token}x"}
    return client


@pytest.fixture()
def client_with_admin_permissions(client, user):
    access_token = create_jwt_token(
        data={"uid": user["id"], "scopes": ["admin"]},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        secret_key=settings.ACCESS_TOKEN_SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    client.headers = {**client.headers, "Authorization": f"Bearer {access_token}"}
    return client
