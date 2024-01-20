import os
import sys
from datetime import timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


sys.path.append("./app")

from database import Base, get_db  # noqa: E402
from main import app  # noqa: E402
from settings import settings  # noqa: E402
from utils.auth import create_access_token  # noqa: E402


SQLALCHEMY_DATABASE_URL = settings.POSTGRESQL_CONNECTION_URL_TEST

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def test_mode():
    os.environ["TESTING"] = "YES"
    yield
    os.environ.pop("TESTING", None)


@pytest.fixture()
def session():
    print("my session fixture ran")
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


@pytest.fixture
def test_user(client):
    user_data = {"email": "sanjeev@gmail.com", "password": "password123"}
    res = client.post("/users/create", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def active_test_user(client):
    user_data = {"email": "sanjeev@gmail.com", "password": "password123"}
    res = client.post("/users/create", json=user_data)

    assert res.status_code == 201

    res = client.patch("/users/activate", json={"email": user_data["email"]})

    assert res.status_code == 200

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def authorized_client(client, test_user):
    access_token = create_access_token(
        {"sub": test_user["email"]}, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    client.headers = {**client.headers, "Authorization": f"Bearer {access_token}"}
    return client


@pytest.fixture
def authorized_active_client(client, active_test_user):
    access_token = create_access_token(
        {"sub": active_test_user["email"]}, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    client.headers = {**client.headers, "Authorization": f"Bearer {access_token}"}
    return client
